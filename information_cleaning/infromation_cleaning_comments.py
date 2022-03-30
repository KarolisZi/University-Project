from web_scraping import scrape_google_spreadsheet
from information_cleaning import helper_functions
import re

"""
================================================================================================================
DATA CLEANING PART FOR COMMENT SECTION DATA

 @ clean_comment_section_data - filters the comments and retrieves useful information

================================================================================================================
"""


def clean_comment_section_data(comments, topic_author):
    proof_comments = []
    author_comments = []
    participation_comments = []

    for comment in comments:

        poster_info = comment.find('td', class_="poster_info")
        forum_username = poster_info.find('a').text

        if "PROOF" in str(comment.text.upper()) and forum_username != topic_author:
            proof_comments.append(comment)
        elif forum_username == topic_author:
            author_comments.append(comment)
        else:
            participation_comments.append(comment)

    cleaned_proof_comments = extract_data_from_proof_comments(proof_comments)

    cleaned_participation_comments = extract_data_from_participation_comments(participation_comments)

    sheet_ids = extract_spreadsheet_ids_from_comments(author_comments)

    return [cleaned_proof_comments, cleaned_participation_comments, sheet_ids]


# Clean and extract the data from proof comments
def extract_data_from_proof_comments(proof_comments):
    results = []
    eth_patter = re.compile('/^0x[a-fA-F0-9]{40}$/g')

    for comment in proof_comments:

        telegram_username = ""
        campaigns = ""
        address = ""
        data = []

        # Retrieve forum username and link
        poster_info = comment.find('td', class_="poster_info")
        forum_username = poster_info.find('a').text
        profile_url = poster_info.find('a').get('href')

        # Retrieve post and header
        header_post = comment.find('td', class_="td_headerandpost")

        # Retrieve comment_id from the header
        comment_id = header_post.find('a', class_='message_number').text.replace("#", "")

        # Retrieve time from the header
        time = header_post.find('div', class_='smalltext').text

        if 'Last edit:' in time:
            temp = time.split('Last edit:')
            time = temp[0].strip()

        time = helper_functions.convert_time(time)

        # Retrieve post from header and post
        post = header_post.find('div', class_='post').text.split("\n")

        for text in post:

            # Telegram user name
            if "TELEGRAM" and "USER" and "NAME" in text.upper():
                temp = text.replace(":", " : ")
                temp = temp.split(":")
                telegram_username = temp[-1].rstrip().lstrip()

            elif "CAMPAIGN" in text.upper():
                temp = text.split(":")
                campaigns = temp[-1].rstrip().lstrip()
            elif "ADDRESS" in text.upper():
                temp = text.split(":")
                if eth_patter.match(temp[-1].rstrip().lstrip()):
                    address = temp[-1].rstrip().lstrip()
            else:
                data.append(text)

        results.append([comment_id, forum_username, profile_url, telegram_username, campaigns, time, address])

    return results


# Clean and extract the data from participation comments
def extract_data_from_participation_comments(participation_comments):
    result = []

    url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

    twitter_url_pattern = re.compile('https\:\/\/(www.)?(mobile.)?twitter\.com\/\w*')
    facebook_url_pattern = re.compile('https\:\/\/(www.)?(web.)?(m.)?facebook\.com\/\w*')
    telegram_url_pattern = re.compile('https\:\/\/(www.)?t\.me\/\w*')
    instagram_url_pattern = re.compile('https\:\/\/(www.)?instagram\.com\/\w*')
    reddit_url_pattern = re.compile('https\:\/\/(www.)reddit\.com\/\w*')

    for comment in participation_comments:

        week = []
        participation = []

        twitter_links = []
        facebook_links = []
        instagram_links = []
        telegram_links = []
        reddit_links = []
        other_links = []

        social_media_profile_url = ''

        # Retrieve forum username and link
        poster_info = comment.find('td', class_="poster_info")
        forum_username = poster_info.find('a').text
        forum_profile_url = poster_info.find('a').get('href')

        # Retrieve post and header
        header_post = comment.find('td', class_="td_headerandpost")

        # Retrieve comment_id from the header
        comment_id = header_post.find('a', class_='message_number').text.replace("#", "")

        # Retrieve time from the header
        time = header_post.find('div', class_='smalltext').text

        if 'Last edit:' in time:
            temp = time.split('Last edit:')
            time = temp[0].strip()

        time = helper_functions.convert_time(time)

        # Retrieve post from header and post
        comment_lines = header_post.find('div', class_='post').text.split('\n')

        for line in comment_lines:

            if "WEEK" in line.upper():
                week = line

            urls = re.findall(url_regex, line)

            if len(urls) > 0:
                if twitter_url_pattern.match(urls[0][0]):
                    twitter_links.append(urls[0][0])
                    if 'Twitter' not in participation:
                        participation.append('Twitter')
                elif facebook_url_pattern.match(urls[0][0]):
                    facebook_links.append(urls[0][0])
                    if 'Facebook' not in participation:
                        participation.append('Facebook')
                elif instagram_url_pattern.match(urls[0][0]):
                    instagram_links.append(urls[0][0])
                    if 'Instagram' not in participation:
                        participation.append('Instagram')
                elif telegram_url_pattern.match(urls[0][0]):
                    telegram_links.append(urls[0][0])
                    if 'Telegram' not in participation:
                        participation.append('Telegram')
                elif reddit_url_pattern.match(urls[0][0]):
                    reddit_links.append(urls[0][0])
                    if 'Reddit' not in participation:
                        participation.append('Reddit')
                else:
                    other_links.append(urls[0][0])
                    if 'Other' not in participation:
                        participation.append('Other')

        links = [twitter_links, facebook_links]

        result.append(
            [comment_id, forum_username, forum_profile_url, week, social_media_profile_url, links, participation, time])

    return result


"""
================================================================================================================

FUNCTIONS TO EXTRACT SPREADSHEET LINKS AND DATA

================================================================================================================
"""


# Clean and extract the data from google spreadsheets comments
def extract_spreadsheet_ids_from_comments(author_comments):

    sheet_ids = []

    links = get_spreadsheet_links_from_comments(author_comments)

    for link in links:

        deconstructed = link.split('/')

        sheet_ids.append(deconstructed[5])

    return sheet_ids


def get_spreadsheet_links_from_comments(author_comments):
    spreadsheet_links = []

    spreadsheet_pattern = re.compile('https\:\/\/(www.)?docs\.google\.com\/spreadsheets\/\w*')

    for comment in author_comments:

        # Retrieve post and header
        header_post = comment.find('td', class_="td_headerandpost")

        # Retrieve comment_id from the header
        comment_id = header_post.find('a', class_='message_number').text.replace("#", "")

        # if comment_id == 1:

        comment_lines = header_post.find('div', class_='post')

        if (len(comment_lines)) > 0:

            post_links = comment_lines.find_all('a', class_='ul')

            for link in post_links:

                if spreadsheet_pattern.match(link.get('href')):
                    spreadsheet_links.append(link.get('href'))

    return spreadsheet_links
