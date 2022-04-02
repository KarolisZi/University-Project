social_platforms = ['TWITTER', 'FACEBOOK', 'REDDIT', 'YOUTUBE', 'LINKEDIN', 'INSTAGRAM', 'TELEGRAM']
from values import regex

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

