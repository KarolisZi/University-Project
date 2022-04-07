import psycopg2
from database import connect_to_database
from values import constant

"""
========================================================================================================================
CREATE (INSERT) STATEMENTS
    @ insert_entry() - inserts a topic record with the data retrieved from topic page
    @ insert_spreadsheet_ids() - inserts sheet_ids retrieved from author_comments
========================================================================================================================
"""


def insert_entry(topics):
    try:
        # Connect to the database
        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO """ + constant.DB_HOME + """(topic_id, url, original_topic, topic, token_name, author, replies,
         views, last_post_time, last_post_author) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        for topic in topics:
            record_to_insert = (
                topic[0], topic[1], topic[2], topic[3], topic[4], topic[5], topic[6], topic[7], topic[8], topic[9])
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into the table", error)

    finally:

        print("Inserted %s posts into table: %s" % (len(topics), constant.DB_HOME))

        # closing database connection.
        if connection:
            cursor.close()
            connection.close()


def insert_spreadsheet_ids(topic_id, sheet_ids):
    try:
        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()

        postgres_update_query = """UPDATE """ + constant.DB_HOME + """ SET sheet_ids = %s 
                                                                                    WHERE topic_id = %s"""

        cursor.execute(postgres_update_query, (sheet_ids, topic_id))

        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert sheet ids", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()


"""
========================================================================================================================
SELECT STATEMENTS
    @ fetch_all_id_url_author() - retrieves [topic_id, url, author]
    @ fetch_all_id_sheet_ids() - retrieves [topic_id, sheet_ids]
    @ fetch_post_time_replies - retrieves [last_post_time, replies]
========================================================================================================================
"""


def fetch_all_id_url_author():
    try:
        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()

        postgres_select_query = """ SELECT topic_id, url, author FROM """ + constant.DB_HOME

        cursor.execute(postgres_select_query)

        result = cursor.fetchall()

        connection.commit()

        return result

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into the table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()


def fetch_all_id_sheet_ids():
    try:
        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()

        postgres_select_query = """SELECT topic_id, sheet_ids FROM """ + constant.DB_HOME

        cursor.execute(postgres_select_query)

        result = cursor.fetchall()

        connection.commit()

        return result

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into the table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()


def fetch_post_time_replies(topic_id):
    try:
        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()

        postgres_select_query = """SELECT last_post_time, replies FROM """ + constant.DB_HOME + """ WHERE topic_id = %s"""

        cursor.execute(postgres_select_query, (topic_id,))

        result = cursor.fetchone()

        connection.commit()

        return result

    except (Exception, psycopg2.Error) as error:
        print("Failed to retrieve records from the table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()


"""
========================================================================================================================
UPDATE STATEMENTS
    @ fetch_all_id_url_author() - retrieves [topic_id, url, author]
    @ fetch_all_id_sheet_ids() - retrieves [topic_id, sheet_ids]
    @ fetch_post_time_replies - retrieves [last_post_time, replies]
========================================================================================================================
"""


def update_entry(replies, views, last_post_time, last_post_author, topic_id):
    try:
        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()

        postgres_update_query = """UPDATE """ + constant.DB_HOME + """ SET replies = %s, views = %s, last_post_time = %s, last_post_author = %s WHERE topic_id = %s"""

        cursor.execute(postgres_update_query, (replies, views, last_post_time, last_post_author, topic_id))

        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to update replies and last_update_time", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
