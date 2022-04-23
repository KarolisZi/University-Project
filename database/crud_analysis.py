import psycopg2
from database import connect_to_database
from values import constant


def read(name, data):
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    postgres_select_query, table_name = '', ''

    match name:
        case 'proof/participation[username_frequency]':
            table_name = data
            postgres_select_query = """ SELECT forum_username, count(*) as c FROM """ + table_name + """ GROUP BY forum_username"""
        case 'proof[campaigns]':
            table_name = constant.DB_PROOF
            postgres_select_query = """ SELECT campaigns FROM """ + table_name
        case 'topic[author_frequency]':
            table_name = constant.DB_TOPIC
            postgres_select_query = """ SELECT author, count(*) as c FROM """ + table_name + """ GROUP BY author"""
        case 'participation[twitter_links]':
            table_name = constant.DB_PARTICIPATION
            postgres_select_query = """ SELECT topic_id, twitter_links FROM """ + table_name + """ WHERE twitter_links != '{}'"""

    try:
        cursor.execute(postgres_select_query)
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
