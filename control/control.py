from web_scraping import scrape_forum_home_page
from web_scraping import scrape_forum_post_comments
from database import crud_home_page_data
from database import crud_comment_data
from database import create_table
from values import constant

"""
================================================================================================
CONTROL OPERATIONS FOR THE MAIN PAGE DATA (TOPICS):
    @create_one_page_post_records_in_database(): scrape the first page of the forum
    @create_all_post_records_in_database(): scrape all pages of the forum
    @populate_database_main_page(): create database, choose how many pages to scrape
================================================================================================
"""


# Create records of every post in the given URL that includes [BOUNTY] in the name
def create_one_page_post_records_in_database(url):

    topics = scrape_forum_home_page.fetch_post_from_url(url)

    crud_home_page_data.insert_entry(topics)


# Create records of every post that includes [BOUNTY] in the name
def create_all_post_records_in_database(database_table_name, url):
    # Generates all forum post pages from the first to last URL
    links = scrape_forum_home_page.generate_all_post_page_links(
        scrape_forum_home_page.fetch_last_post_page_id(url))

    # Fetch every post in every page that has "BOUNTY" in the name
    for link in links:

        topics = scrape_forum_home_page.fetch_post_from_url(link)

        crud_home_page_data.insert_entry(topics)


def populate_database_main_page(check):
    # Create database table
    create_table.create_home_page_database()

    # if check True populate the database with the given page
    # if check False populate the database with all pages
    match check:
        case "one":

            create_one_page_post_records_in_database(constant.FIRST_PAGE_URL)
        case "all":
            create_all_post_records_in_database(constant.FIRST_PAGE_URL)


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
        comments = scrape_forum_post_comments.fetch_comments_from_url(links[-1], data[0][2])
    else:
        comments = scrape_forum_post_comments.fetch_comments_from_url(data[0][1], data[0][2])

    crud_comment_data.insert_proof_comments(data[0][0], comments[0])
    crud_comment_data.insert_participation_comments(data[0][0], comments[1])


def create_first_database_post__all_pages_comment_records_in_database(data, reverse):
    # Get the number of the last comment page
    page_id = scrape_forum_post_comments.fetch_last_comment_page_id(data[0][1])

    # Generate all page numbers
    links = scrape_forum_post_comments.generate_all_comment_page_links(page_id)

    if reverse:
        links = list(reversed(links))

    # Go through all comments in all pages and store them in the database
    for link in links:
        comments = scrape_forum_post_comments.fetch_comments_from_url(link, data[0][2])

        crud_comment_data.insert_proof_comments(data[0][0], comments[0])
        crud_comment_data.insert_participation_comments(data[0][0], comments[1])


def create_all_post_first_page_comment_records_in_database(data, reverse):
    for entry in data:

        if reverse:
            page_id = scrape_forum_post_comments.fetch_last_comment_page_id(entry[1])
            links = scrape_forum_post_comments.generate_all_comment_page_links(page_id)
            comments = scrape_forum_post_comments.fetch_comments_from_url(links[-1], entry[2])
        else:
            comments = scrape_forum_post_comments.fetch_comments_from_url(entry[1], entry[2])

        crud_comment_data.insert_proof_comments(entry[0], comments[0])
        crud_comment_data.insert_participation_comments(data[0][0], comments[1])


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
            comments = scrape_forum_post_comments.fetch_comments_from_url(link, entry[2])

            crud_comment_data.insert_proof_comments(entry[0], comments[0])
            crud_comment_data.insert_participation_comments(data[0][0], comments[1])


def populate_database_comment_page(check, reverse):

    # Fetch all URLs and IDs of the comments
    data = crud_home_page_data.fetch_all_id_url_author(constant.TABLE_NAME_HOME_PAGE)

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
