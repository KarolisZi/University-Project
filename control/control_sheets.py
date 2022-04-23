from web_scraping import scrape_sheets
from database import crud_topic
from database import create_table
from database import crud_sheets
from information_cleaning import clean_spreadsheets
from alive_progress import alive_bar

"""
================================================================================================

CONTROL OPERATIONS FOR GOOGLE SHEETS DATA RETRIEVAL

================================================================================================
"""


def populate_database_sheets(mode):

    data = crud_topic.read('topic[topic_id, sheet_ids]', [])

    create_table.google_sheets()

    if mode == "all":
        create_all_sheet_records(data)
    elif mode.isnumeric():
        create_x_sheet_records(data, int(mode))


def create_all_sheet_records(data):
    with alive_bar(len(data), title='Sheets') as bar:
        for ids in data:

            sheet_ids = ids[1].replace('{', '').replace('}', '').split(',')

            for sheet_id in sheet_ids:

                sheet_data = scrape_sheets.fetch_sheet_data(sheet_id)

                for sheet in sheet_data:
                    cleaned_sheet_data = clean_spreadsheets.clean_sheets_data(sheet[1])

                    crud_sheets.create('sheets', [sheet_id, ids[0], sheet[0], cleaned_sheet_data])
        bar()


def create_x_sheet_records(data, number):

    for topic_sheet in data:

        while number > 0:

            for sheet_id in topic_sheet[1]:

                sheet_data = scrape_sheets.fetch_sheet_data(sheet_id)

                for sheet in sheet_data:

                    cleaned_sheet_data = clean_spreadsheets.clean_sheets_data(sheet[1])

                    crud_sheets.create('sheets', [sheet_id, topic_sheet[0], sheet[0], cleaned_sheet_data])

            number -= 1

