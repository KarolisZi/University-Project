from web_scraping import scrape_topics
from web_scraping import scrape_comments
from database import db_crud_topics
from database import db_crud_comments
from database import create_table
from database import db_crud_sheets
from values import constant
from information_cleaning import clean_topic
from information_cleaning import clean_comments
from information_cleaning import clean_spreadsheets
from web_scraping import scrape_sheets
from information_cleaning import helper_functions

"""
================================================================================================
CONTROL OPERATIONS FOR THE MAIN PAGE DATA (TOPICS):
    @create_one_page_post_records_in_database(): scrape the first page of the forum
    @create_all_post_records_in_database(): scrape all pages of the forum
    @populate_database_main_page(): create database, choose how many pages to scrape
================================================================================================
"""


# Create records of every post in the given URL that includes [BOUNTY] in the name
def create_one_page_post_records_in_database():
    results, url = [], constant.FIRST_PAGE_URL

    topics = scrape_topics.fetch_post_data(url)

    for topic in topics:
        cleaned_topic_data = clean_topic.clean_topic_data(topic)
        results.append(cleaned_topic_data)

    db_crud_topics.insert_entry(results)


# Create records of every post that includes [BOUNTY] in the name
def create_all_post_records_in_database():
    # Generates all forum post pages from the first to last URL
    all_urls = scrape_topics.generate_all_post_page_links()

    # Fetch every post in every page that has "BOUNTY" in the name
    for url in all_urls:

        results = []

        # Retrieve all topics from a link
        all_topics = scrape_topics.fetch_post_data(url)

        # Clean every topic in a link and insert it into the database
        for topic in all_topics:
            cleaned_topic_data = clean_topic.clean_topic_data(topic)
            results.append(cleaned_topic_data)

        db_crud_topics.insert_entry(results)


def populate_database_main(amount):
    create_table.create_home_page_database()

    match amount:
        case "one":
            create_one_page_post_records_in_database()
        case "all":
            create_all_post_records_in_database()


"""
================================================================================================
CONTROL OPERATIONS FOR THE COMMENT PAGE DATA
    @create_first_database_post_one_page_comment_records_in_database():  populate the database with comments from first page
    @create_first_database_post__all_pages_comment_records_in_database(): populate the database with all comments from one topic
    @create_all_post_first_page_comment_records_in_database(): populate the database with the first page of every topic
    @create_all_post_all_pages_comment_records_in_database(): populate the database with all comments form all posts
    @populate_database_comment_page(): control how many comment pages to insert into the database
        @reverse - start reading comments from the last page
================================================================================================
"""


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

    # Go through all comments in all pages and store them in the database
    for link in links:
        comments = scrape_comments.fetch_comments(link)
        cleaned_comments = clean_comments.clean(comments, data[0][2])
        topic_ids = helper_functions.get_topic_ids(link)

        insert_comment_data(topic_ids, cleaned_comments)


def comment_all_post_one_page(data, reverse):
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


def comment_all_post_all_pages(data, reverse):
    for entry in data:

        # Generate all page numbers
        links = scrape_comments.generate_comment_links(entry[1])

        if reverse:
            links = list(reversed(links))

        # Go through all comments in all pages and store them in the database
        for link in links:
            comments = scrape_comments.fetch_comments(link)
            cleaned_comments = clean_comments.clean(comments, entry[2])
            topic_ids = helper_functions.get_topic_ids(link)

            insert_comment_data(topic_ids, cleaned_comments)


def print_insertion_message(ids, len_proof, len_participation):
    print('Inserting %s comments to %s, %s comments to %s, topic_id = %s.%s' % (
        len_proof, constant.DB_PROOF, len_participation, constant.DB_PARTICIPATION, ids[0], ids[1]))


def insert_comment_data(topic_ids, comments_c):

    print_insertion_message(topic_ids, len(comments_c[0]), len(comments_c[1]))

    db_crud_comments.insert_proof_comments(topic_ids[0], topic_ids[1], comments_c[0])
    db_crud_comments.insert_participation_comments(topic_ids[0], topic_ids[1], comments_c[1])
    db_crud_topics.insert_spreadsheet_ids(topic_ids[0], comments_c[3])


def populate_database_comments(check, reverse):
    # Fetch all URLs and IDs of the comments
    data = db_crud_topics.fetch_all_id_url_author()

    # Create database table for comments
    create_table.create_comments_proof_database()
    create_table.create_comments_participation_database()

    match check:
        case "one_one":
            comment_first_post_one_page(data, reverse)
        case "one_all":
            comment_first_post_all_pages(data, reverse)
        case "all_one":
            comment_all_post_one_page(data, reverse)
        case "all_all":
            comment_all_post_all_pages(data, reverse)


"""
================================================================================================

CONTROL OPERATIONS FOR GOOGLE SHEETS DATA RETRIEVAL

================================================================================================
"""


def populate_database_sheets(check):
    data = db_crud_topics.fetch_all_id_sheet_ids()

    create_table.create_google_sheets_database()

    if check == "all":
        create_all_sheet_records(data)
    elif check.isnumeric():
        create_x_sheet_records(data, int(check))


def create_all_sheet_records(data):
    for ids in data:

        sheet_ids = ids[1].replace('{', '').replace('}', '').split(',')

        for sheet_id in sheet_ids:

            sheet_data = scrape_sheets.fetch_sheet_data(sheet_id)

            for sheet in sheet_data:
                cleaned_sheet_data = clean_spreadsheets.clean_sheets_data(sheet[1])

                db_crud_sheets.insert_sheets(sheet_id, ids[0], sheet[0], cleaned_sheet_data)


def create_x_sheet_records(data, number):
    for ids in data:

        sheet_ids = ids[1].replace('{', '').replace('}', '').split(',')

        while number > 0:

            for sheet_id in sheet_ids:

                sheet_data = scrape_sheets.fetch_sheet_data(sheet_id)

                for sheet in sheet_data:
                    cleaned_sheet_data = clean_spreadsheets.clean_sheets_data(sheet[1])

                    db_crud_sheets.insert_sheets(sheet_id, ids[0], sheet[0], cleaned_sheet_data)

            number -= 1