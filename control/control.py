from web_scraping import scrape_forum_topics
from web_scraping import scrape_forum_post_comments
from database import crud_topic_data
from database import crud_comment_data
from database import create_table
from database import crud_sheets_data
from values import constant
from information_cleaning import infromation_cleaning_topic
from information_cleaning import infromation_cleaning_comments
from information_cleaning import information_cleaning_sheets
from web_scraping import scrape_google_spreadsheet

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
    topics = scrape_forum_topics.fetch_post_from_url(constant.FIRST_PAGE_URL)

    results = []

    for topic in topics:
        cleaned_topic_data = infromation_cleaning_topic.clean_topic_data(topic)
        results.append(cleaned_topic_data)

    crud_topic_data.insert_entry(results)


# Create records of every post that includes [BOUNTY] in the name
def create_all_post_records_in_database():
    # Generates all forum post pages from the first to last URL
    links = scrape_forum_topics.generate_all_post_page_links()

    # Fetch every post in every page that has "BOUNTY" in the name
    for link in links:

        results = []

        # Retrieve all topics from a link
        topics = scrape_forum_topics.fetch_post_from_url(link)

        # Clean every topic in a link and insert it into the database
        for topic in topics:
            cleaned_topic_data = infromation_cleaning_topic.clean_topic_data(topic)
            results.append(cleaned_topic_data)

        crud_topic_data.insert_entry(results)


def populate_database_main_page(check):
    # Create database table
    create_table.create_home_page_database()

    # if check True populate the database with the given page
    # if check False populate the database with all pages
    match check:
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


def create_first_database_post_one_page_comment_records_in_database(data, reverse):
    if reverse:
        page_id = scrape_forum_post_comments.fetch_last_comment_page_id(data[0][1])
        links = scrape_forum_post_comments.generate_all_comment_page_links(page_id)
        comments = scrape_forum_post_comments.fetch_comments_from_url(links[-1])
        cleaned_comments = infromation_cleaning_comments.filter_comment_section_data(comments, data[0][2])

    else:
        comments = scrape_forum_post_comments.fetch_comments_from_url(data[0][1])
        cleaned_comments = infromation_cleaning_comments.filter_comment_section_data(comments, data[0][2])

    crud_comment_data.insert_proof_comments(data[0][0], cleaned_comments[0])
    crud_comment_data.insert_participation_comments(data[0][0], cleaned_comments[1])
    # Insert spreadsheet ids
    crud_topic_data.insert_spreadsheet_ids(data[0][0], cleaned_comments[2])


def create_first_database_post__all_pages_comment_records_in_database(data, reverse):
    # Get the number of the last comment page
    page_id = scrape_forum_post_comments.fetch_last_comment_page_id(data[0][1])

    # Generate all page numbers
    links = scrape_forum_post_comments.generate_all_comment_page_links(page_id)

    if reverse:
        links = list(reversed(links))

    # Go through all comments in all pages and store them in the database
    for link in links:
        comments = scrape_forum_post_comments.fetch_comments_from_url(link)
        cleaned_comments = infromation_cleaning_comments.filter_comment_section_data(comments, data[0][2])

        crud_comment_data.insert_proof_comments(data[0][0], cleaned_comments[0])
        crud_comment_data.insert_participation_comments(data[0][0], cleaned_comments[1])
        crud_topic_data.insert_spreadsheet_ids(data[0][0], cleaned_comments[2])


def create_all_post_first_page_comment_records_in_database(data, reverse):
    for entry in data:

        if reverse:
            page_id = scrape_forum_post_comments.fetch_last_comment_page_id(entry[1])
            links = scrape_forum_post_comments.generate_all_comment_page_links(page_id)
            comments = scrape_forum_post_comments.fetch_comments_from_url(links[-1])
            cleaned_comments = infromation_cleaning_comments.filter_comment_section_data(comments, entry[2])
        else:
            comments = scrape_forum_post_comments.fetch_comments_from_url(entry[1])
            cleaned_comments = infromation_cleaning_comments.filter_comment_section_data(comments, entry[2])

        crud_comment_data.insert_proof_comments(entry[0], cleaned_comments[0])
        crud_comment_data.insert_participation_comments(entry[0], cleaned_comments[1])
        crud_topic_data.insert_spreadsheet_ids(entry[0], cleaned_comments[2])


def create_all_post_all_pages_comment_records_in_database(data, reverse):
    for entry in data:
        # Get the number of the last comment page
        page_id = scrape_forum_post_comments.fetch_last_comment_page_id(entry[1])

        # Generate all page numbers
        links = scrape_forum_post_comments.generate_all_comment_page_links(page_id)

        if reverse:
            links = list(reversed(links))

        # Go through all comments in all pages and store them in the database
        for link in links:
            comments = scrape_forum_post_comments.fetch_comments_from_url(link)
            cleaned_comments = infromation_cleaning_comments.filter_comment_section_data(comments, entry[2])

            crud_comment_data.insert_proof_comments(entry[0], cleaned_comments[0])
            crud_comment_data.insert_participation_comments(entry[0], cleaned_comments[1])
            crud_topic_data.insert_spreadsheet_ids(entry[0], cleaned_comments[2])


def populate_database_comment_page(check, reverse):
    # Fetch all URLs and IDs of the comments
    data = crud_topic_data.fetch_all_id_url_author()

    # Create database table for comments
    create_table.create_comments_proof_database()
    create_table.create_comments_participation_database()

    match check:
        case "one_one":
            create_first_database_post_one_page_comment_records_in_database(data, reverse)
        case "one_all":
            create_first_database_post__all_pages_comment_records_in_database(data, reverse)
        case "all_one":
            create_all_post_first_page_comment_records_in_database(data, reverse)
        case "all_all":
            create_all_post_all_pages_comment_records_in_database(data, reverse)


"""
================================================================================================

CONTROL OPERATIONS FOR GOOGLE SHEETS DATA RETRIEVAL

================================================================================================
"""


def populate_database_sheets(check):
    data = crud_topic_data.fetch_all_id_sheet_ids()

    create_table.create_google_sheets_database()

    if check == "all":
        create_all_sheet_records(data)
    elif check.isnumeric():
        create_x_sheet_records(data, int(check))


def create_all_sheet_records(data):
    for ids in data:

        sheet_ids = ids[1].replace('{', '').replace('}', '').split(',')

        for sheet_id in sheet_ids:

            sheet_data = scrape_google_spreadsheet.fetch_sheet_data(sheet_id)

            for sheet in sheet_data:

                cleaned_sheet_data = information_cleaning_sheets.clean_sheets_data(sheet[1])

                crud_sheets_data.insert_proof_comments(sheet_id, ids[0], sheet[0], cleaned_sheet_data)


def create_x_sheet_records(data, number):

    for ids in data:

        sheet_ids = ids[1].replace('{', '').replace('}', '').split(',')

        if number > 0:

            for sheet_id in sheet_ids:

                sheet_data = scrape_google_spreadsheet.fetch_sheet_data(sheet_id)

                for sheet in sheet_data:

                    cleaned_sheet_data = information_cleaning_sheets.clean_sheets_data(sheet[1])

                    crud_sheets_data.insert_proof_comments(sheet_id, ids[0], sheet[0], cleaned_sheet_data)

            number -= 1

        else:

            break
