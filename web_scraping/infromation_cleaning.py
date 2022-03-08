from datetime import datetime
import re

"""
=================================================================================================================
DATA CLEANING PART FOR HOME PAGE DATA

 @ clean_post_information_data - retrieves the data from an object with html enconding and calls cleaning methods
 @ convert_time - converts time and date from 12 hour format to 24 hour format
 @ clean_last_author - cleans new line, tab symbols and "by"
 @ clean_topic - removes useless information
================================================================================================================
"""


# Takes a column and extracts data from it
def clean_post_information_data(column):
    url = column[2].find('a').get('href')
    topic_id = extract_id_from_url(url)
    original_topic = column[2].find('a').text
    topic = clean_topic(original_topic)
    author = column[3].text.strip('\n').strip('\t').rstrip()
    replies = column[4].text.strip('\n').strip('\t').rstrip()
    views = column[5].text.strip('\n').strip('\t').rstrip()
    last_post_time = convert_time(column[6].text.splitlines()[3].strip('\n').strip('\t').rstrip())
    last_post_author = clean_last_author(column[6].text.splitlines()[4])

    return [topic_id, url, original_topic, topic, author, replies, views, last_post_time, last_post_author]


def extract_id_from_url(url):
    topic_id_12 = url.split(".")
    topic_id_1_temp = topic_id_12[-2].split("=")
    topic_id_1 = topic_id_1_temp[-1]

    return topic_id_1


# Converts time to 24-hour format and date to number format
# Converts TODAY into a date and returns a "true" check for re-scraping
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


# Clean last author line
def clean_last_author(last_post_author):
    last_post_author = last_post_author.strip('\n').strip('\t')

    last_post_author = last_post_author.rstrip()

    last_post_author = last_post_author.replace("by ", "")

    return last_post_author


# Clean last topic line
def clean_topic(topic):
    # Regex expressions for emoji's
    emoji_pattern = re.compile("["
                               u"\U0001F9DE"  # aladdin
                               u"\U0001F911"  # money mouth face
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U000024C2-\U0001F251"


                               "]+", flags=re.UNICODE)

    # Remove most emoji characters from topic
    topic = emoji_pattern.sub('', topic)

    # Remove underscores
    topic = topic.replace("_", "")

    # Remove [BOUNTY]
    topic = topic.replace("[Bounty]", "")
    topic = topic.replace("[BOUNTY]", "")
    topic = topic.replace("[BOUNTY STAR]", "")
    topic = topic.replace("[BOUNTY ALADDIN]", "")
    topic = topic.replace("[BOUNTY DETECTIVE]", "")
    topic = topic.replace("[BOUNTY OPPORTUNITY]", "")

    # Remove empty spaces
    topic = topic.strip()

    return topic


"""
================================================================================================================
DATA CLEANING PART FOR COMMENT SECTION DATA

 @ clean_comment_section_data - filters the comments and retrieves useful information

================================================================================================================
"""


def clean_comment_section_data(comments):
    proof_comments = []
    other_comments = []

    for comment in comments:

        if "PROOF" in str(comment.text.upper()):
            proof_comments.append(comment)
        else:
            other_comments.append(comment)

    analysed_proof_comments = extract_data_from_proof_comments(proof_comments)

    return analysed_proof_comments


def extract_data_from_proof_comments(proof_comments):
    results = []

    for comment in proof_comments:

        comment_id = comment.find('a', class_='message_number').text.replace("#", "")

        comment = comment.text.split("\n")

        forum_username = ""
        profile_url = ""
        telegram_username = ""
        campaigns = ""
        time = ""
        address = ""
        data = []

        for text in comment:

            if (
                    "FORUM" in text.upper() or "BITCOINTALK" in text.upper() or "BITCOIN TALK" in text.upper()) and "USERNAME" in text.upper():
                temp = text.split(":")
                forum_username = temp[-1].rstrip()
            elif ("LINK" in text.upper() or "URL" in text.upper()) and "PROFILE" in text.upper():
                temp = text.split(":")
                profile_url = temp[-1].rstrip()
            elif "TELEGRAM" in text.upper():
                temp = text.split(":")
                telegram_username = temp[-1].rstrip()
            elif "CAMPAIGN" in text.upper():
                temp = text.split(":")
                campaigns = temp[-1].rstrip()
            elif "ADDRESS" in text.upper():
                temp = text.split(":")
                address = temp[-1].rstrip()
            elif "JANUARY" in text.upper() or "FEBRUARY" in text.upper() or "MARCH" in text.upper() or "APRIL" in text.upper() or "MAY" in text.upper() or "JUNE" in text.upper() or "JULY" in text.upper() or "AUGUST" in text.upper() or "SEPTEMBER" in text.upper() or "OCTOBER" in text.upper() or "NOVEMBER" in text.upper() or "DECEMBER" in text.upper():
                time = text.rstrip()
            else:
                data.append(text)

        results.append([comment_id, forum_username, profile_url, telegram_username, campaigns, time, address])

    return results
