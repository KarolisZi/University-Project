import psycopg2
from database import connect_to_database


def create_home_page_database(table_name):
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    try:

        postgres_insert_query = """
        CREATE TABLE """ + table_name + """ (
        id SERIAL PRIMARY KEY,
        url VARCHAR(64) ,
        original_topic VARCHAR(255),
        topic VARCHAR(255),
        author VARCHAR(64),
        replies INTEGER,
        views INTEGER,
        last_post_time VARCHAR(64),
        last_post_author VARCHAR(64)
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


def create_comments_database(table_name):
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    try:

        postgres_insert_query = """
                CREATE TABLE """ + table_name + """ (
                post_id VARCHAR(255),
                comment_id VARCHAR(255),
                forum_username VARCHAR(255),
                forum_profile_url VARCHAR(255),
                telegram_username VARCHAR(255),
                campaigns VARCHAR(255),
                post_time VARCHAR(255)
                );
                """

        cursor.execute(postgres_insert_query)

        connection.commit()

        print("Table " + table_name + " has been created successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Failed to create comment database table", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()