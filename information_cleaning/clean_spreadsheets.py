from values import regex
from classes.google_sheet import Sheet

social_platforms = ['FACEBOOK', 'TWITTER', 'REDDIT', 'YOUTUBE', 'LINKEDIN', 'INSTAGRAM', 'TIKTOK', 'ARTICLE', 'VIDEO',
                    'BLOG', 'MEDIUM', 'DISCORD', 'SIGNATURE', 'TRANSLATION']

"""
========================================================================================================================

EXTRACT INFORMATION FROM GOOGLE SPREADSHEETS

========================================================================================================================
"""


# Extract useful information form the retrieved data
def clean_sheets_data(data):
    results = []

    i = get_index(data)

    if i:
        timestamp, forum_username, profile_link, social_username, = i[0], i[1], i[2], i[3]
        followers, telegram_username, data_row = i[4], i[5], i[6]

        for index, row in enumerate(data):

            if index >= data_row:

                sheet = Sheet(None, None, None, None, None, None, None, None, None)

                sheet.set_row(index + 1)

                if timestamp:
                    sheet.set_timestamp(row[timestamp])
                if forum_username:
                    sheet.set_forum_username(row[forum_username])
                if profile_link and regex.profile_url_format.match(row[profile_link]):
                    sheet.set_profile_url(row[profile_link])
                if social_username:
                    sheet.set_social_media_username(row[social_username])
                if followers:
                    sheet.set_followers(row[followers])
                if telegram_username:
                    sheet.set_telegram_username(row[telegram_username])

                results.append(sheet)

    return results


# Index columns based on column name
def get_index(data):
    results, first_find = [], True

    for i, row in enumerate(data):

        found, timestamp, forum_username, profile_link, social_username, followers, telegram_username = 0, None, None, None, None, None, None
        soft_found, soft_timestamp, soft_forum_username, soft_profile_link, soft_social_username, soft_followers, soft_telegram_username = 0, None, None, None, None, None, None

        for index, cell in enumerate(row):

            if 'TIMESTAMP' in cell.upper():
                soft_timestamp, timestamp = index, index
            elif 'USER' in cell.upper() and 'NAME' in cell.upper():
                soft_forum_username = index
                if 'BITCOINTALK' in cell.upper() or 'FORUM' in cell.upper():
                    forum_username = index
            elif 'PROFILE' in cell.upper() and 'LINK' in cell.upper() or 'URL' in cell.upper():
                soft_profile_link, profile_link = index, index
            elif 'FOLLOWERS' in cell.upper():
                followers, soft_followers = index, index
            elif 'TELEGRAM' in cell.upper():
                soft_telegram_username = index
                if 'USERNAME' in cell.upper():
                    telegram_username = index
            for platform in social_platforms:
                soft_social_username = index
                if platform in cell.upper() and 'USERNAME' in cell.upper() or 'LINK' in cell.upper() or 'URL' in cell.upper():
                    social_username = index

        found = calculate_found(timestamp, forum_username, profile_link, social_username, followers, telegram_username)
        soft_found = calculate_found(soft_timestamp, soft_forum_username, soft_profile_link, soft_social_username,
                                     soft_followers, soft_telegram_username)

        if found >= 3 and first_find:
            results = [timestamp, forum_username, profile_link, social_username, followers, telegram_username, i + 2]
            first_find = False
        elif soft_found >= 3 and not first_find:
            results[6] = i + 2
            return results
        if i >= 10:
            return results


# Calculate how many data types were found
def calculate_found(timestamp, forum_username, profile_link, social_username, followers, telegram_username):
    found = 0

    if timestamp:
        found += 1
    if forum_username:
        found += 1
    if profile_link:
        found += 1
    if social_username:
        found += 1
    if followers:
        found += 1
    if telegram_username:
        found += 1

    return found
