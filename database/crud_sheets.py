import psycopg2
from database import connect_to_database
from values import constant

"""
========================================================================================================================

CRUD OPERATION FOR GOOGLE SHEETS RELATED DATA

========================================================================================================================
"""


def create(name, data):
    postgres_insert_query, records_to_insert, errors_no, errors = '', [], 0, []

    match name:
        case 'populate_sheets':
            sheet_id, topic_id, sheet_name, sheet_data = data[0], data[1], data[2], data[3]
            postgres_insert_query = """ INSERT INTO """ + constant.DB_SHEETS + """(row, sheet_id, topic_id, sheet_name, timestamp, forum_username, profile_link, social_media_username, followers, telegram_username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            for row in sheet_data:
                records_to_insert.append(tuple(
                    [row.get_row(), sheet_id, topic_id, sheet_name, row.get_timestamp(), row.get_forum_username(),
                     row.get_profile_url(), row.get_social_media_username(), row.get_followers(),
                     row.get_telegram_username()]))

    for record in records_to_insert:
        connection = connect_to_database.connect_to_the_database()
        cursor = connection.cursor()
        try:
            cursor.execute(postgres_insert_query, record)
            connection.commit()
        except (Exception, psycopg2.Error) as error:
            errors.append(str(error))

        finally:
            if connection:
                cursor.close()
                connection.close()

    if errors:
        update('successful_transfers[sheet_successful=True]', data[1])
        print("Successfully inserted %s rows into table: %s" % (len(data[3]), constant.DB_SHEETS))
    elif not errors:
        update('successful_transfers[sheet_successful=False]', data[1])
        print('When inserting %s rows to %s, encountered %s errors:' % (len(data[3]), constant.DB_SHEETS, len(errors)))
        for error in errors:
            print(error)


def update(name, data):
    connection = connect_to_database.connect_to_the_database()
    cursor = connection.cursor()

    table_name, postgres_update_query, record_to_insert = '', '', ''

    match name:
        case 'successful_transfers[sheet_successful=True]':
            table_name, topic_id = constant.DB_SUCCESSFUL_TRANSFERS, data
            postgres_update_query = """UPDATE """ + table_name + """ SET sheet_successful = True WHERE topic_id = %s"""
            record_to_insert = (topic_id,)
        case 'successful_transfers[sheet_successful=False]':
            table_name, topic_id = constant.DB_SUCCESSFUL_TRANSFERS, data
            postgres_update_query = """UPDATE """ + table_name + """ SET sheet_successful = False WHERE topic_id = %s"""
            record_to_insert = (topic_id,)

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
