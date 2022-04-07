from web_scraping import scrape_topics
from database import db_crud_topics
from database import db_crud_comments
from database import create_table
from values import constant
from information_cleaning import clean_topic
from alive_progress import alive_bar

"""
================================================================================================
CONTROL OPERATIONS FOR THE MAIN PAGE DATA (TOPICS):
    @create_one_page_post_records_in_database(): scrape the first page of the forum
    @create_all_post_records_in_database(): scrape all pages of the forum
    @populate_database_main_page(): create database, choose how many pages to scrape
================================================================================================
"""


def populate_database_main(check):
    if check == 'one':
        create_table.home_page()
        title_one_page()
    elif check == 'all':
        create_table.home_page()
        title_all_pages()
        create_table.home_page()
    elif type(check) == type(list()):
        title_select_pages(check)
    elif check == 'update':
        create_table.comments_update()
        title_update()


# Create records of every post in the given URL that includes [BOUNTY] in the name
def title_one_page():
    results, url = [], constant.FIRST_PAGE_URL

    topics = scrape_topics.fetch_post_data(url)
    for topic in topics:
        cleaned_topic_data = clean_topic.clean_topic_data(topic)
        results.append(cleaned_topic_data)

    db_crud_topics.insert_entry(results)


# Create records of every post that includes [BOUNTY] in the name
def title_all_pages():
    # Generates all forum post pages from the first to last URL
    all_urls = scrape_topics.generate_all_post_page_links()

    with alive_bar(len(all_urls), title='Topics') as bar:
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
            bar()


def title_select_pages(ids):
    all_urls = []

    for id in ids:
        if int(id) % 40 == 0:
            all_urls.append(constant.FIRST_PAGE_URL_NO_PAGE_ID + id)
        else:
            print('There is no page with the id: %s' % id)

    with alive_bar(len(all_urls), title='Topics') as bar:
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
            bar()


def title_update():

    count = 0
    # Generates all forum post pages from the first to last URL
    all_urls = scrape_topics.generate_all_post_page_links()

    # Fetch every post in every page that has "BOUNTY" in the name
    for url in all_urls:

        # Retrieve all topics from a link
        all_topics = scrape_topics.fetch_post_data(url)

        # Clean every topic in a link and insert it into the database
        for topic in all_topics:

            cleaned_topic_data = clean_topic.clean_topic_data(topic)

            time_replies = db_crud_topics.fetch_post_time_replies(cleaned_topic_data[0])

            if time_replies is None:
                db_crud_topics.insert_entry(cleaned_topic_data)
                db_crud_comments.insert_comments_update(cleaned_topic_data[0], 'None', cleaned_topic_data[6], True)
                count = 0
            elif time_replies[0].strftime("%Y-%m-%d %H:%M:%S") != cleaned_topic_data[8]:

                exists_check = db_crud_comments.retrieve_topic_ids_comments_update(cleaned_topic_data[0])

                if exists_check is None:
                    db_crud_comments.insert_comments_update(cleaned_topic_data[0], time_replies[1], cleaned_topic_data[6], False)
                else:
                    db_crud_comments.update_comments_update(cleaned_topic_data[0], cleaned_topic_data[6])

                db_crud_topics.update_entry(cleaned_topic_data[6], cleaned_topic_data[7], cleaned_topic_data[8],cleaned_topic_data[9], cleaned_topic_data[0])
                count = 0
            else:
                count += 1

        if count >= 6:
            break
