from web_scraping import scrape_sheets
from database import crud_topic
from database import crud_sheets
from information_cleaning import clean_spreadsheets
from alive_progress import alive_bar

"""
================================================================================================

CONTROL OPERATIONS FOR GOOGLE SHEETS DATA RETRIEVAL

================================================================================================
"""


# Form an array of data based on the operation mode
def populate_database_sheets(mode):
    data = crud_topic.read('topic[topic_id, sheet_ids]', [])
    filtered_data = [tup for tup in data if tup[1] is not None and tup[1] != []]

    if mode.isnumeric() and int(mode) < len(filtered_data):
        filtered_data = filtered_data[0:int(mode)]

    create_sheet_records(filtered_data)


# Retrieve and store entries from Google sheets to the database
def create_sheet_records(data):
    with alive_bar(len(data), title='Google sheets') as bar:
        for index, entry in enumerate(data):

            successful_check = crud_topic.read('successful_transfers[sheet_successful]', entry[0])

            if not successful_check[0][0]:

                for sheet_id in entry[1]:

                    sheet_data = scrape_sheets.fetch_sheet_data(sheet_id)

                    for sheet in sheet_data:
                        cleaned_sheet_array = clean_spreadsheets.clean_sheets_data(sheet[1])

                        crud_sheets.create('populate_sheets', [sheet_id, entry[0], sheet[0], cleaned_sheet_array])

            bar()
