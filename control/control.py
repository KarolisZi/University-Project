from web_scraping import scrape_forum_home_page
from web_scraping import scrape_forum_post_comments
from database import crud_home_page_data
from database import crud_comment_data
from database import create_table
from values import constant

"""
================================================================================================
CONTROL OPERATIONS FOR THE MAIN PAGE DATA
================================================================================================
"""


# Create records of every post in the given URL that includes [BOUNTY] in the name
def create_one_page_post_records_in_database(database_table_name, url):
    posts_per_page = scrape_forum_home_page.fetch_post_from_url(url)

    for post in posts_per_page:
        crud_home_page_data.insert_entry(post, database_table_name)

    print("Inserting %s posts into table: %s" % (len(posts_per_page), database_table_name))


# Create records of every post that includes [BOUNTY] in the name
def create_all_post_records_in_database(database_table_name, url):
    # Generates all forum post pages from the first to last URL
    links = scrape_forum_home_page.generate_all_post_page_links(
        scrape_forum_home_page.fetch_last_post_page_id(url))

    # Fetch every post in every page that has "BOUNTY" in the name
    for link in links:

        posts_per_page = scrape_forum_home_page.fetch_post_from_url(link)

        for post in posts_per_page:
            crud_home_page_data.insert_entry(post, database_table_name)

        print("Inserting %s posts into table: %s" % (len(posts_per_page), database_table_name))


def populate_database_main_page(check):
    # Create database table
    create_table.create_home_page_database()

    # if check True populate the database with the given page
    # if check False populate the database with all pages
    match check:
        case "one":

            create_one_page_post_records_in_database(constant.TABLE_NAME_HOME_PAGE, constant.FIRST_PAGE_URL)
        case "all":
            create_all_post_records_in_database(constant.TABLE_NAME_HOME_PAGE, constant.FIRST_PAGE_URL)


"""
================================================================================================
CONTROL OPERATIONS FOR THE COMMENT PAGE DATA
================================================================================================
"""


def create_one_post_one_page_comment_records_in_database(data, database_table_name):

    comments = scrape_forum_post_comments.fetch_comments_from_url(data[0][1])

    for comment in comments:
        crud_comment_data.insert_entry(data[0][0], comment, database_table_name)

    print("Inserting %s comments into table: %s" % (len(comments), database_table_name))


def create_one_post__all_pages_comment_records_in_database(data, database_table_name):

    # Get the number of the last comment page
    page_id = scrape_forum_post_comments.fetch_last_comment_page_id(data[0][1])

    # Generate all page numbers
    links = scrape_forum_post_comments.generate_all_comment_page_links(page_id)

    # Go through all comments in all pages and store them in the database

    for link in links:

        comments = scrape_forum_post_comments.fetch_comments_from_url(link)

        for comment in comments:
            crud_comment_data.insert_entry(data[0][0], comment, database_table_name)

        print("Inserting %s comments into table: %s" % (len(comments), database_table_name))


def create_all_post_all_pages_comment_records_in_database(data, database_table_name):

    for entry in data:
        # Get the number of the last comment page
        page_id = scrape_forum_post_comments.fetch_last_comment_page_id(entry[1])

        # Generate all page numbers
        links = scrape_forum_post_comments.generate_all_comment_page_links(page_id)

        # Go through all comments in all pages and store them in the database
        for link in links:

            comments = scrape_forum_post_comments.fetch_comments_from_url(link)

            for comment in comments:
                crud_comment_data.insert_entry(entry[0], comment, database_table_name)

            print("Inserting %s comments into table: %s" % (len(comments), database_table_name))


def populate_database_comment_page(check):
    """

    :rtype: object
    """
    # Fetch all URLs and IDs of the comments
    data = crud_home_page_data.fetch_all_id_url(constant.TABLE_NAME_HOME_PAGE)

    # Create database table for comments
    create_table.create_comments_database()

    match check:
        case "one_one":
            create_one_post_one_page_comment_records_in_database(data, constant.TABLE_NAME_COMMENT_PAGE)
        case "one_all":
            create_one_post__all_pages_comment_records_in_database(data, constant.TABLE_NAME_COMMENT_PAGE)
        case "all_all":
            create_all_post_all_pages_comment_records_in_database(data, constant.TABLE_NAME_COMMENT_PAGE)