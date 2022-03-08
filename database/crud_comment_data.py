import psycopg2
from database import connect_to_database


def insert_entry(post_id, post, table_name):
    try:
        # Connect to the database
        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO """ + table_name + """(post_id, comment_id, forum_username, forum_profile_url, 
        telegram_username, campaigns, post_time) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

        record_to_insert = (post_id, post[0], str(post[1]), str(post[2]), str(post[3]), str(post[4]), str(post[5]))

        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into the table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()