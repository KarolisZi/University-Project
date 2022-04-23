import psycopg2
from database import connect_to_database
from values import constant


def create(name, data):
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    postgres_insert_query, records_to_insert = '', []

    match name:
        case 'sheets':
            sheet_id, topic_id, sheet_name, sheet_data = data[0], data[1], data[2], data[3]
            postgres_insert_query = """ INSERT INTO """ + constant.DB_SHEETS + """(row, sheet_id, topic_id, sheet_name, timestamp, forum_username, profile_link, social_media_username, followers) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            for row in sheet_data:
                records_to_insert.append(tuple([row[0], sheet_id, topic_id, sheet_name, row[1], row[2], row[3], row[4], row[5]]))

    for record in records_to_insert:
        try:
            cursor.execute(postgres_insert_query, record)
            connection.commit()
        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into the table %s" % constant.DB_SHEETS, error)
        finally:

            print("Inserted %s rows into table: %s" % (len(data[3]), constant.DB_SHEETS))

            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
