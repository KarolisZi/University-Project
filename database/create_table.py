import psycopg2
from database import connect_to_database
from values import constant


def create_home_page_database():
    table_name = constant.TABLE_NAME_HOME_PAGE
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    try:

        postgres_insert_query = """
        CREATE TABLE """ + table_name + """ (
        topic_id INTEGER,
        url VARCHAR(64),
        original_topic VARCHAR(255),
        topic VARCHAR(255),
        token_name VARCHAR(255),
        author VARCHAR(64),
        replies INTEGER,
        views INTEGER,
        last_post_time VARCHAR(64),
        last_post_author VARCHAR(64),
        sheet_ids TEXT,
        PRIMARY KEY(topic_id)
        );
        """

        cursor.execute(postgres_insert_query)

        connection.commit()

        print("Table " + table_name + " has been created successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Failed to create home page database table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()


def create_comments_proof_database():
    table_name = constant.TABLE_NAME_COMMENT_PAGE_PROOF
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    try:

        postgres_insert_query_1 = """
                CREATE TABLE """ + table_name + """ (
                topic_id INTEGER,
                comment_id VARCHAR(255),
                forum_username VARCHAR(255),
                forum_profile_url VARCHAR(255),
                telegram_username VARCHAR(255),
                campaigns VARCHAR(255),
                post_time VARCHAR(255),
                PRIMARY KEY (topic_id, comment_id)
                );
                """

        postgres_insert_query_2 = """
        ALTER TABLE """ + table_name + """ 
        ADD CONSTRAINT fk_""" + constant.TABLE_NAME_HOME_PAGE + """Table
        FOREIGN KEY (topic_id) 
        REFERENCES """ + constant.TABLE_NAME_HOME_PAGE + """ (topic_id)
        """

        cursor.execute(postgres_insert_query_1)
        cursor.execute(postgres_insert_query_2)

        connection.commit()

        print("Table " + table_name + " has been created successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Failed to create comment database table", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()


def create_comments_participation_database():
    table_name = constant.TABLE_NAME_COMMENT_PAGE_PARTICIPATION
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    try:

        postgres_insert_query_1 = """
                CREATE TABLE """ + table_name + """ (
                topic_id INTEGER,
                comment_id VARCHAR(255),
                forum_username VARCHAR(255),
                forum_profile_url VARCHAR(255),
                week VARCHAR(255),
                social_media_profile_url VARCHAR(255),
                social_media_links TEXT,
                participation TEXT,
                post_time VARCHAR(255),
                PRIMARY KEY (topic_id, comment_id)
                );
                """

        postgres_insert_query_2 = """
        ALTER TABLE """ + table_name + """ 
        ADD CONSTRAINT fk_""" + constant.TABLE_NAME_HOME_PAGE + """Table
        FOREIGN KEY (topic_id) 
        REFERENCES """ + constant.TABLE_NAME_HOME_PAGE + """ (topic_id)
        """

        cursor.execute(postgres_insert_query_1)
        cursor.execute(postgres_insert_query_2)

        connection.commit()

        print("Table " + table_name + " has been created successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Failed to create comment database table", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()


def create_google_sheets_database():
    table_name = constant.TABLE_NAME_GOOGLE_SHEETS
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    try:

        postgres_insert_query_1 = """
                CREATE TABLE """ + table_name + """ (
                row VARCHAR(255),
                sheet_id VARCHAR(255),
                topic_id INTEGER,
                sheet_name VARCHAR(255),
                timestamp VARCHAR(255),
                forum_username VARCHAR(255),
                profile_link VARCHAR(255),
                social_media_username VARCHAR(255),
                followers VARCHAR(255),
                PRIMARY KEY (row, sheet_id, topic_id, sheet_name)
                );
                """

        postgres_insert_query_2 = """
        ALTER TABLE """ + table_name + """
        ADD CONSTRAINT fk_""" + constant.TABLE_NAME_HOME_PAGE + """Table
        FOREIGN KEY (topic_id)
        REFERENCES """ + constant.TABLE_NAME_HOME_PAGE + """ (topic_id)
        """

        cursor.execute(postgres_insert_query_1)
        cursor.execute(postgres_insert_query_2)

        connection.commit()

        print("Table " + table_name + " has been created successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Failed to create comment database table", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
