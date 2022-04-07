from web_scraping import scrape_sheets
from database import db_crud_topics
from database import create_table
from database import db_crud_sheets
from information_cleaning import clean_spreadsheets
from alive_progress import alive_bar

"""
================================================================================================

CONTROL OPERATIONS FOR GOOGLE SHEETS DATA RETRIEVAL

================================================================================================
"""


def populate_database_sheets(check):
    data = db_crud_topics.fetch_all_id_sheet_ids()

    create_table.google_sheets()

    if check == "all":
        create_all_sheet_records(data)
    elif check.isnumeric():
        create_x_sheet_records(data, int(check))


def create_all_sheet_records(data):
    with alive_bar(len(data), title='Sheets') as bar:
        for ids in data:

            sheet_ids = ids[1].replace('{', '').replace('}', '').split(',')

            for sheet_id in sheet_ids:

                sheet_data = scrape_sheets.fetch_sheet_data(sheet_id)

                for sheet in sheet_data:
                    cleaned_sheet_data = clean_spreadsheets.clean_sheets_data(sheet[1])

                    db_crud_sheets.insert_sheets(sheet_id, ids[0], sheet[0], cleaned_sheet_data)
        bar()


def create_x_sheet_records(data, number):
    for ids in data:

        sheet_ids = ids[1].replace('{', '').replace('}', '').split(',')

        while number > 0:

            for sheet_id in sheet_ids:

                sheet_data = scrape_sheets.fetch_sheet_data(sheet_id)

                for sheet in sheet_data:
                    cleaned_sheet_data = clean_spreadsheets.clean_sheets_data(sheet[1])

                    db_crud_sheets.insert_sheets(sheet_id, ids[0], sheet[0], cleaned_sheet_data)

            number -= 1

