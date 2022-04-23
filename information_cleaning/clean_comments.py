from information_cleaning import clean_comments_proof
from information_cleaning import clean_comments_participation
from information_cleaning import clean_comments_author
from classes.topic import Topic

"""
========================================================================================================================
DATA CLEANING PART FOR COMMENT SECTION DATA

 @ clean() - calls data cleaning functions on each of the 3 categories + retrieves sheet_ids from author comments
 @ filter_comment_section_data() - filters the comments into 3 categories: PROOF, PARTICIPATION, AUTHOR

========================================================================================================================
"""


def clean(comments, topic_author, tables, topic_id):

    cleaned_proof_comments, cleaned_participation_comments, cleaned_author_comments = [], [], []
    topic = Topic()

    proof_participation_author = filter_comment_section_data(comments, topic_author)

    if 'proof' in tables:
        cleaned_proof_comments = clean_comments_proof.clean_comments(proof_participation_author[0])

    if 'participation' in tables:
        cleaned_participation_comments = clean_comments_participation.clean_comments(proof_participation_author[1])

    if 'author' in tables:
        cleaned_author_comments = clean_comments_author.clean_comments(proof_participation_author[2], topic_id)
        topic.set_sheet_ids(clean_comments_author.extract_spreadsheet_ids(proof_participation_author[2]))

    return [cleaned_proof_comments, cleaned_participation_comments, cleaned_author_comments, topic]


def filter_comment_section_data(comments, topic_author):
    proof_comments, participation_comments, author_comments = [], [], []

    for comment in comments:

        poster_info = comment.find('td', class_="poster_info")

        if type(poster_info) is not None and poster_info is not None:

            forum_username = poster_info.find('a').text
            text = str(comment.text.upper())

            if forum_username == topic_author:
                author_comments.append(comment)
            elif "DAY" in text or "WEEK" in text and forum_username != topic_author and 'PROOF' not in text:
                participation_comments.append(comment)
            elif 'PROOF' in text:
                proof_comments.append(comment)
            elif 'ADDRESS' in text and 'TELEGRAM' in text and 'USERNAME' in text and 'FORUM' in text:
                proof_comments.append(comment)

    return [proof_comments, participation_comments, author_comments]
