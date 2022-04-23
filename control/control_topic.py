from web_scraping import scrape_topics
from database import crud_comments
from database import crud_topic
from values import constant
from information_cleaning import clean_topic
from alive_progress import alive_bar
from datetime import datetime

"""
================================================================================================
CONTROL OPERATIONS FOR THE MAIN PAGE DATA (TOPICS):
    @create_one_page_post_records_in_database(): scrape the first page of the forum
    @create_all_post_records_in_database(): scrape all pages of the forum
    @populate_database_main_page(): create database, choose how many pages to scrape
================================================================================================
"""


def populate_database(mode):

    all_urls, date, date_count_check = [], [], 0

    # ONE PAGE
    if mode == 'one':
        all_urls = [constant.FIRST_PAGE_URL]
    # ALL PAGES
    elif mode == 'all':
        all_urls = scrape_topics.generate_all_post_page_links()
    # UPDATE MODE (BASED ON 'LAST REPLY TIME')
    elif mode == 'update':
        update()
        return
    # DATE OR DATE RANGE MODE
    elif '/' in mode:
        date = extract_date(mode)
        all_urls = scrape_topics.generate_all_post_page_links()
    # CUSTOM IDS MODE
    elif type(mode) == type(list()):
        all_urls = generate_urls_from_custom_id(mode)

    with alive_bar(len(all_urls), title='Topics') as bar:

        for url in all_urls:
            results = []

            # Retrieve all topics from a link
            all_topics = scrape_topics.fetch_post_data(url)

            # Clean every topic in a link and insert it into the database
            for topic in all_topics:

                cleaned_topic = clean_topic.clean_topic_data(topic, 'full')

                if not date:
                    results.append(cleaned_topic)
                else:
                    time = datetime.strptime(cleaned_topic.get_last_post_time(), '%Y-%m-%d %H:%M:%S')
                    if len(date) == 1:
                        if time >= date[0]:
                            results.append(cleaned_topic)
                            date_count_check = 0
                        else:
                            date_count_check += 1
                    elif len(date) == 2:
                        if date[0] <= time <= date[1]:
                            results.append(cleaned_topic)
                            date_count_check = 0
                        else:
                            date_count_check += 1

                if date_count_check >= 5:
                    print('All topics in the provided date range have been inserted')
                    return

            crud_topic.create('populate_topic', results)
            crud_topic.create('populate_successful_transfers', results)

            bar()


# GO THROUGH TOPICS AND UPDATE THOSE WHICH LAST_POST_TIME IN THE DATABASE DIFFERS FROM THE ONE ON THE WEBSITE
# BASED ON LAST STORED VALUE OF REPLIES, ALSO DEDUCE HOW MANY COMMENTS HAVE TO BE UPDATED AS WELL
def update():
    count = 0
    # IDEA: GET URLS BY DATE
    # Generates all forum post pages from the first to last URL
    all_urls = scrape_topics.generate_all_post_page_links()

    # Fetch every post in every page that has "BOUNTY" in the name
    for url in all_urls:

        # Retrieve all topics from a link
        all_topics = scrape_topics.fetch_post_data(url)

        for topic in all_topics:

            # Clean the data and prepare for Database storage
            topic_object = clean_topic.clean_topic_data(topic, 'updates')

            # Retrieves [last_post_time, replies] for provided topic_id
            time_replies = crud_topic.read('topic[last_post_time, replies]', topic_object.get_topic_id())
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Check if an entry exists in the topic (new topic updates)
            if time_replies is None:
                # Insert topic and a reminder for comment updates
                crud_topic.create('populate_successful_transfers', [topic_object])
                crud_topic.create('populate_topic', [topic_object])
                crud_comments.create('populate_comments_update',
                                     [topic_object.get_topic_id(), 0, topic_object.get_author(), now])
                count = 0

            # Compare two datetime objects (database, website)
            elif time_replies[0] != datetime.strptime(topic_object.get_last_post_time(), '%Y-%m-%d %H:%M:%S'):

                # Retrieve all topic_id from comment_updates
                comment_update = crud_comments.read('comments_update[topic_id]')

                if topic_object.get_topic_id() in comment_update:
                    crud_comments.create('populate_comments_update',
                                         [topic_object.get_topic_id(), time_replies[1], topic_object.get_author(), now])
                    crud_topic.update('successful_transfers[topic_successful=False]', topic_object.get_topic_id())

                # If the last_post_time has changed, update topic information
                crud_topic.update('topic[full]', [topic_object.get_replies(), topic_object.get_views(),
                                                  topic_object.get_last_post_time(),
                                                  topic_object.get_last_post_author(), topic_object.get_topic_id()])
                count = 0
            else:
                count += 1

            # If 6 topics have the same time in a row, terminate the program and conclude that all necessary updates have been completed
            if count >= 6:
                break


def extract_date(string):
    date = []

    if '-' in string:

        date.append(datetime.strptime(string.split(' - ')[0], '%Y/%m/%d'))
        date.append(datetime.strptime(string.split(' - ')[1], '%Y/%m/%d'))

    else:
        date.append(datetime.strptime(string, '%Y/%m/%d'))

    return date


def generate_urls_from_custom_id(ids):
    results = []

    for id in ids:
        if int(id) % 40 == 0:
            results.append(constant.FIRST_PAGE_URL_NO_PAGE_ID + str(id))
        else:
            print('There is no page with the id: %s' % id)

    return results
