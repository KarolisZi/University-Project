import psycopg2
from database import connect_to_database
from values import constant


def insert_entry(topics):
    try:
        # Connect to the database
        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO """ + constant.TABLE_NAME_HOME_PAGE + """(topic_id, url, original_topic, topic, author, replies,
         views, last_post_time, last_post_author) VALUES (%s,%s,%s, %s, %s, %s, %s, %s, %s)"""

        for topic in topics:
            record_to_insert = (
                topic[0], topic[1], topic[2], topic[3], topic[4], topic[5], topic[6], topic[7], topic[8])
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into the table", error)

    finally:

        print("Inserted %s posts into table: %s" % (len(topics), constant.TABLE_NAME_HOME_PAGE))

        # closing database connection.
        if connection:
            cursor.close()
            connection.close()


def insert_spreadsheet_ids(topic_id, sheet_ids):
    try:
        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()

        postgres_insert_query = """UPDATE """ + constant.TABLE_NAME_HOME_PAGE + """ SET sheet_ids = %s 
                                                                                    WHERE topic_id = %s"""

        cursor.execute(postgres_insert_query, (sheet_ids, topic_id))

        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert sheet ids", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()


def fetch_all_id_url_author():
    try:
        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()

        postgres_insert_query = """ SELECT topic_id, url, author FROM """ + constant.TABLE_NAME_HOME_PAGE

        cursor.execute(postgres_insert_query)

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

        postgres_insert_query = """SELECT topic_id, sheet_ids FROM """ + constant.TABLE_NAME_HOME_PAGE

        cursor.execute(postgres_insert_query)

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
