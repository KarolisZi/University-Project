from values import regex
from information_cleaning import helper_functions

"""
=================================================================================================================
DATA CLEANING PART FOR HOME PAGE DATA

 @ clean_topic_data() - extracts data from the comment and prepares for storage in the database
 @ extract_id_from_url - retrieves the topic id from the URL
 @ retrieve_last_author() - retrieves the topics last post author
 @ clean_topic() - removes redundant information from the topic title
================================================================================================================
"""


# Cleans topic data and returns:
# [Link, Topic, Started by, Replies, Views, Last post time, Last post author]
def clean_topic_data(column):
    url = column[2].find('a').get('href')
    topic_id = extract_id_from_url(url)
    original_topic = column[2].find('a').text
    topic = clean_topic(original_topic)
    author = column[3].text.strip('\n').strip('\t').rstrip().lstrip()
    replies = column[4].text.strip('\n').strip('\t').rstrip().lstrip()
    views = column[5].text.strip('\n').strip('\t').rstrip().lstrip()
    last_post_time = helper_functions.convert_time(
        column[6].text.splitlines()[3].strip('\n').strip('\t').rstrip()).lstrip()
    last_post_author = retrieve_last_post_author(column[6].text.splitlines()[4])

    return [topic_id, url, original_topic, topic, author, replies, views, last_post_time, last_post_author]


def extract_id_from_url(url):
    topic_id_12 = url.split(".")
    topic_id_1_temp = topic_id_12[-2].split("=")
    topic_id_1 = topic_id_1_temp[-1]

    return topic_id_1


def retrieve_last_post_author(last_post_author):

    last_post_author = last_post_author.strip('\n').strip('\t')

    last_post_author = last_post_author.rstrip()

    last_post_author = last_post_author.replace("by ", "")

    return last_post_author


# Clean last topic line
def clean_topic(topic):
    # Regex expressions for emoji's

    # Remove most emoji characters from topic
    topic = regex.emoji_pattern.sub('', topic)

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
