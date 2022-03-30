import gspread
import time


def fetch_sheet_data(id):
    sheet_data = []

    sa = gspread.service_account(filename='API/service_account.json')
    sh = sa.open_by_key(id)

    worksheet_list = sh.worksheets()

    for worksheet in worksheet_list:

        try:

            sheet_data.append([worksheet.title, worksheet.get_all_values()])

        except gspread.exceptions.APIError:

            print('Quota exceeded, sleeping for 1 minute')
            time.sleep(60)
            sheet_data.append([worksheet.title, worksheet.get_all_values()])

    return sheet_data
