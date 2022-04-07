import psycopg2
from database import connect_to_database
from values import constant

"""
========================================================================================================================
ANALYSIS FUNCTIONS
========================================================================================================================
"""


def retrieve_username_frequency(table_name):
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    try:

        postgres_select_query = """ SELECT forum_username, count(*) as c FROM """ + table_name + """ GROUP BY forum_username"""

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


def retrieve_campaign_frequency():
    table_name = constant.DB_PROOF
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    try:

        postgres_select_query = """ SELECT campaigns FROM """ + table_name

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
