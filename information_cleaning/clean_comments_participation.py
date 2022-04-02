from values import regex
from information_cleaning import helper_functions
import re


def clean_comments(participation_comments):
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

        result.append(
            [comment_id, forum_username, forum_profile_url, week, us_li_pa[0], us_li_pa[1], us_li_pa[2], time])

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
