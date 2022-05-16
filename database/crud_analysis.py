import psycopg2
from database import connect_to_database
from values import constant

"""
========================================================================================================================

DATA RETRIEVAL FOR DATA ANALYSIS

========================================================================================================================
"""


def read(name, data):
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    postgres_select_query, table_name = '', ''

    match name:
        case 'proof/participation[username_frequency]':
            table_name, mode = data[0], data[1]
            if mode == 'asc':
                postgres_select_query = """ SELECT forum_username, count(*) as c FROM """ + table_name + """ GROUP BY forum_username ORDER BY c ASC"""
            elif mode == 'desc':
                postgres_select_query = """ SELECT forum_username, count(*) as c FROM """ + table_name + """ GROUP BY forum_username ORDER BY c DESC"""
        case 'proof[campaigns]':
            table_name = constant.DB_PROOF
            postgres_select_query = """ SELECT campaigns FROM """ + table_name
        case 'topic[author_frequency]':
            table_name, mode = constant.DB_TOPIC, data
            if mode == 'asc':
                postgres_select_query = """ SELECT author, count(*) as c FROM """ + table_name + """ GROUP BY author ORDER BY c ASC"""
            elif mode == 'desc':
                postgres_select_query = """ SELECT author, count(*) as c FROM """ + table_name + """ GROUP BY author ORDER BY c DESC"""
        case 'participation[twitter_links]':
            table_name = constant.DB_PARTICIPATION
            postgres_select_query = """ SELECT topic_id, comment_id, twitter_links FROM """ + table_name + """ WHERE twitter_links != '{}'"""
        case 'topic[creation_time]':
            table_name = constant.DB_TOPIC
            postgres_select_query = """ SELECT creation_time FROM """ + table_name + """ ORDER BY creation_time """
        case 'topic[last_post_time]':
            table_name = constant.DB_TOPIC
            postgres_select_query = """ SELECT last_post_time FROM """ + table_name + """ ORDER BY last_post_time """
        case 'proof/participation[count]':
            if data == 'proof':
                table_name = constant.DB_PROOF
            elif data == 'participation':
                table_name = constant.DB_PARTICIPATION
            postgres_select_query = """SELECT topic_id, count(*) as c FROM """ + table_name + """ GROUP BY topic_id ORDER BY c DESC"""
        case 'topic[last_post,creation]':
            table_name = constant.DB_TOPIC
            postgres_select_query = """SELECT last_post_time, creation_time FROM """ + table_name
        case 'participation[participation]':
            table_name = constant.DB_PARTICIPATION
            postgres_select_query = """SELECT participation FROM """ + table_name + """ WHERE participation IS NOT NULL"""
        case 'participation[links]':
            table_name, platform = constant.DB_PARTICIPATION, data
            postgres_select_query = """SELECT """ + platform + """_links FROM """ + table_name + """ WHERE cardinality(""" + platform + """_links) > 0"""
        case 'google_sheets[sheet_name]':
            table_name = constant.DB_SHEETS
            postgres_select_query = """SELECT sheet_name, count(*) as c FROM """ + table_name + """ GROUP BY sheet_name ORDER BY c DESC """
        case '[twitter_user[created_at]':
            table_name = constant.DB_TWITTER_USER
            postgres_select_query = """SELECT created_at FROM """ + table_name + """ ORDER BY created_at DESC """
        case '[twitter_user[tweet_count]':
            table_name = constant.DB_TWITTER_USER
            postgres_select_query = """SELECT tweet_count FROM """ + table_name + """ ORDER BY tweet_count DESC """
        case '[twitter_user[followers, following, real, fake]':
            table_name = constant.DB_TWITTER_USER
            postgres_select_query = """SELECT followers, following, real_followers, fake_followers FROM """ + table_name
        case 'twitter_tweet[text]':
            table_name = constant.DB_TWITTER_TWEET
            postgres_select_query = """SELECT text FROM """ + table_name
        case 'twitter_tweet[reply_count, retweet_count, like_count]':
            table_name = constant.DB_TWITTER_TWEET
            postgres_select_query = """SELECT reply_count, retweet_count, like_count FROM """ + table_name
        case 'topic[reward_allocation]':
            table_name = constant.DB_TOPIC
            postgres_select_query = """SELECT reward_allocation FROM """ + table_name + """ WHERE reward_allocation IS NOT NULL AND reward_allocation <> '{}'"""

    try:
        cursor.execute(postgres_select_query)
        result = cursor.fetchall()
        connection.commit()
        return result
    except (Exception, psycopg2.Error) as error:
        print("Failed to retrieve data from %s: %s" % (table_name, error))
        raise error

    finally:
        if connection:
            cursor.close()
            connection.close()
