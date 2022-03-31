import psycopg2
from database import connect_to_database
from values import constant


def insert_proof_comments(topic_id, comments):
    try:
        # Connect to the database
        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO """ + constant.TABLE_NAME_COMMENT_PAGE_PROOF + """(topic_id, comment_id, forum_username, forum_profile_url, 
        telegram_username, campaigns, post_time) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

        for comment in comments:
            record_to_insert = (topic_id, comment[0], str(comment[1]), str(comment[2]), str(comment[3]), str(comment[4]), str(comment[5]))
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into the table", error)

    finally:

        print("Inserted %s comments into table: %s" % (len(comments), constant.TABLE_NAME_COMMENT_PAGE_PROOF ))

        # closing database connection.
        if connection:
            cursor.close()
            connection.close()


def insert_participation_comments(topic_id, comments):
    try:
        # Connect to the database
        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO """ + constant.TABLE_NAME_COMMENT_PAGE_PARTICIPATION + """(topic_id, comment_id, forum_username, forum_profile_url, 
        week, social_media_profile_url, social_media_links, participation, post_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        for comment in comments:
            record_to_insert = (topic_id, comment[0], str(comment[1]), str(comment[2]), str(comment[3]), str(comment[4]), str(comment[5]), str(comment[6]), str(comment[7]))
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into the table", error)

    finally:

        print("Inserted %s comments into table: %s" % (len(comments), constant.TABLE_NAME_COMMENT_PAGE_PARTICIPATION))

        # closing database connection.
        if connection:
            cursor.close()
            connection.close()

def retrieve_participation_proof_comments_username_recurrance(table_name):
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    try:

        postgres_insert_query = """ SELECT forum_username, count(*) as c FROM """ + table_name + """ GROUP BY forum_username"""

        cursor.execute(postgres_insert_query)

        result = cursor.fetchall()

        connection.commit()

        return result

    except (Exception, psycopg2.Error) as error:
        print("Failed to retrieve data from %s: %s" % (table_name, error))

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()