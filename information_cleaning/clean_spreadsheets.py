from values import regex

social_platforms = ['FACEBOOK', 'TWITTER', 'REDDIT', 'YOUTUBE', 'LINKEDIN', 'INSTAGRAM', 'TIKTOK', 'ARTICLE', 'VIDEO', 'BLOG', 'MEDIUM', 'DISCORD', 'SIGNATURE', 'TRANSLATION']

"""
========================================================================================================================

EXTRACT INFORMATION FROM GOOGLE SPREADSHEETS

@ clean_sheets_data() - extracts data from spreadsheets for storage in the database

========================================================================================================================
"""


def clean_sheets_data(data):
    result_array = []

    timestamp, forum_username, profile_link, social_username, followers, telegram_username = None, None, None, None, None, None

    for index in range(0, len(data[0])):

        if 'TIMESTAMP' in data[0][index].upper():
            timestamp = index
        elif 'USER' in data[0][index].upper() and 'NAME' in data[0][index].upper() and 'BITCOINTALK' in data[0][index].upper() or 'FORUM' in data[0][index].upper():
            forum_username = index
        elif 'PROFILE' in data[0][index].upper() and 'LINK' in data[0][index].upper() or 'URL' in data[0][index].upper():
            profile_link = index
        elif 'FOLLOWERS' in data[0][index].upper():
            followers = index
        elif 'TELEGRAM' in data[0][index].upper() and 'USERNAME'  in data[0][index].upper():
            telegram_username = index
        for platform in social_platforms:
            if platform in data[0][index].upper() and 'USERNAME' in data[0][index].upper() or 'LINK' in data[0][index].upper() or 'URL' in data[0][index].upper():
                social_username = index

    for i in range(1, len(data)):

        result = [i + 1]

        if timestamp is not None:
            result.append(data[i][timestamp])
        else:
            result.append('none')

        if forum_username is not None:
            result.append(data[i][forum_username])
        else:
            result.append('none')

        if profile_link is not None and regex.profile_url_format.match(data[i][profile_link]):
            result.append(data[i][profile_link])
        else:
            result.append('none')

        if social_username is not None:
            result.append(data[i][social_username])
        else:
            result.append('none')

        if followers is not None:
            result.append(data[i][followers])
        else:
            result.append('none')

        if telegram_username is not None:
            result.append(data[i][telegram_username])
        else:
            result.append('none')

        result_array.append(result)

    # ROW, TIMESTAMP, FORUM USERNAME, PROFILE LINK, SOCIAL MEDIA USERNAME, TELEGRAM USERNAME
    return result_array

