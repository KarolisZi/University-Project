from values import constant
from database import connect_to_database
import psycopg2

"""
========================================================================================================================

CRUD OPERATION RELATED TO TOPIC (THREAD) DATA

========================================================================================================================
"""


def create(name, data):
    no_error, records_to_insert, postgres_insert_query, table_name = True, [], '', ''

    match name:
        case 'populate_topic':
            table_name, topics = constant.DB_TOPIC, data
            postgres_insert_query = """ INSERT INTO """ + table_name + """(topic_id, url, original_topic, topic, author, replies, views, last_post_time, last_post_author) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            for topic in topics:
                record = [
                    topic.get_topic_id(), topic.get_url(), topic.get_original_topic(), topic.get_topic(),
                    topic.get_author(), topic.get_replies(), topic.get_views(), topic.get_last_post_time(),
                    topic.get_last_post_author()]
                records_to_insert.append(tuple(record))
        case 'populate_reward_rules':
            table_name, topic_id, campaign_info = constant.DB_TOPIC_REWARD_RULES, data[0], data[1]
            postgres_insert_query = """ INSERT INTO """ + table_name + """(topic_id, campaign, reward, rules) VALUES (%s, %s, %s, %s)"""
            if campaign_info is not None:
                for campaign in campaign_info:
                    records_to_insert.append(tuple([topic_id, campaign[0], campaign[1], campaign[2]]))
        case 'populate_successful_transfers':
            table_name, topics = constant.DB_SUCCESSFUL_TRANSFERS, data
            postgres_insert_query = """ INSERT INTO """ + table_name + """(topic_id) VALUES (%s)"""
            for topic in topics:
                records_to_insert.append((topic.get_topic_id(),))

    for record in records_to_insert:
        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()
        try:
            cursor.execute(postgres_insert_query, record)
            connection.commit()
        except (Exception, psycopg2.Error) as error:
            print("Failed to create record in the table %s:" % table_name, error)
            no_error = False
        finally:
            if connection:
                cursor.close()
                connection.close()

    if no_error:
        print("Successfully inserted %s record(s) to %s" % (len(records_to_insert), table_name))


def read(name, data):
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    table_name, fetch_all = '', True
    postgres_select_query, record_to_insert = '', ''
    result = []

    match name:
        case 'topic[topic_id, url, author]':
            table_name = constant.DB_TOPIC
            postgres_select_query = """ SELECT topic_id, url, author FROM """ + table_name
            match data:
                case 'one':
                    fetch_all = False
                case ' all':
                    fetch_all = True
        case 'topic[url, author]':
            table_name, topic_id = constant.DB_TOPIC, data
            postgres_select_query = """ SELECT url, author FROM """ + table_name + """ WHERE topic_id = %s"""
            record_to_insert = (topic_id,)
            fetch_all = False
        case 'topic[topic_id, url, author] by date':
            table_name, date = constant.DB_TOPIC, data
            if len(date) == 1:
                postgres_select_query = """ SELECT topic_id, url, author FROM """ + table_name + """ WHERE last_post_time > %s"""
                record_to_insert = (date[0],)
            elif len(date) == 2:
                postgres_select_query = """ SELECT topic_id, url, author FROM """ + table_name + """ WHERE last_post_time > %s AND last_post_time < %s"""
                record_to_insert = (date[0], date[1])
        case 'topic[topic_id, sheet_ids]':
            table_name = constant.DB_TOPIC
            postgres_select_query = """SELECT topic_id, sheet_ids FROM """ + table_name
        case 'topic[last_post_time, replies]':
            table_name, topic_id = constant.DB_TOPIC, data
            postgres_select_query = """SELECT last_post_time, replies FROM """ + table_name + """ WHERE topic_id = %s"""
            record_to_insert = (topic_id,)
            fetch_all = False
        case 'successful_transfers[topic_successful]':
            topic_id, table_name = data, constant.DB_SUCCESSFUL_TRANSFERS
            postgres_select_query = """SELECT topic_successful FROM """ + table_name + """ WHERE topic_id = %s"""
            record_to_insert = (topic_id,)
        case 'successful_transfers[images_successful]':
            topic_id, table_name = data, constant.DB_SUCCESSFUL_TRANSFERS
            postgres_select_query = """SELECT images_successful FROM """ + table_name + """ WHERE topic_id = %s"""
            record_to_insert = (topic_id,)
        case 'successful_transfers[sheet_successful]':
            topic_id, table_name = data, constant.DB_SUCCESSFUL_TRANSFERS
            postgres_select_query = """SELECT sheet_successful FROM """ + table_name + """ WHERE topic_id = %s"""
            record_to_insert = (topic_id,)
        case 'topic[author]':
            topic_id, table_name = data, constant.DB_TOPIC
            postgres_select_query = """SELECT author FROM """ + table_name + """ WHERE topic_id = %s"""
            record_to_insert = (topic_id,)

    try:
        if not record_to_insert:
            cursor.execute(postgres_select_query)
        elif record_to_insert:
            cursor.execute(postgres_select_query, record_to_insert)
        if fetch_all:
            result = cursor.fetchall()
        elif not fetch_all:
            result = cursor.fetchone()
        connection.commit()

        return result
    except (Exception, psycopg2.Error) as error:
        print("Failed to read records from table %s:" % table_name, error)
        raise error
    finally:
        if connection:
            cursor.close()
            connection.close()


def update(name, data):
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    table_name, postgres_update_query, record_to_insert = '', '', ''

    match name:
        case 'topic[full]':
            replies, views, last_post_time, last_post_author, topic_id, table_name = data[0], data[1], data[2], data[3], \
                                                                                     data[4], constant.DB_TOPIC
            postgres_update_query = """UPDATE """ + table_name + """ SET replies = %s, views = %s, last_post_time = %s, last_post_author = %s WHERE topic_id = %s"""
            record_to_insert = replies, views, last_post_time, last_post_author, topic_id
        case 'topic[spreadsheet_ids]':
            topic_id, topic, table_name = data[0], data[1], constant.DB_TOPIC
            postgres_update_query = """UPDATE """ + table_name + """ SET sheet_ids = %s WHERE topic_id = %s"""
            record_to_insert = topic.get_sheet_ids(), topic_id
        case 'topic[author]':
            topic_id, topic, table_name = data[0], data[1], constant.DB_TOPIC
            postgres_update_query = """UPDATE """ + table_name + """ SET token_name = %s, reward_pool = %s, reward_allocation = %s WHERE topic_id = %s"""
            record_to_insert = (topic.get_token_name(), topic.get_reward_pool(), topic.get_reward_allocation(), topic_id)
        case 'topic[creation_time]':
            topic_id, creation_time, table_name = data[0], data[1], constant.DB_TOPIC
            postgres_update_query = """UPDATE """ + table_name + """ SET creation_time = %s WHERE topic_id = %s"""
            record_to_insert = (creation_time, topic_id)
        case 'successful_transfers[topic_successful=False]':
            topic_id, table_name = data, constant.DB_SUCCESSFUL_TRANSFERS
            postgres_update_query = """UPDATE """ + table_name + """ SET topic_successful = False WHERE topic_id = %s"""
            record_to_insert = (topic_id, )
        case 'successful_transfers[topic_successful=null]':
            topic_id, table_name = data, constant.DB_SUCCESSFUL_TRANSFERS
            postgres_update_query = """UPDATE """ + table_name + """ SET topic_successful = null WHERE topic_id = %s"""
            record_to_insert = (topic_id,)
        case 'successful_transfers[topic_successful=True]':
            table_name, topic_id = constant.DB_SUCCESSFUL_TRANSFERS, data
            postgres_update_query = """UPDATE """ + table_name + """ SET topic_successful = True WHERE topic_id = %s"""
            record_to_insert = (topic_id, )
        case 'successful_transfers[images_successful=True]':
            table_name, topic_id = constant.DB_SUCCESSFUL_TRANSFERS, data
            postgres_update_query = """UPDATE """ + table_name + """ SET images_successful = True WHERE topic_id = %s"""
            record_to_insert = (topic_id,)
        case 'successful_transfers[images_successful=False]':
            table_name, topic_id = constant.DB_SUCCESSFUL_TRANSFERS, data
            postgres_update_query = """UPDATE """ + table_name + """ SET images_successful = False WHERE topic_id = %s"""
            record_to_insert = (topic_id,)

    try:

        cursor.execute(postgres_update_query, record_to_insert)
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to update records in the table %s:" % table_name, error)
        raise error
    finally:
        if connection:
            cursor.close()
            connection.close()
