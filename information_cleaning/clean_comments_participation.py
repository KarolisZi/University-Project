from values import regex
from information_cleaning import helper_functions
from classes.comment_participation import Participation
import re

"""
========================================================================================================================

DATA CLEANING FOR PARTICIPATION COMMENTS

========================================================================================================================
"""


# Prepare comments for storage in the database
def clean_comments(participation_comments):
    result = []

    for comment in participation_comments:

        participation = Participation(None, None, None, None, None, [], None, [], None, None)

        # RETRIEVE FORUM USERNAME AND LINK
        poster_info = comment.find('td', class_="poster_info")
        participation.set_forum_username(poster_info.find('a').text)
        participation.set_forum_profile_url(poster_info.find('a').get('href'))

        # RETRIEVE COMMENT ID AND POST TIME
        time_id = helper_functions.extract_post_time_and_id(comment)
        participation.set_post_time(time_id[0])
        participation.set_comment_id(time_id[1])

        # RETRIEVE POST FROM THE COMMENT
        comment_full = comment.find('div', class_='post').text
        comment_lines = comment_full.split('\n')

        for line in comment_lines:

            # Extract DAYS AND WEEKS
            if "WEEK" in line.upper() or "DAY" in line.upper():

                dates, string = [], ''

                for match in re.finditer(regex.day_month, line):
                    dates.append(line[match.start(): match.end()])
                if dates is not None:
                    for date in dates:
                        string += date
                        string += ' - '
                    string = string[:-3]
                    if string != '':
                        participation.set_week(string)

        urls = re.findall(regex.url_regex, comment_full)

        filter_url(urls, participation)

        result.append(participation)

    return result


# Analyse URL contained in a comment and sorted them based on the URL type
def filter_url(urls, participation_object):
    social_media_handle, participation = [], []
    twitter_links, facebook_links, instagram_links, telegram_links, reddit_links, other_links = [], [], [], [], [], []
    twitter_username, facebook_username = None, None

    for url in urls:
        # ================== TWITTER ==================
        if regex.twitter_url_pattern.match(url):

            twitter_username = url.split('/')[3]

            if not regex.twitter_username_url_pattern.match(url):
                twitter_links.append(url)

            if 'Twitter' not in participation:
                participation.append('Twitter')

        # ================== FACEBOOK ==================
        elif regex.facebook_url_pattern.match(url):

            if not regex.facebook_username_url_pattern.match(url):
                facebook_links.append(url)
                facebook_username = url.split('/')[-1]

            if 'Facebook' not in participation:
                participation.append('Facebook')
        # ================== INSTAGRAM ==================
        elif regex.instagram_url_pattern.match(url):
            instagram_links.append(url)
            if 'Instagram' not in participation:
                participation.append('Instagram')
        # ================== TELEGRAM ==================
        elif regex.telegram_url_pattern.match(url):
            telegram_links.append(url)
            if 'Telegram' not in participation:
                participation.append('Telegram')
        # ================== REDDIT ==================
        elif regex.reddit_url_pattern.match(url):
            reddit_links.append(url)
            if 'Reddit' not in participation:
                participation.append('Reddit')
        # ================== OTHER ==================
        else:
            if 'bitcointalk.org' not in url:
                other_links.append(url)
                if 'Other' not in participation:
                    participation.append('Other')

    if twitter_username is not None:
        social_media_handle.append('Twitter:' + twitter_username)
    if facebook_username is not None:
        social_media_handle.append('Facebook:' + facebook_username)

    participation_object.set_twitter_links(twitter_links)
    participation_object.set_facebook_links(facebook_links)
    participation_object.set_instagram_links(instagram_links)
    participation_object.set_telegram_links(telegram_links)
    participation_object.set_reddit_links(reddit_links)
    participation_object.set_other_links(other_links)

    participation_object.set_social_media_handle(social_media_handle)
    participation_object.set_participation(participation)
