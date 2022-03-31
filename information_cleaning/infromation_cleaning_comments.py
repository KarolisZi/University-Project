from web_scraping import scrape_google_spreadsheet
from information_cleaning import helper_functions
from values import regex
import re

"""
========================================================================================================================
DATA CLEANING PART FOR COMMENT SECTION DATA

 @ clean_comment_section_data() - filters and separates comments: proof, participation and author
 @ extract_data_from_proof_comments() - extracts data from proof comments for storage in the database
 @ extract_data_from_participation_comments() - extracts data from participation comments for storage in the database
 @ filter_url - filters urls and finds usernames, social media platforms used
========================================================================================================================
"""


def filter_comment_section_data(comments, topic_author):
    proof_comments = []
    author_comments = []
    participation_comments = []

    for comment in comments:

        poster_info = comment.find('td', class_="poster_info")

        if type(poster_info) is not None and poster_info is not None:

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


def extract_data_from_proof_comments(proof_comments):
    results = []

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
                if regex.eth_patter.match(temp[-1].rstrip().lstrip()):
                    address = temp[-1].rstrip().lstrip()
            else:
                data.append(text)

        results.append([comment_id, forum_username, profile_url, telegram_username, campaigns, time, address])

    return results


def extract_data_from_participation_comments(participation_comments):

    result = []

    for comment in participation_comments:

        week = None
        us_li_pa = [[], [], []]

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

            urls = re.findall(regex.url_regex, line)

            if len(urls) > 0:
                # Usernames, links, participation
                us_li_pa = filter_url(urls[0][0])


        result.append([comment_id, forum_username, forum_profile_url, week, us_li_pa[0], us_li_pa[1], us_li_pa[2], time])

    return result


def filter_url(url):

    links, social_media_usernames, week, participation, twitter_links, facebook_links, instagram_links, telegram_links, reddit_links, other_links = [], [], [], [], [], [], [], [], [], []
    twitter_username, facebook_username = None, None

    # Twitter links and username extraction
    if regex.twitter_url_pattern.match(url):

        url_decomposed = url.split('/')
        twitter_username = url_decomposed[3]

        if 'Twitter' not in participation:
            participation.append('Twitter')

        if not regex.twitter_username_url_pattern.match(url):
            twitter_links.append(url)

    # Facebook links and username extraction
    elif regex.facebook_url_pattern.match(url):

        if not regex.facebook_username_url_pattern.match(url):
            facebook_links.append(url)
        else:
            url_decomposed = url.split('/')
            facebook_username = url_decomposed[-1]

        if 'Facebook' not in participation:
            participation.append('Facebook')

    elif regex.instagram_url_pattern.match(url):
        instagram_links.append(url)
        if 'Instagram' not in participation:
            participation.append('Instagram')
    elif regex.telegram_url_pattern.match(url):
        telegram_links.append(url)
        if 'Telegram' not in participation:
            participation.append('Telegram')
    elif regex.reddit_url_pattern.match(url):
        reddit_links.append(url)
        if 'Reddit' not in participation:
            participation.append('Reddit')
    else:
        other_links.append(url)
        if 'Other' not in participation:
            participation.append('Other')

    if twitter_username is not None:
        social_media_usernames.append(twitter_username)
    if facebook_username is not None:
        social_media_usernames.append(facebook_username)

    if len(twitter_links) > 0:
        links.append(twitter_links)
    if len(facebook_links) > 0:
        links.append(facebook_links)

    return [social_media_usernames, links, participation]


"""
========================================================================================================================

FUNCTIONS TO EXTRACT SPREADSHEET LINKS AND IDS FROM AUTHOR COMMENTS

@ get_spreadsheet_links_from_comments() - extract spreadsheet links from author comments
@ extract_spreadsheet_ids_from_comments() - extracts spreadsheet ids from spreadsheet links

========================================================================================================================
"""


def get_spreadsheet_links_from_comments(author_comments):
    spreadsheet_links = []

    for comment in author_comments:

        # Retrieve post and header
        header_post = comment.find('td', class_="td_headerandpost")

        # Retrieve comment_id from the header
        # comment_id = header_post.find('a', class_='message_number').text.replace("#", "")
        # if comment_id == 1:

        comment_lines = header_post.find('div', class_='post')

        if (len(comment_lines)) > 0:

            post_links = comment_lines.find_all('a', class_='ul')

            for link in post_links:

                if regex.spreadsheet_pattern.match(link.get('href')):
                    spreadsheet_links.append(link.get('href'))

    return spreadsheet_links


def extract_spreadsheet_ids_from_comments(author_comments):
    sheet_ids = []

    links = get_spreadsheet_links_from_comments(author_comments)

    for link in links:
        deconstructed = link.split('/')

        sheet_ids.append(deconstructed[5])

    return sheet_ids
