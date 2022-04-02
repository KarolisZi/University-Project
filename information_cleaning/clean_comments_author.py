import urllib.parse
from values import regex

"""
========================================================================================================================
DATA CLEANING PART FOR AUTHOR COMMENT SECTION DATA

 @ extract_data_from_author_comments() - extracts data from author comments
========================================================================================================================
"""


def extract_data_from_author_comments(author_comments):
    author_comments_text = []

    if len(author_comments[0].text) > 2000:

        for comment in author_comments:
            author_comments_text.append(comment.text)
    else:
        urls = retrieve_author_image_post_urls(author_comments)

    return [urls, author_comments_text]


def retrieve_author_image_post_urls(author_comments):
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
