from web_scraping import scrape_comments
from information_cleaning import clean_comments
from information_cleaning import helper_functions
from alive_progress import alive_bar
from database import crud_comments
from database import crud_topic
from values import constant
from datetime import datetime

"""
========================================================================================================================

CONTROL OPERATIONS FOR EXTRACTING COMMENT SECTION DATA

========================================================================================================================
"""


# Retrieve, clean, store comments in the database
def populate_database(mode, pages_mode, reverse, tables):
    urls, empty_ids, data = [], [], retrieve_data_from_mode(mode)

    for i, entry in enumerate(data):

        successful_check = crud_topic.read('successful_transfers[topic_successful]', entry[0])

        if successful_check[0][0] is None:

            urls = retrieve_urls_from_page_mode(entry[1], pages_mode)

            # Reverse
            if reverse:
                urls = list(reversed(urls))

            with alive_bar(len(urls), title=('Topic: %s/%s' % (i + 1, len(data)))) as bar:
                for url in urls:
                    comments = scrape_comments.fetch_comments(url)

                    topic_ids = helper_functions.get_topic_ids(url)

                    cleaned_comments = clean_comments.clean(comments, entry[2], tables, topic_ids[0])

                    insert_comment_data(topic_ids, cleaned_comments)

                    bar()

        no_error_check = crud_comments.read('comments_scrape_error[topic_id]', entry[0])

        if not no_error_check:
            crud_topic.update('successful_transfers[topic_successful=True]', entry[0])
        elif no_error_check:
            crud_topic.update('successful_transfers[topic_successful=False]', entry[0])


# Retrieve, clean, store comments from topic_update table
def update(data):
    for entry in data:

        urls = scrape_comments.generate_comment_links(entry[1], 'all')

        with alive_bar(len(urls), title='Comment update') as bar:
            for url in urls:

                comments = scrape_comments.fetch_comments(url)

                cleaned_comments = clean_comments.clean(comments, entry[2], ['participation', 'author', 'proof'],
                                                        entry[0])

                proof = cleaned_comments[0]
                participation = cleaned_comments[1]
                author = cleaned_comments[2]

                topic_ids = helper_functions.get_topic_ids(url)

                for proof_comment in proof:
                    if int(proof_comment.get_comment_id()) > entry[3] + 1:
                        del proof_comment
                for participation_comment in participation:
                    if int(participation_comment.get_comment_id()) > entry[3] + 1:
                        del participation_comment
                for author_comment in author:
                    if int(author_comment.get_comment_id()) > entry[3] + 1:
                        del author_comment

                insert_comment_data(topic_ids, [proof, participation, author, cleaned_comments[3]])
                bar()

            no_error_check = crud_comments.read('comments_scrape_error[topic_id]', entry[0])

            if not no_error_check:
                crud_topic.update('successful_transfers[topic_successful=True]', entry[0])
                crud_comments.delete('comments_update[entry]', entry[0])
            elif no_error_check:
                crud_topic.update('successful_transfers[topic_successful=False]', entry[0])


"""
========================================================================================================================

HELPER FUNCTIONS

========================================================================================================================
"""


# Print messages about the number of comments being stored each itteration
def print_insertion_message(ids, len_proof, len_participation, len_author):
    print_check = False
    string = 'Inserting '

    if len_proof > 0:
        string += ('%s comments to %s, ' % (len_proof, constant.DB_PROOF))
        print_check = True
    if len_participation > 0:
        string += ('%s comments to %s, ' % (len_participation, constant.DB_PARTICIPATION))
        print_check = True
    if len_author > 0:
        string += ('%s comments to %s, ' % (len_author, constant.DB_AUTHOR))
        print_check = True

    string += ('topic_id = %s.%s' % (ids[0], ids[1]))

    if print_check:
        print(string)


# Insert retrieved data into appropriate database tables
def insert_comment_data(topic_ids, comments_clean):
    proof, participation, author, topic, no_errors = comments_clean[0], comments_clean[1], comments_clean[2], \
                                                     comments_clean[3], True

    print_insertion_message(topic_ids, len(proof), len(participation), len(author))

    if len(proof) > 0:
        crud_comments.create('populate_proof', [topic_ids[0], topic_ids[1], proof])
    if len(participation) > 0:
        crud_comments.create('populate_participation', [topic_ids[0], topic_ids[1], participation])
    if len(author) > 0:
        crud_comments.create('populate_author', [topic_ids[0], author])
        crud_topic.update('topic[creation_time]', [topic_ids[0], author[0].get_post_time()])
        if topic.get_campaign() is not None:
            try:
                crud_topic.create('populate_reward_rules', [topic_ids[0], topic.get_campaign()])
            except Exception as error:
                print(error)
                no_errors = False

            if no_errors:
                crud_topic.update('successful_transfers[images_successful=True]', topic_ids[0])
            else:
                crud_topic.update('successful_transfers[images_successful=False]', topic_ids[0])

    crud_topic.update('topic[spreadsheet_ids]', [topic_ids[0], topic])


# If the program run with the date mode, extract the date from the string
def extract_date(string):
    date = []

    if '-' in string:

        string_temp = string.split(' - ')

        date.append(datetime.strptime(string_temp[0], '%Y/%m/%d'))
        date.append(datetime.strptime(string_temp[1], '%Y/%m/%d'))

    else:
        date.append(datetime.strptime(string, '%Y/%m/%d'))

    return date


# Retrieve appropriate data based on the program running mode
def retrieve_data_from_mode(mode):
    data = []

    # MODE OF OPERATION (UPDATE - COMMENTS WHICH HAVE NOT BEEN UPDATED BEFORE)
    if mode == 'update':
        data = crud_comments.read('comments_update[topic_id]', [])
        update(data)
        return []
    # MODE OF OPERATION (DATE OR DATE RANGE)
    elif '/' in mode:
        date = extract_date(mode)
        data = crud_topic.read('topic[topic_id, url, author] by date', date)
    # MODE OF OPERATION (ALL)
    elif mode == 'all':
        data = crud_topic.read('topic[topic_id, url, author]', 'all')
    # MODE OF OPERATION (ONE)
    elif mode == 'one':
        data = crud_topic.read('topic[topic_id, url, author]', 'one')
        data = [data]
    # MODE OF OPERATION (CUSTOM ID)
    elif type(mode) == type(list()):
        data = []
        for entry in mode:
            url = 'https://bitcointalk.org/index.php?topic=%s' % entry
            author = crud_topic.read('topic[author]', entry)
            if author:
                data.append([entry, url, author[0][0]])
            else:
                print('The entry with topic id %s, does nto exist in topic database' % entry)
    return data


# Select how many pages of comments to retrieve
def retrieve_urls_from_page_mode(url, pages_mode):
    if pages_mode.isnumeric():
        urls = scrape_comments.generate_comment_links(url, pages_mode)
    elif pages_mode == 'all':
        urls = scrape_comments.generate_comment_links(url, pages_mode)
    else:
        print('Please select one of the following modes: all, 1, 2, 3, 4, ...')
        return

    return urls
