from values import constant
from database import connect_to_database
import psycopg2

"""
========================================================================================================================

CRUD OPERATION RELATED TO TWITTER DATA

========================================================================================================================
"""


def create(name, data):
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    record_to_insert, postgres_insert_query, table_name = '', '', ''

    match name:
        case 'populate_twitter_tweet':
            table_name, topic_id, comment_id, tweet = constant.DB_TWITTER_TWEET, data[0], data[1], data[2]
            postgres_insert_query = """ INSERT INTO """ + table_name + """(topic_id, comment_id, tweet_id, author_id, text, retweet, created_at, retweet_count, reply_count, like_count, quote_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            record_to_insert = (
                topic_id, comment_id, tweet.get_tweet_id(), tweet.get_author_id(), tweet.get_text(),
                tweet.get_retweet(), tweet.get_created_at(),
                tweet.get_retweet_count(), tweet.get_reply_count(), tweet.get_like_count(),
                tweet.get_quote_count())

        case 'populate_twitter_user':
            table_name, user = constant.DB_TWITTER_USER, data
            postgres_insert_query = """ INSERT INTO """ + table_name + """(author_id, name, username, created_at, followers, following, tweet_count, listed_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            record_to_insert = (
                user.get_author_id(), user.get_name(), user.get_username(), user.get_created_at(), user.get_followers(),
                user.get_following(), user.get_tweet_count(), user.get_listed_count())

    try:

        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Failed to create record in the table %s:" % table_name, error)
        raise error
    finally:
        if connection:
            cursor.close()
            connection.close()


def read(name, data):
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    table_name, postgres_select_query, record_to_insert = '', '', ''

    match name:
        case 'twitter_tweet[tweet_id]':
            table_name, topic_id = constant.DB_TWITTER_TWEET, data
            postgres_select_query = """ SELECT tweet_id FROM """ + table_name + """ WHERE tweet_id = %s"""
            record_to_insert = (topic_id,)
        case 'twitter_user[author_id]':
            table_name, author_id = constant.DB_TWITTER_USER, data
            postgres_select_query = """ SELECT author_id FROM """ + table_name + """ WHERE author_id = %s"""
            record_to_insert = (str(author_id),)
        case 'twitter_user[username]':
            table_name = constant.DB_TWITTER_USER
            postgres_select_query = """ SELECT author_id, username FROM """ + table_name
        case 'twitter_user[real,fake]':
            table_name, author_id = constant.DB_TWITTER_USER, data
            postgres_select_query = """ SELECT real_followers, fake_followers FROM """ + table_name + """ WHERE author_id = %s"""
            record_to_insert = (str(author_id),)

    try:
        cursor.execute(postgres_select_query, record_to_insert)
        result = cursor.fetchall()

    except (Exception, psycopg2.Error) as error:
        print("Failed to read records from table %s:" % table_name, error)
        raise error
    finally:

        if connection:
            cursor.close()
            connection.close()

    return result


def update(name, data):
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    table_name, postgres_update_query, record_to_insert = '', '', ''

    match name:
        case 'twitter_user[real, fake]':
            table_name, author_id, real_followers, fake_followers = constant.DB_TWITTER_USER, data[0], data[1], data[2]
            postgres_update_query = """ UPDATE """ + table_name + """ SET real_followers = %s, fake_followers = %s WHERE author_id = %s"""
            record_to_insert = (real_followers, fake_followers, author_id)

    try:

        cursor.execute(postgres_update_query, record_to_insert)
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to update records in the table %s:" % table_name, error)
        raise error
    finally:
        if connection:
            cursor.close()
            connection.close()
