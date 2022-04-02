from information_cleaning import clean_comments_proof
from information_cleaning import clean_comments_participation
from information_cleaning import clean_comments_author

"""
========================================================================================================================
DATA CLEANING PART FOR COMMENT SECTION DATA

 @ clean() - calls data cleaning functions on each of the 3 categories + retrieves sheet_ids from author comments
 @ filter_comment_section_data() - filters the comments into 3 categories: PROOF, PARTICIPATION, AUTHOR

========================================================================================================================
"""


def clean(comments, topic_author):

    proof_participation_author = filter_comment_section_data(comments, topic_author)

    cleaned_proof_comments = clean_comments_proof.clean_comments(proof_participation_author[0])

    cleaned_participation_comments = clean_comments_participation.clean_comments(proof_participation_author[1])

    cleaned_author_comments = clean_comments_author.clean_comments(proof_participation_author[2])

    sheet_ids = clean_comments_author.extract_spreadsheet_ids(proof_participation_author[2])

    return [cleaned_proof_comments, cleaned_participation_comments, cleaned_author_comments, sheet_ids]


def filter_comment_section_data(comments, topic_author):
    proof_comments, participation_comments, author_comments = [], [], []

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

    return [proof_comments, participation_comments, author_comments]
