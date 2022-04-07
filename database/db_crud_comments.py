import psycopg2
from database import connect_to_database
from values import constant

"""
========================================================================================================================
CREATE (INSERT) STATEMENTS
    @ insert_proof_comments() - inserts PROOF comments into the database table
    @ insert_participation_comments() - inserts PARTICIPATION comments into the database table
    @ insert_author_comments() - inserts AUTHOR comments into the database table 
    @ insert_comments_update() - inserts topic_id which have to run comment updates
========================================================================================================================
"""


def insert_proof_comments(topic_id, page_id, comments):
    try:
        # Connect to the database
        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO """ + constant.DB_PROOF + """(topic_id, page_id, comment_id, forum_username, forum_profile_url, 
        telegram_username, campaigns, post_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

        for comment in comments:
            record_to_insert = (
                topic_id, page_id, comment[0], str(comment[1]), str(comment[2]), str(comment[3]), str(comment[4]),
                str(comment[5]))
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into the table", error)

    finally:

        print("%s: Success!" % constant.DB_PROOF)

        # closing database connection.
        if connection:
            cursor.close()
            connection.close()


def insert_participation_comments(topic_id, page_id, comments):
    try:
        # Connect to the database
        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO """ + constant.DB_PARTICIPATION + """(topic_id, page_id, comment_id, forum_username, forum_profile_url, 
        week, social_media_profile_url, social_media_links, participation, post_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        for comment in comments:
            record_to_insert = (
                topic_id, page_id, comment[0], str(comment[1]), str(comment[2]), str(comment[3]), str(comment[4]),
                str(comment[5]),
                str(comment[6]), str(comment[7]))
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into the table", error)

    finally:

        print("%s: Success!" % constant.DB_PARTICIPATION)

        # closing database connection.
        if connection:
            cursor.close()
            connection.close()


def insert_author_comments(topic_id, data):
    try:
        # Connect to the database
        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()

        for entry in data:

            postgres_insert_query = ''
            record_to_insert = ''

            if entry[2]:
                postgres_insert_query = """ INSERT INTO """ + constant.DB_AUTHOR + """(topic_id, comment_id, text_data, image_check, image_urls) VALUES (%s, %s, %s, %s, %s)"""
                record_to_insert = (topic_id, entry[3], entry[0].text, True, entry[1])
            elif not entry[2]:
                postgres_insert_query = """ INSERT INTO """ + constant.DB_AUTHOR + """(topic_id, comment_id, text_data, image_check) VALUES (%s, %s, %s, %s)"""
                record_to_insert = (topic_id, entry[3], entry[0].text, False)

            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into the table: ", error)

    finally:

        print("%s: Success!" % constant.DB_AUTHOR)

        # closing database connection.
        if connection:
            cursor.close()
            connection.close()


def insert_comments_update(topic_id, replies_old, replies_new, new_post):
    try:
        # Connect to the database
        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO """ + constant.DB_COMMENTS_UPDATE + """(topic_id, replies_old, replies_new, new_post) VALUES (%s, %s, %s, %s)"""

        record_to_insert = (topic_id, replies_old, replies_new, new_post)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into the table", error)

    finally:

        print("%s: Success!" % constant.DB_PROOF)

        # closing database connection.
        if connection:
            cursor.close()
            connection.close()


"""
========================================================================================================================
READ (SELECT) STATEMENTS
    @ retrieve_topic_ids_comments_update() - retrieve a topic_id to check if an entry already exists in the database
    @ fetch_all_id_image_urls() - retrieve [topic_id, image_urls, image_check]
========================================================================================================================
"""


def retrieve_topic_ids_comments_update(topic_id):
    table_name = constant.DB_COMMENTS_UPDATE
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    try:

        postgres_select_query = """ SELECT topic_id FROM """ + table_name

        cursor.execute(postgres_select_query, (topic_id,))

        result = cursor.fetchone()

        connection.commit()

        return result

    except (Exception, psycopg2.Error) as error:
        print("Failed to retrieve data from %s: %s" % (table_name, error))

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()


def fetch_all_id_image_urls():
    try:
        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()

        postgres_select_query = """SELECT topic_id, image_urls, image_check FROM """ + constant.DB_AUTHOR

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


"""
========================================================================================================================
UPDATE STATEMENTS
    @ insert_image_text() - inserts image data into the database as text
    @ update_comments_update() - update comment updates which have not been executed yet
========================================================================================================================
"""


def insert_image_text(topic_id, image_data):

    try:
        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()

        postgres_update_query = """UPDATE """ + constant.DB_AUTHOR + """ SET image_data = %s 
                                                                                    WHERE topic_id = %s"""

        records_to_insert = (image_data, topic_id)

        cursor.execute(postgres_update_query, records_to_insert)

        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert image text: ", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()


def update_comments_update(topic_id, replies_new):
    try:
        # Connect to the database
        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()

        postgres_update_query = """UPDATE """ + constant.DB_COMMENTS_UPDATE + """ SET replies_new = %s WHERE topic_id = %s"""

        record_to_insert = (replies_new, topic_id)
        cursor.execute(postgres_update_query, record_to_insert)
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into the table", error)

    finally:

        print("%s: Success!" % constant.DB_COMMENTS_UPDATE)

        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
