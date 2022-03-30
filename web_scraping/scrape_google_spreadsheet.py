import gspread
import time


def fetch_sheet_data(sheet_id):
    sheet_data = []

    sa = gspread.service_account(filename='API/service_account.json')
    try:
        if sheet_id != '' and sheet_id is not None:
            sh = sa.open_by_key(sheet_id)

            worksheet_list = sh.worksheets()

            for worksheet in worksheet_list:

                try:

                    sheet_data.append([worksheet.title, worksheet.get_all_values()])

                except gspread.exceptions.APIError:

                    print('Quota exceeded, sleeping for 1 minute')
                    time.sleep(60)
                    sheet_data.append([worksheet.title, worksheet.get_all_values()])

    except gspread.exceptions.APIError:
        print('Error: ' + str(gspread.exceptions.APIError))
        # Insert into the database that the sheet no longer exists
    return sheet_data
