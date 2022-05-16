import time
import gspread

"""
================================================================================================

FUNCTIONS FOR RETRIEVING DATA FROM GOOGLE SHEETS

================================================================================================
"""


# Retrieve data from a Google sheet
def fetch_sheet_data(sheet_id):
    sheet_data = []

    sa = gspread.service_account(filename='API/service_account.json')

    try:
        sh = sa.open_by_key(sheet_id)

        worksheet_list = sh.worksheets()

        for worksheet in worksheet_list:

            try:

                sheet_data.append([worksheet.title, worksheet.get_all_values()])

            except (Exception, gspread.exceptions.APIError) as error:

                print('Quota exceeded, sleeping for 1 minute')
                time.sleep(60)
                sheet_data.append([worksheet.title, worksheet.get_all_values()])

    except (Exception, gspread.exceptions.APIError) as error:
        if sheet_id == '':
            print('Error: no sheet_id provided')
        else:
            print('Error: ' + str(error))
    return sheet_data
