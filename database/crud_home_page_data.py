import psycopg2
from database import connect_to_database


def insert_entry(comment, table_name):
    try:
        # Connect to the database
        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO """ + table_name + """(topic_id, url, original_topic, topic, author, replies,
         views, last_post_time, last_post_author) VALUES (%s,%s,%s, %s, %s, %s, %s, %s, %s)"""

        record_to_insert = (comment[0], comment[1], comment[2], comment[3], comment[4], comment[5], comment[6], comment[7], comment[8])

        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into the table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()


def fetch_all_id_url_author(table_name):
    try:
        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()

        postgres_insert_query = """ SELECT topic_id, url, author from """ + table_name

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