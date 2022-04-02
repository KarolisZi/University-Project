from datetime import datetime

"""
========================================================================================================================

HELPER FUNCTIONS USED FOR COMMENT AND TOPIC CLEANING

@ convert_time() - converts the time from 12-hour format to 24-hour format
========================================================================================================================
"""


# Converts time to 24-hour format and date to number format
def convert_time(last_post_time):
    if "Today" in last_post_time:

        # 2 - time in hours, 3 - PM/AM
        time = last_post_time.split(" ")

        result = str(datetime.today().date()) + " " + str(time[2]) + " " + str(time[3])

        in_time = datetime.strptime(result, "%Y-%m-%d %I:%M:%S %p")

        out_time = datetime.strftime(in_time, "%Y-%m-%d %H:%M:%S")

        return out_time
    else:

        in_time = datetime.strptime(last_post_time, "%B %d, %Y, %I:%M:%S %p")

        out_time = datetime.strftime(in_time, "%Y-%m-%d %H:%M:%S")

        return out_time


def get_topic_ids(url):
    url_decomposed = url.split('=')
    id_12 = url_decomposed[-1].split('.')
    return id_12
