import psycopg2
from database import connect_to_database
from values import constant


def insert_proof_comments(sheet_id, topic_id, sheet_name, data):
    try:
        # Connect to the database
        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO """ + constant.TABLE_NAME_GOOGLE_SHEETS + """(row, sheet_id, topic_id, sheet_name, timestamp, forum_username, profile_link, social_media_username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

        for row in data:
            record_to_insert = (row[0], sheet_id, topic_id, sheet_name, row[1], row[2], row[3], row[4])
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into the table", error)

    finally:

        print("Inserted %s rows into table: %s" % (len(data), constant.TABLE_NAME_GOOGLE_SHEETS ))

        # closing database connection.
        if connection:
            cursor.close()
            connection.close()