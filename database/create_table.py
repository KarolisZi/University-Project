import psycopg2
from database import connect_to_database
from values import constant

"""
========================================================================================================================

DATABASE TABLE CREATION

========================================================================================================================
"""


def home_page():
    table_name = constant.DB_TOPIC
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    try:

        postgres_insert_query = """
        CREATE TABLE """ + table_name + """ (
        topic_id INTEGER,
        url VARCHAR(50),
        original_topic VARCHAR(100),
        topic VARCHAR(100),
        author VARCHAR(25),
        replies INTEGER,
        views INTEGER,
        last_post_time TIMESTAMP,
        last_post_author VARCHAR(25),
        creation_time TIMESTAMP,
        token_name VARCHAR(250),
        reward_pool TEXT,
        reward_allocation TEXT,
        sheet_ids TEXT [],
        PRIMARY KEY(topic_id)
        );
        """

        postgres_alter_query_2 = """ALTER TABLE """ + table_name + """ SET SCHEMA """ + constant.SCHEMA

        cursor.execute(postgres_insert_query)
        cursor.execute(postgres_alter_query_2)

        connection.commit()

        print("Table " + table_name + " has been created successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Failed to create " + table_name + " table:", error)

    finally:
        if connection:
            cursor.close()
            connection.close()


def topic_reward_rules():
    table_name = constant.DB_TOPIC_REWARD_RULES
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    try:

        postgres_insert_query = """
        CREATE TABLE """ + table_name + """ (
        topic_id INTEGER,
        campaign TEXT,
        reward TEXT[],
        rules TEXT[],
        PRIMARY KEY(topic_id, campaign)
        );
        """

        postgres_alter_query_2 = """ALTER TABLE """ + table_name + """ SET SCHEMA """ + constant.SCHEMA

        cursor.execute(postgres_insert_query)
        cursor.execute(postgres_alter_query_2)

        connection.commit()

        print("Table " + table_name + " has been created successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Failed to create " + table_name + " table:", error)

    finally:
        if connection:
            cursor.close()
            connection.close()


