import re
from values import regex
from information_cleaning import helper_functions
import enchant

"""
=================================================================================================================
DATA CLEANING PART FOR HOME PAGE DATA

 @ clean_topic_data() - extracts data from the comment and prepares for storage in the database
 @ extract_id_from_url - retrieves the topic id from the URL
 @ retrieve_last_author() - retrieves the topics last post author
 @ clean_topic() - removes redundant information from the topic title
 @ extract_coin_name() - retrieves the TOKEN name from the topic
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
    author = column[3].text.strip('\n').strip('\t').strip()
    replies = column[4].text.strip('\n').strip('\t').strip()
    views = column[5].text.strip('\n').strip('\t').strip()
    last_post_time = helper_functions.convert_time(column[6].text.splitlines()[3].strip('\n').strip('\t')).strip()
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


def extract_coin_name(topic):
    possible_token_names = []
    token_name = ''

    en_US = enchant.Dict("en_US")
    en_GB = enchant.Dict("en_GB")

    # Higher chance for the token name to be at the start of the string
    words = topic.split(' ')

    """
        TOKEN NAME FILTERING RULES (1st rule is superior to 2nd and etc...)
        1) If the topic has a length of 1, that is the TOKEN name
        2) The word followed by the word 'COIN', 'TOKEN', 'TOKENS', 'STABLECOIN' is the TOKEN name
        3) Non English words with all capital letters (3 - 10 letters) and not number followed by K, k, M, m
        4) English Words with all capital letters (3 - 5 letters)
        5) If no TOKEN name is found then take the first word as a TOKEN name
    """

    # 1)
    if len(words) == 1:
        token_name = words[0]
        # print('Rule #1')
    elif len(words) > 1:
        for i in range(0, len(words)):

            words[i] = words[i].strip()

            # Making sure that other common words that would match the criteria ar not the TOKEN name
            if symbols_abbreviations_check(words[i]):
                # 2)
                if 'TOKEN' == words[i].upper() or 'TOKENS' == words[i].upper() or 'COIN' == words[i].upper() or 'STABLECOIN' == words[i].upper() and i != 0:
                    if words[i-1] != 'of':
                        token_name = words[i - 1]
                        # print('Rule #2')
                        break
                # 3)
                elif words[i].isupper() and 1 < len(words[i]) < 15 and not regex.number_letter_format.match(words[i]):
                    if not en_US.check(words[i]) and not en_GB.check(words[i]):
                        token_name = words[i]
                        # print('Rule #3')
                        break
                    # 4)
                    elif words[i].isupper() and 1 < len(words[i]) < 6:
                        possible_token_names.append(words[i])
                        # print('Rule #4')
    # 5)
    if not token_name:
        for i in range(0, len(words)):
            if symbols_abbreviations_check(words[i]) and 1 < len(words[i]) < 6:
                possible_token_names.append(words[i])
                break
        # print('Rule #5')
    elif token_name:
        possible_token_names.insert(0, token_name)

    return possible_token_names


def symbols_abbreviations_check(word_to_analyse):

    # Array of words that should not be equal to the TOKEN name
    abbreviations = ['ETH', 'BTC', 'NFT', 'USD', 'ERC20', 'BEP20', 'APY', 'POOL', 'Million', 'BUSD', 'KYC']
    # Symbols that should not be in a TOKEN name
    symbols = ['$', '.', '*', '@', ',']

    for abbreviation in abbreviations:
        if abbreviation == word_to_analyse:
            return False

    for symbol in symbols:
        if symbol in word_to_analyse:
            return False

    if word_to_analyse.isdigit():
        return False

    return True



