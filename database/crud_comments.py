from values import constant
from database import connect_to_database
import psycopg2

"""
========================================================================================================================

CRUD OPERATIONS FOR COMMENT SECTION RELATED TABLES

========================================================================================================================
"""


def create(name, data):
    records_to_insert, postgres_insert_query, table_name = [], [], ''

    match name:
        case 'populate_proof':
            topic_id, page_id, proof, table_name = data[0], data[1], data[2], constant.DB_PROOF
            postgres_insert_query = """ INSERT INTO """ + table_name + """(topic_id, page_id, comment_id, forum_username, forum_profile_url, telegram_username, campaigns, post_time, wallet_address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            for comment in proof:
                record = [topic_id, page_id, comment.get_comment_id(), comment.get_forum_username(),
                          comment.get_forum_profile_url(), comment.get_telegram_username(), comment.get_campaigns(),
                          comment.get_post_time(), comment.get_wallet_address()]
                records_to_insert.append(tuple(record))
        case 'populate_participation':
            topic_id, page_id, participation, table_name = data[0], data[1], data[2], constant.DB_PARTICIPATION
            postgres_insert_query = """ INSERT INTO """ + table_name + """(topic_id, page_id, comment_id, forum_username, forum_profile_url, week, social_media_handle, participation, post_time, twitter_links, facebook_links, instagram_links, telegram_links, reddit_links, other_links) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            for comment in participation:
                if comment.get_participation():
                    record = [topic_id, page_id, comment.get_comment_id(), comment.get_forum_username(),
                              comment.get_forum_profile_url(), comment.get_week(), comment.get_social_media_handle(),
                              comment.get_participation(), comment.get_post_time(), comment.get_twitter_links(),
                              comment.get_facebook_links(), comment.get_instagram_links(), comment.get_telegram_links(),
                              comment.get_reddit_links(), comment.get_other_links()]
                    records_to_insert.append(tuple(record))
        case 'populate_author':
            topic_id, author, table_name = data[0], data[1], constant.DB_AUTHOR
            postgres_insert_query = """ INSERT INTO """ + table_name + """(topic_id, comment_id, post_time, raw_data, image_check, image_urls, urls) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            for comment in author:
                record = [topic_id, comment.get_comment_id(), comment.get_post_time(), comment.get_text_data(),
                          comment.get_image_check(), comment.get_image_urls(), comment.get_urls()]
                records_to_insert.append(tuple(record))
        case 'populate_comments_update':
            topic_id, replies_old, author, timestamp, table_name = data[0], data[1], data[2], data[
                3], constant.DB_COMMENTS_UPDATE
            postgres_insert_query = """ INSERT INTO """ + table_name + """(topic_id, url, replies, author, last_update_time) VALUES (%s, %s, %s, %s, %s)"""
            url = constant.TOPIC_PAGE_URL + str(topic_id)
            records_to_insert.append(tuple([topic_id, url, replies_old, author, timestamp]))
        case 'populate_scrape_errors':
            topic_id, page_id, comment_id, error, table_name = data[0], data[1], data[2], data[
                3], constant.DB_COMMENT_SCRAPE_ERRORS

            postgres_insert_query = """ INSERT INTO """ + table_name + """(topic_id, page_id, comment_id, error) VALUES (%s, %s, %s, %s)"""
            records_to_insert.append(tuple([topic_id, page_id, comment_id, error]))

    for record in records_to_insert:

        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()

        try:
            cursor.execute(postgres_insert_query, record)
            connection.commit()
        except (Exception, psycopg2.Error) as error:

            print("Failed to insert record into the table %s:" % table_name, error)

            if name == 'populate_proof' or name == 'populate_participation' or name == 'populate_author':
                if not 'duplicate key value violates unique constraint' in str(error):
                    create('populate_scrape_errors', [record[0], record[1], record[2], str(error)])
        finally:
            if connection:
                cursor.close()
                connection.close()


def read(name, data):
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()
    table_name, postgres_select_query, record_to_insert = '', '', ''

    match name:
        case 'comments_update[topic_id]':
            table_name = constant.DB_COMMENTS_UPDATE
            postgres_select_query = """ SELECT topic_id, url, author, replies FROM """ + table_name
        case 'author[topic_id, comment_id=1, image_urls, raw_text]':
            table_name = constant.DB_AUTHOR
            postgres_select_query = """SELECT topic_id, comment_id, image_urls, raw_data FROM """ + table_name + """ WHERE image_check = True AND comment_id = 1"""
        case 'comments_update[topic_id WHERE topic_id]':
            table_name, topic_id = constant.DB_COMMENTS_UPDATE, data
            postgres_select_query = """SELECT topic_id FROM """ + table_name + """ WHERE topic_id = %s"""
            record_to_insert = (topic_id,)
        case 'comments_scrape_error[topic_id]':
            table_name, topic_id = constant.DB_COMMENT_SCRAPE_ERRORS, data
            postgres_select_query = """SELECT topic_id FROM """ + table_name + """ WHERE topic_id = %s"""
            record_to_insert = (topic_id,)

    try:
        if record_to_insert:
            cursor.execute(postgres_select_query, record_to_insert)
            result = cursor.fetchone()
        else:
            cursor.execute(postgres_select_query, record_to_insert)
            result = cursor.fetchall()

        connection.commit()
        return result
    except (Exception, psycopg2.Error) as error:
        print("Failed to retrieve data from %s: %s" % (table_name, error))
        raise error
    finally:
        if connection:
            cursor.close()
            connection.close()


def delete(name, data):
    table_name, postgres_delete_query, records_to_insert = '', [], []

    match name:
        case 'comments_update[entry]':
            topic_id, table_name = data, constant.DB_COMMENTS_UPDATE
            postgres_delete_query.append("""DELETE FROM """ + table_name + """ WHERE topic_id = %s""")
            records_to_insert.append((topic_id,))
        case 'comments[by_topic_id]':
            topic_id, page_id = data[0], data[1]
            records_to_insert.append(tuple([topic_id, page_id]))
            records_to_insert.append(tuple([topic_id, page_id]))
            records_to_insert.append((topic_id,))
            postgres_delete_query.append(
                """DELETE FROM """ + constant.DB_PROOF + """ WHERE topic_id = %s AND page_id = %s""")
            postgres_delete_query.append(
                """DELETE FROM """ + constant.DB_PARTICIPATION + """ WHERE topic_id = %s AND page_id = %s""")
            postgres_delete_query.append("""DELETE FROM """ + constant.DB_AUTHOR + """ WHERE topic_id = %s""")

    for query, records in zip(postgres_delete_query, records_to_insert):

        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()
        try:
            cursor.execute(query, records)
            connection.commit()
        except (Exception, psycopg2.Error) as error:
            if name == 'comments[by_topic_id]':
                print("Failed to delete an entry from the table %s:" % 'proof/participation/author', error)
            else:
                print("Failed to delete an entry from the table %s:" % table_name, error)
                raise error
        finally:
            if connection:
                cursor.close()
                connection.close()
