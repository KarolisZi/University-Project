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
    author = column[3].text.strip('\n').strip('\t').rstrip().lstrip()
    replies = column[4].text.strip('\n').strip('\t').rstrip().lstrip()
    views = column[5].text.strip('\n').strip('\t').rstrip().lstrip()
    last_post_time = convert_time(column[6].text.splitlines()[3].strip('\n').strip('\t').rstrip()).lstrip()
    last_post_author = clean_last_author(column[6].text.splitlines()[4])

    return [topic_id, url, original_topic, topic, author, replies, views, last_post_time, last_post_author]


def extract_id_from_url(url):
    topic_id_12 = url.split(".")
    topic_id_1_temp = topic_id_12[-2].split("=")
    topic_id_1 = topic_id_1_temp[-1]

    return topic_id_1


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


def clean_comment_section_data(comments, author):
    proof_comments = []
    other_comments = []

    for comment in comments:

        if "PROOF" in str(comment.text.upper()):
            proof_comments.append(comment)
        else:
            other_comments.append(comment)

    analysed_proof_comments = extract_data_from_proof_comments(proof_comments, author)

    return analysed_proof_comments


def extract_data_from_proof_comments(proof_comments, author):
    results = []
    eth_patter = re.compile('/^0x[a-fA-F0-9]{40}$/g')

    for comment in proof_comments:

        telegram_username = ""
        campaigns = ""
        address = ""
        data = []

        # Retrieve forum username and link
        poster_info = comment.find('td', class_="poster_info")
        forum_username = poster_info.find('a').text
        profile_url = poster_info.find('a').get('href')

        # Retrieve post and header
        header_post = comment.find('td', class_="td_headerandpost")

        # Retrieve comment_id from the header
        comment_id = header_post.find('a', class_='message_number').text.replace("#", "")

        # Retrieve time from the header
        time = header_post.find('div', class_='smalltext').text

        # Retrieve post from header and post
        post = header_post.find('div', class_='post').text.split("\n")

        if forum_username != author:

            for text in post:

                # Telegram user name
                if "TELEGRAM" and "USER" and "NAME" in text.upper():
                    temp = text.replace(":", " : ")
                    temp = temp.split(":")
                    telegram_username = temp[-1].rstrip().lstrip()

                elif "CAMPAIGN" in text.upper():
                    temp = text.split(":")
                    campaigns = temp[-1].rstrip().lstrip()
                elif "ADDRESS" in text.upper():
                    temp = text.split(":")
                    if eth_patter.match(temp[-1].rstrip().lstrip()):
                        address = temp[-1].rstrip().lstrip()
                else:
                    data.append(text)

            results.append([comment_id, forum_username, profile_url, telegram_username, campaigns, time, address])

    return results