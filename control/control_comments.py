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
CONTROL OPERATIONS FOR THE COMMENT PAGE DATA

    @create_first_database_post_one_page_comment_records_in_database():  populate the database with comments from first page
    @create_first_database_post__all_pages_comment_records_in_database(): populate the database with all comments from one topic
    @create_all_post_first_page_comment_records_in_database(): populate the database with the first page of every topic
    @create_all_post_all_pages_comment_records_in_database(): populate the database with all comments form all posts
    @populate_database_comment_page(): control how many comment pages to insert into the database
        @reverse - start reading comments from the last page
========================================================================================================================
"""


def populate_database(mode, pages_mode, reverse, tables):
    urls, empty_ids, data = [], [], retrieve_data_from_mode(mode)

    for i, entry in enumerate(data):

        ids_error, complete = [], False

        successful_check = crud_topic.read('successful_transfers[topic_successful]', entry[0])

        if successful_check[0][0]:

            urls = retrieve_urls_from_page_mode(entry[1], pages_mode)

            # Check for empty posts in a row (usually happens one website bans the IP address of the scraper)
            if len(urls) == 1 and urls[0].split('=')[-1].split('.')[-1] == '0':
                empty_ids.append(urls[0].split('=')[-1].split('.')[0])
            else:
                empty_ids = []

            # if len(empty_ids) >= 5:
            #     for empty_id in empty_ids:
            #           crud_topic.update('successful_transfers[topic_successful=null]', empty_id)

                print('Aborting due to 5 empty posts in a row: %s' % (empty_ids,))
                break

            # Reverse
            if reverse:
                urls = list(reversed(urls))

            with alive_bar(len(urls), title=('Topic: %s/%s' % (i + 1, len(data)))) as bar:
                for url in urls:

                    comments = scrape_comments.fetch_comments(url)

                    topic_ids = helper_functions.get_topic_ids(url)

                    cleaned_comments = clean_comments.clean(comments, entry[2], tables, topic_ids[0])

                    try:
                        insert_comment_data(topic_ids, cleaned_comments)

                    except Exception as error:
                        print('Error caught: ' + str(error))
                        ids_error.append(
                            [helper_functions.get_topic_ids(url)[0], helper_functions.get_topic_ids(url)[1],
                             str(error)])

                    bar()

            # If error encountered: record the error + (topic and page) id AND delete inserted comments (from that page) from all tables
            if ids_error:
                for id_error in ids_error:
                    crud_comments.create('populate_scrape_errors', [id_error[0], id_error[1], id_error[2]])
                    crud_comments.delete('comments[by_topic_id]', [id_error[0], id_error[1]])
            # If everything dones successfully add it to the database as complete:
            elif not ids_error:
                crud_topic.update('successful_transfers[topic_successful=True]', entry[0])


def update(data):
    for entry in data:

        ids_error, complete = [], []

        urls = scrape_comments.generate_comment_links(entry[1], 'all')

        successful_check = crud_topic.read('successful_transfers[topic_successful]', entry[0])

        if not successful_check[0][0]:

            for url in urls:

                try:
                    comments = scrape_comments.fetch_comments(url)

                    cleaned_comments = clean_comments.clean(comments, entry[2], ['participation', 'author', 'proof'])

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
                except Exception as error:
                    print('Error caught: ' + str(error))
                    ids_error.append(
                        [helper_functions.get_topic_ids(url)[0], helper_functions.get_topic_ids(url)[1], str(error)])

            # If everything done successfully delete the comment_update entry
            if not ids_error:
                crud_comments.delete('comments_update[entry]', entry[0])
            # If error encountered: record the error + (topic and page) id AND delete inserted comments (from that page) from all tables
            elif ids_error:
                for id_error in ids_error:
                    crud_comments.create('populate_scrape_errors', [id_error[0], id_error[1], id_error[2]])
                    crud_comments.delete('comments[by_topic_id]', [id_error[0], id_error[1]])
            elif not ids_error:
                crud_topic.create('successful_transfers[topic_successful=True]', entry[0])


"""
========================================================================================================================
HELPER FUNCTIONS
    @ print_insertion_message() - responsible for printing messages about the amount of comments inserted
    @ insert_comment_data() - inserts cleaned comments data into the database
========================================================================================================================
"""


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


def insert_comment_data(topic_ids, comments_clean):
    proof = comments_clean[0]
    participation = comments_clean[1]
    author = comments_clean[2]
    topic = comments_clean[3]

    print_insertion_message(topic_ids, len(proof), len(participation), len(author))

    try:

        if len(proof) > 0:
            crud_comments.create('populate_proof', [topic_ids[0], topic_ids[1], proof])
        if len(participation) > 0:
            crud_comments.create('populate_participation', [topic_ids[0], topic_ids[1], participation])
        if len(author) > 0:
            crud_comments.create('populate_author', [topic_ids[0], author])
            crud_topic.update('topic[creation_time]', [topic_ids[0], author[0].get_post_time()])
            if topic.get_campaign() is not None:
                crud_topic.create('populate_reward_rules', [topic_ids[0], topic.get_campaign()])

        crud_topic.update('topic[spreadsheet_ids]', [topic_ids[0], topic])

    except Exception as error:
        print(error)


def extract_date(string):
    date = []

    if '-' in string:

        string_temp = string.split(' - ')

        date.append(datetime.strptime(string_temp[0], '%Y/%m/%d'))
        date.append(datetime.strptime(string_temp[1], '%Y/%m/%d'))

    else:
        date.append(datetime.strptime(string, '%Y/%m/%d'))

    return date


def retrieve_data_from_mode(mode):
    data = []

    # MODE OF OPERATION (UPDATE - COMMENTS WHICH HAVE NOT BEEN UPDATED BEFORE) +-+-
    if mode == 'update':
        data = crud_comments.read('comments_update[topic_id]')
        update(data)
        return
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
    # MODE OF OPERATION ([ID, URL, AUTHOR])
    elif type(mode) == type(list()):
        data = mode

    return data


def retrieve_urls_from_page_mode(url, pages_mode):

    if pages_mode.isnumeric():
        urls = scrape_comments.generate_comment_links(url, pages_mode)
    elif pages_mode == 'all':
        urls = scrape_comments.generate_comment_links(url, pages_mode)
    else:
        print('Please select one of the following modes: all, 1, 2, 3, 4, ...')
        return

    return urls
