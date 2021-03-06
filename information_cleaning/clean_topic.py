import re
from classes.topic import Topic
from values import regex
from information_cleaning import helper_functions

"""
=================================================================================================================
DATA CLEANING PART FOR TOPIC (THREAD) DATA
================================================================================================================
"""


# Extracts topic related information from the retrieved data
def clean_topic_data(column, mode):
    topic = Topic(None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)

    topic.set_url(column[2].find('a').get('href'))
    topic.set_topic_id(extract_id_from_url(topic.get_url()))
    topic.set_replies(column[4].text.strip('\n').strip('\t').strip())
    topic.set_views(column[5].text.strip('\n').strip('\t').strip())
    topic.set_last_post_time(
        helper_functions.convert_time(column[6].text.splitlines()[3].strip('\n').strip('\t')).strip())
    topic.set_last_post_author(retrieve_last_post_author(column[6].text.splitlines()[4]))
    topic.set_author(column[3].text.strip('\n').strip('\t').strip())
    match mode:
        case 'updates':
            return topic
        case 'full':
            topic.set_original_topic(column[2].find('a').text)
            topic.set_topic(clean_topic(topic.get_original_topic()))

            return topic


# Retrieve topic id from the URL
def extract_id_from_url(url):
    return url.split('.')[-2].split('=')[-1]


# Retrieve last post author
def retrieve_last_post_author(last_post_author):
    last_post_author = last_post_author.strip('\n').strip('\t')

    last_post_author = last_post_author.rstrip()

    last_post_author = last_post_author.replace("by ", "")

    return last_post_author


# Clean last topic subject line
def clean_topic(topic):
    # The number of emojis used
    emoji_len = len(re.findall(regex.emoji_pattern, topic))
    # Remove emoji characters from topic
    topic = regex.emoji_pattern.sub(' ', topic)

    # Remove underscores
    topic = topic.replace("_", "")

    for string in ['Bounty Star', 'Bounty Aladdin', 'Bounty Detective', 'Bounty Opportunity', 'Live Bounty', 'Bounty',
                   'ANN', 'ICO', 'PRE-ICO', 'Closed', 'Finished', 'Ended', 'End', 'ILO', '[', ']', '(', ')', '|', ':',
                   '!', 'Airdrop', '&']:
        if string in topic:
            topic = topic.replace(string, '')
        if string.upper() in topic:
            topic = topic.replace(string.upper(), '')

    # Replace double or triple spaces with one
    topic = topic.replace('      ', ' ')
    topic = topic.replace('     ', ' ')
    topic = topic.replace('    ', ' ')
    topic = topic.replace('   ', ' ')
    topic = topic.replace('  ', ' ')

    # Remove empty spaces
    topic = topic.strip()

    return topic
