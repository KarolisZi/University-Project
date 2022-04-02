import psycopg2
from database import connect_to_database
from values import constant


def create_home_page_database():
    table_name = constant.DB_HOME
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    try:

        postgres_insert_query = """
        CREATE TABLE """ + table_name + """ (
        topic_id INTEGER,
        url VARCHAR(50),
        original_topic VARCHAR(80),
        topic VARCHAR(80),
        token_name VARCHAR(50),
        author VARCHAR(25),
        replies INTEGER,
        views INTEGER,
        last_post_time TIMESTAMP,
        last_post_author VARCHAR(25),
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
    table_name = constant.DB_PROOF
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    try:

        postgres_insert_query_1 = """
                CREATE TABLE """ + table_name + """ (
                topic_id INTEGER,
                page_id INTEGER,
                comment_id INTEGER,
                forum_username VARCHAR(25),
                forum_profile_url VARCHAR(60),
                telegram_username VARCHAR(33),
                campaigns VARCHAR(150),
                post_time TIMESTAMP,
                PRIMARY KEY (topic_id, comment_id)
                );
                """

        postgres_insert_query_2 = """
        ALTER TABLE """ + table_name + """ 
        ADD CONSTRAINT fk_""" + constant.DB_HOME + """Table
        FOREIGN KEY (topic_id) 
        REFERENCES """ + constant.DB_HOME + """ (topic_id)
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
    table_name = constant.DB_PARTICIPATION
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    try:

        postgres_insert_query_1 = """
                CREATE TABLE """ + table_name + """ (
                topic_id INTEGER,
                page_id INTEGER,
                comment_id INTEGER,
                forum_username VARCHAR(25),
                forum_profile_url VARCHAR(60),
                week VARCHAR(150),
                social_media_profile_url VARCHAR(255),
                social_media_links TEXT,
                participation TEXT,
                post_time TIMESTAMP,
                PRIMARY KEY (topic_id, comment_id)
                );
                """

        postgres_insert_query_2 = """
        ALTER TABLE """ + table_name + """ 
        ADD CONSTRAINT fk_""" + constant.DB_HOME + """Table
        FOREIGN KEY (topic_id) 
        REFERENCES """ + constant.DB_HOME + """ (topic_id)
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
    table_name = constant.DB_SHEETS
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    try:

        postgres_insert_query_1 = """
                CREATE TABLE """ + table_name + """ (
                row INTEGER,
                sheet_id INTEGER,
                topic_id INTEGER,
                sheet_name VARCHAR(100),
                timestamp TIMESTAMP,
                forum_username VARCHAR(25),
                profile_link VARCHAR(60),
                social_media_username VARCHAR(100),
                followers VARCHAR(100),
                PRIMARY KEY (row, sheet_id, topic_id, sheet_name)
                );
                """

        postgres_insert_query_2 = """
        ALTER TABLE """ + table_name + """
        ADD CONSTRAINT fk_""" + constant.DB_HOME + """Table
        FOREIGN KEY (topic_id)
        REFERENCES """ + constant.DB_HOME + """ (topic_id)
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
