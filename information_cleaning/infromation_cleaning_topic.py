from values import regex
from information_cleaning import helper_functions
import enchant
import numpy as np

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
    token_name = extract_coin_name(topic)
    author = column[3].text.strip('\n').strip('\t').rstrip().lstrip()
    replies = column[4].text.strip('\n').strip('\t').rstrip().lstrip()
    views = column[5].text.strip('\n').strip('\t').rstrip().lstrip()
    last_post_time = helper_functions.convert_time(
        column[6].text.splitlines()[3].strip('\n').strip('\t').rstrip()).lstrip()
    last_post_author = retrieve_last_post_author(column[6].text.splitlines()[4])

    return [topic_id, url, original_topic, topic, token_name, author, replies, views, last_post_time, last_post_author]


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

    # Remove emoji characters from topic
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
    topic = topic.replace("[LIVE BOUNTY]", "")
    topic = topic.replace("[ANN]", "")
    topic = topic.replace("[ICO]", "")
    topic = topic.replace("ICO", "")
    topic = topic.replace("PRE-ICO", "")
    topic = topic.replace("[CLOSED]", "")
    topic = topic.replace("(Bounty)", "")
    topic = topic.replace("(BOUNTY)", "")
    topic = topic.replace("BOUNTY", "")
    topic = topic.replace("Bounty", "")

    # Remove empty spaces
    topic = topic.strip()

    return topic


def extract_coin_name(topic):

    fist_word = ''
    token_name = []

    en_US = enchant.Dict("en_US")
    en_GB = enchant.Dict("en_GB")

    # Higher chance for the token name to be at the start of the string
    words = np.flip(topic.split(' '))

    for word in words:

        word = word.replace('[', '')
        word = word.replace(']', '')
        word = word.replace('(', '')
        word = word.replace(')', '')
        word = word.replace('|', '')
        word = word.replace('.', '')
        word = word.replace(':', '')

        if word != '':

            if 'ETH' not in word and 'BTC' not in word and '$' not in word and 'NFT' not in word and 'USD' not in word and 'ERC20' not in word and 'BEP20' not in word and 'APY' not in word and 'POOL' not in word:

                if regex.token_all_capitals.match(word):
                    if not en_US.check(word) and not en_GB.check(word):
                        token_name.append(word)
                    elif regex.token_all_capitals_short.match(word):
                        token_name.append(word)

            fist_word = word

    if not token_name:
        token_name.append(fist_word)


    return token_name
