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

    # Clean raw text comments here:

    # [raw_text, image_urls, image_check, comment_index]
    return text_image


def filter_comments(author_comments):

    results = []
    raw_text, image_urls, image_check, comment_index = '', [], None, ''

    if author_comments:

        for i in range(0, len(author_comments)):

            comment_index = i+1

            image_urls = retrieve_author_post_image_links(author_comments[i])

            raw_text = author_comments[i]

            if not image_urls:
                # Full raw_text
                image_check = False
            elif image_urls:
                image_check = True

            results.append([raw_text, image_urls, image_check, comment_index])

    return results


def retrieve_author_post_image_links(comment):
    image_urls = []

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