def comments_proof():
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
                wallet_address VARCHAR(120),
                PRIMARY KEY (topic_id, comment_id)
                );
                """

        postgres_alter_query_2 = """ALTER TABLE """ + table_name + """ ADD CONSTRAINT fk_""" + constant.DB_TOPIC + """Table
        FOREIGN KEY (topic_id) REFERENCES """ + constant.DB_TOPIC + """ (topic_id)"""

        postgres_alter_query_3 = """ALTER TABLE """ + table_name + """ SET SCHEMA """ + constant.SCHEMA

        cursor.execute(postgres_insert_query_1)
        cursor.execute(postgres_alter_query_2)
        cursor.execute(postgres_alter_query_3)

        connection.commit()

        print("Table " + table_name + " has been created successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Failed to create " + table_name + " table:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


def comments_participation():
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
                week TEXT,
                social_media_handle TEXT[],
                participation TEXT,
                post_time TIMESTAMP,
                twitter_links TEXT[],
                facebook_links TEXT[],
                instagram_links TEXT[],
                telegram_links TEXT[],
                reddit_links TEXT[],
                other_links TEXT[],
                PRIMARY KEY (topic_id, comment_id)
                );
                """

        postgres_alter_query_2 = """ALTER TABLE """ + table_name + """ ADD CONSTRAINT fk_""" + constant.DB_TOPIC + """Table
        FOREIGN KEY (topic_id) REFERENCES """ + constant.DB_TOPIC + """ (topic_id)"""

        postgres_alter_query_3 = """ALTER TABLE """ + table_name + """ SET SCHEMA """ + constant.SCHEMA

        cursor.execute(postgres_insert_query_1)
        cursor.execute(postgres_alter_query_2)
        cursor.execute(postgres_alter_query_3)

        connection.commit()

        print("Table " + table_name + " has been created successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Failed to create " + table_name + " table:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


def google_sheets():
    table_name = constant.DB_SHEETS
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    try:

        postgres_insert_query_1 = """
                CREATE TABLE """ + table_name + """ (
                row INTEGER,
                sheet_id VARCHAR(50),
                topic_id INTEGER,
                sheet_name VARCHAR(200),
                timestamp VARCHAR(200),
                forum_username VARCHAR(25),
                profile_link VARCHAR(200),
                social_media_username VARCHAR(200),
                followers VARCHAR(200),
                telegram_username VARCHAR(33),
                PRIMARY KEY (row, sheet_id, topic_id, sheet_name)
                );
                """

        postgres_alter_query_2 = """ALTER TABLE """ + table_name + """ ADD CONSTRAINT fk_""" + constant.DB_TOPIC + """Table
        FOREIGN KEY (topic_id) REFERENCES """ + constant.DB_TOPIC + """ (topic_id) """

        postgres_alter_query_3 = """ALTER TABLE """ + table_name + """ SET SCHEMA """ + constant.SCHEMA

        cursor.execute(postgres_insert_query_1)
        cursor.execute(postgres_alter_query_2)
        cursor.execute(postgres_alter_query_3)

        connection.commit()

        print("Table " + table_name + " has been created successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Failed to create " + table_name + " table:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


def comments_author():
    table_name = constant.DB_AUTHOR
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    try:

        postgres_insert_query_1 = """
                CREATE TABLE """ + table_name + """ (
                topic_id INTEGER,
                comment_id INTEGER,
                post_time TIMESTAMP,
                image_check BOOLEAN,
                image_urls TEXT [],
                urls TEXT [],
                raw_data TEXT,
                PRIMARY KEY (topic_id, comment_id, image_check)
                );
                """

        postgres_alter_query_2 = """ALTER TABLE """ + table_name + """ ADD CONSTRAINT fk_""" + constant.DB_TOPIC + """Table
        FOREIGN KEY (topic_id) REFERENCES """ + constant.DB_TOPIC + """ (topic_id) """

        postgres_alter_query_3 = """ALTER TABLE """ + table_name + """ SET SCHEMA """ + constant.SCHEMA

        cursor.execute(postgres_insert_query_1)
        cursor.execute(postgres_alter_query_2)
        cursor.execute(postgres_alter_query_3)

        connection.commit()

        print("Table " + table_name + " has been created successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Failed to create " + table_name + " table:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


def comments_update():
    table_name = constant.DB_COMMENTS_UPDATE
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    try:

        postgres_insert_query_1 = """
                CREATE TABLE """ + table_name + """ (
                topic_id INTEGER,
                url VARCHAR(50),
                replies INTEGER,
                author VARCHAR(25),
                last_update_time TIMESTAMP,
                PRIMARY KEY (topic_id)
                );
                """

        postgres_alter_query_2 = """ALTER TABLE """ + table_name + """ SET SCHEMA """ + constant.SCHEMA

        cursor.execute(postgres_insert_query_1)
        cursor.execute(postgres_alter_query_2)

        connection.commit()

        print("Table " + table_name + " has been created successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Failed to create " + table_name + " table:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


def comment_scrape_errors():
    table_name = constant.DB_COMMENT_SCRAPE_ERRORS
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    try:

        postgres_insert_query_1 = """
                CREATE TABLE """ + table_name + """ (
                topic_id INTEGER,
                page_id INTEGER,
                comment_id INTEGER,
                error VARCHAR(150),
                PRIMARY KEY (topic_id, page_id, comment_id)
                );
                """

        postgres_alter_query_2 = """ALTER TABLE """ + table_name + """ SET SCHEMA """ + constant.SCHEMA

        cursor.execute(postgres_insert_query_1)
        cursor.execute(postgres_alter_query_2)

        connection.commit()

        print("Table " + table_name + " has been created successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Failed to create " + table_name + " table:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


def successful_transfers():
    table_name = constant.DB_SUCCESSFUL_TRANSFERS
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    try:

        postgres_insert_query_1 = """
                CREATE TABLE """ + table_name + """ (
                topic_id INTEGER,
                topic_successful BOOLEAN,
                images_successful BOOLEAN,
                sheet_successful BOOLEAN,
                PRIMARY KEY (topic_id)
                );
                """

        postgres_alter_query_2 = """ALTER TABLE """ + table_name + """ SET SCHEMA """ + constant.SCHEMA

        cursor.execute(postgres_insert_query_1)
        cursor.execute(postgres_alter_query_2)

        connection.commit()

        print("Table " + table_name + " has been created successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Failed to create " + table_name + " table:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


def twitter_tweet():
    table_name = constant.DB_TWITTER_TWEET
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    try:
        postgres_insert_query_1 = """
                    CREATE TABLE """ + table_name + """ (
                    topic_id INTEGER,
                    comment_id INTEGER,
                    tweet_id TEXT,
                    author_id TEXT,
                    text TEXT,
                    retweet BOOLEAN,
                    created_at TIMESTAMP,
                    retweet_count INTEGER,
                    reply_count INTEGER,
                    like_count INTEGER,
                    quote_count INTEGER,
                    PRIMARY KEY (topic_id, comment_id, tweet_id)
                    );
                    """

        postgres_alter_query_2 = """ALTER TABLE """ + table_name + """ SET SCHEMA """ + constant.SCHEMA

        cursor.execute(postgres_insert_query_1)
        cursor.execute(postgres_alter_query_2)

        connection.commit()

        print("Table " + table_name + " has been created successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Failed to create " + table_name + " table:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


def twitter_user():
    table_name = constant.DB_TWITTER_USER
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    try:
        postgres_insert_query_1 = """
                        CREATE TABLE """ + table_name + """ (
                        author_id TEXT,
                        name TEXT,
                        username TEXT,
                        created_at TIMESTAMP,
                        followers INTEGER,
                        following INTEGER,
                        tweet_count INTEGER,
                        listed_count INTEGER,
                        real_followers INTEGER,
                        fake_followers INTEGER,
                        PRIMARY KEY (author_id)
                        );
                        """

        postgres_alter_query_2 = """ALTER TABLE """ + table_name + """ SET SCHEMA """ + constant.SCHEMA

        cursor.execute(postgres_insert_query_1)
        cursor.execute(postgres_alter_query_2)

        connection.commit()

        print("Table " + table_name + " has been created successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Failed to create " + table_name + " table:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

# Create all database tables
def create_all_tables():
    home_page()
    comments_participation()
    comments_proof()
    comments_author()
    topic_reward_rules()
    comment_scrape_errors()
    successful_transfers()
    comments_update()
    google_sheets()
    twitter_tweet()
    twitter_user()
