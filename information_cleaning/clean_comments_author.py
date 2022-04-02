import urllib.parse
from values import regex

"""
========================================================================================================================
DATA CLEANING PART FOR AUTHOR COMMENT SECTION DATA

 @ extract_data_from_author_comments() - extracts data from author comments
========================================================================================================================
"""


def clean_comments(author_comments):

    text_image = filter_comments(author_comments)

    print(text_image[1])

    return text_image


def filter_comments(author_comments):
    raw_text, image_links = [], []

    if len(author_comments) > 0:

        if len(author_comments[0].text) > 2000:

            for comment in author_comments:
                raw_text.append(comment.text)
        else:
            image_links = retrieve_author_post_image_links(author_comments)

    return [raw_text, image_links]


def retrieve_author_post_image_links(author_comments):
    image_urls = []

    for comment in author_comments:

        img_tags = comment.find_all('img')

        for tag in img_tags:

            url = tag.get('src')

            if regex.image_proxy_pattern.match(url):
                url = url.replace('https://ip.bitcointalk.org/?u=', '')

                url = urllib.parse.unquote(url)

                temp = url.split('&')

                url = temp[0]

                image_urls.append(url)

    return image_urls


"""
========================================================================================================================

FUNCTIONS TO EXTRACT SPREADSHEET LINKS AND IDS FROM AUTHOR COMMENTS

@ get_spreadsheet_links_from_comments() - extract spreadsheet links from author comments
@ extract_spreadsheet_ids_from_comments() - extracts spreadsheet ids from spreadsheet links

========================================================================================================================
"""


def extract_spreadsheet_links(author_comments):
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


def extract_spreadsheet_ids(author_comments):

    sheet_ids = []

    links = extract_spreadsheet_links(author_comments)

    for link in links:

        deconstructed = link.split('/')

        sheet_ids.append(deconstructed[5])

    return sheet_ids
