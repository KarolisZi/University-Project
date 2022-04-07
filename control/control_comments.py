from web_scraping import scrape_comments
from information_cleaning import clean_comments
from information_cleaning import helper_functions
from alive_progress import alive_bar
from database import db_crud_topics
from database import db_crud_comments
from values import constant
from database import create_table

"""
========================================================================================================================
CONTROL OPERATIONS FOR THE COMMENT PAGE DATA

    @create_first_database_post_one_page_comment_records_in_database():  populate the database with comments from first page
    @create_first_database_post__all_pages_comment_records_in_database(): populate the database with all comments from one topic
    @create_all_post_first_page_comment_records_in_database(): populate the database with the first page of every topic
    @create_all_post_all_pages_comment_records_in_database(): populate the database with all comments form all posts
    @populate_database_comment_page(): control how many comment pages to insert into the database
        @reverse - start reading comments from the last page
========================================================================================================================
"""


def populate_database_comments(check, reverse):
    # Fetch all URLs and IDs of the comments
    data = db_crud_topics.fetch_all_id_url_author()

    # Create database table for comments
    create_table.comments_proof()
    create_table.comments_participation()
    create_table.comments_author()

    match check:
        case "one_one":
            comment_first_post_one_page(data, reverse)
        case "one_all":
            comment_first_post_all_pages(data, reverse)
        case "all_one":
            comment_all_post_one_page(data, reverse)
        case "all_all":
            comment_all_post_all_pages(data, reverse)


def comment_first_post_one_page(data, reverse):
    url = ''

    links = scrape_comments.generate_comment_links(data[0][1])
    match reverse:
        case True:
            url = links[-1]
        case False:
            url = links[0]

    comments = scrape_comments.fetch_comments(url)
    cleaned_comments = clean_comments.clean(comments, data[0][2])
    topic_ids = helper_functions.get_topic_ids(url)

    insert_comment_data(topic_ids, cleaned_comments)


def comment_first_post_all_pages(data, reverse):
    links = scrape_comments.generate_comment_links(data[0][1])

    if reverse:
        links = list(reversed(links))

    with alive_bar(len(links), title='Post comments') as bar:
        # Go through all comments in all pages and store them in the database
        for link in links:
            comments = scrape_comments.fetch_comments(link)
            cleaned_comments = clean_comments.clean(comments, data[0][2])
            topic_ids = helper_functions.get_topic_ids(link)

            insert_comment_data(topic_ids, cleaned_comments)
            bar()


def comment_all_post_one_page(data, reverse):
    with alive_bar(len(data), title='Posts') as bar:
        for entry in data:

            links, url = scrape_comments.generate_comment_links(entry[1]), ''

            match reverse:
                case True:
                    url = links[-1]
                case False:
                    url = links[0]

            comments = scrape_comments.fetch_comments(url)
            cleaned_comments = clean_comments.clean(comments, entry[2])
            topic_ids = helper_functions.get_topic_ids(entry[1])

            insert_comment_data(topic_ids, cleaned_comments)
            bar()


def comment_all_post_all_pages(data, reverse):
    for entry in data:

        # Generate all page numbers
        links = scrape_comments.generate_comment_links(entry[1])

        if reverse:
            links = list(reversed(links))

        with alive_bar(len(links), title='Post comments') as bar_one_post:
            # Go through all comments in all pages and store them in the database
            for link in links:
                comments = scrape_comments.fetch_comments(link)
                cleaned_comments = clean_comments.clean(comments, entry[2])
                topic_ids = helper_functions.get_topic_ids(link)

                insert_comment_data(topic_ids, cleaned_comments)
                bar_one_post()


"""
========================================================================================================================
HELPER FUNCTIONS
========================================================================================================================
"""


def print_insertion_message(ids, len_proof, len_participation):
    print('Inserting %s comments to %s, %s comments to %s, topic_id = %s.%s' % (
        len_proof, constant.DB_PROOF, len_participation, constant.DB_PARTICIPATION, ids[0], ids[1]))


def insert_comment_data(topic_ids, comments_c):
    print_insertion_message(topic_ids, len(comments_c[0]), len(comments_c[1]))
    db_crud_comments.insert_proof_comments(topic_ids[0], topic_ids[1], comments_c[0])
    db_crud_comments.insert_participation_comments(topic_ids[0], topic_ids[1], comments_c[1])
    db_crud_comments.insert_author_comments(topic_ids[0], comments_c[2])
    db_crud_topics.insert_spreadsheet_ids(topic_ids[0], comments_c[3])
