from information_cleaning import clean_comments_proof
from information_cleaning import clean_comments_participation
from information_cleaning import clean_comments_author
from information_cleaning import clean_spreadsheets
from values import regex


"""
========================================================================================================================
DATA CLEANING PART FOR COMMENT SECTION DATA

 @ clean_comment_section_data() - filters and separates comments: proof, participation and author
 @ extract_data_from_proof_comments() - extracts data from proof comments for storage in the database
 @ extract_data_from_participation_comments() - extracts data from participation comments for storage in the database
    @ filter_url - filters urls and finds usernames, social media platforms used
 @ extract_data_from_author_comments() - extracts data from author comments
========================================================================================================================
"""

"""
GENERAL SORTING OF COMMENTS: PROOF, PARTICIPATION and AUTHOR
    AUTHOR COMMENTS: SHEET_IDS, IMAGE COMMENTS, TEXT COMMENTS

Returns 3 arrays of comments
"""


def filter_comment_section_data(comments, topic_author):
    proof_comments = []
    author_comments = []
    participation_comments = []

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

    cleaned_proof_comments = clean_comments_proof.extract_data_from_proof_comments(proof_comments)

    cleaned_participation_comments = clean_comments_participation.extract_data_from_participation_comments(participation_comments)

    cleaned_author_comments = clean_comments_author.extract_data_from_author_comments(author_comments)

    sheet_ids = clean_spreadsheets.extract_spreadsheet_ids_from_comments(author_comments)

    return [cleaned_proof_comments, cleaned_participation_comments, sheet_ids, cleaned_author_comments]

