from values import regex

social_platforms = ['TWITTER', 'FACEBOOK', 'REDDIT', 'YOUTUBE', 'LINKEDIN', 'INSTAGRAM', 'TELEGRAM']


"""
========================================================================================================================

EXTRACT INFORMATION FROM GOOGLE SPREADSHEETS

@ clean_sheets_data() - extracts data from spreadsheets for storage in the database

========================================================================================================================
"""


def clean_sheets_data(data):
    result_array = []

    timestamp, forum_username, profile_link, social_username, followers = None, None, None, None, None

    for index in range(0, len(data[0])):

        if 'TIMESTAMP' in data[0][index].upper():
            timestamp = index
        elif 'FORUM USERNAME' in data[0][index].upper():
            forum_username = index
        elif 'PROFILE' and 'LINK' in data[0][index].upper():
            profile_link = index
        elif 'FOLLOWERS' in data[0][index].upper():
            followers = index

        for platform in social_platforms:
            if platform in data[0][index].upper() and 'USERNAME' in data[0][index].upper():
                social_username = index

    for i in range(1, len(data)):

        result = [i + 1]

        if timestamp is not None:
            result.append(data[i][timestamp])
        else:
            result.append('None')

        if forum_username is not None:
            result.append(data[i][forum_username])
        else:
            result.append('None')

        if profile_link is not None and regex.profile_url_format.match(data[i][profile_link]):
            result.append(data[i][profile_link])
        else:
            result.append('None')

        if social_username is not None:
            result.append(data[i][social_username])
        else:
            result.append('None')

        if followers is not None:
            result.append(data[i][followers])
        else:
            result.append('None')

        result_array.append(result)

    # ROW, TIMESTAMP, FORUM USERNAME, PROFILE LINK, SOCIAL MEDIA USERNAME
    return result_array

