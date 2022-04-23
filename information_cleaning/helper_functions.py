from datetime import datetime
import enchant
from values import regex

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
    id_12 = url.split('=')[-1].split('.')

    return id_12


def extract_post_time_and_id(comment):
    # Retrieve post and header
    header_post = comment.find('td', class_="td_headerandpost")

    id = header_post.find('a', class_='message_number').text.replace("#", "")

    # Retrieve time from the header
    time = header_post.find('div', class_='smalltext').text

    if 'Last edit:' in time:
        temp = time.split('Last edit:')
        time = temp[0].strip()

    time = convert_time(time)

    return [time, id]


def extract_token_name(topic):
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
    elif len(words) > 1:
        for i in range(0, len(words)):

            words[i] = words[i].strip()

            # Making sure that other common words that would match the criteria ar not the TOKEN name
            if symbols_abbreviations_check(words[i]):
                # 2)
                if 'TOKEN' == words[i].upper() or 'TOKENS' == words[i].upper() or 'COIN' == words[
                    i].upper() or 'STABLECOIN' == words[i].upper() and i != 0:
                    if words[i - 1] != 'of':
                        token_name = words[i - 1]
                        break
                # 3)
                elif words[i].isupper() and 1 < len(words[i]) < 15 and not regex.number_letter_format.match(words[i]):
                    if not en_US.check(words[i]) and not en_GB.check(words[i]):
                        token_name = words[i]
                        break
                    # 4)
                    elif words[i].isupper() and 1 < len(words[i]) < 6:
                        possible_token_names.append(words[i])
    # 5)
    if not token_name:
        for i in range(0, len(words)):
            if symbols_abbreviations_check(words[i]) and 1 < len(words[i]) < 6 and not en_US.check(
                    words[i]) and not en_GB.check(words[i]) and not words[i].islower():
                possible_token_names.append(words[i])
                break
    elif token_name:
        possible_token_names.insert(0, token_name)

    return possible_token_names


def symbols_abbreviations_check(word_to_analyse):
    # Array of words that should not be equal to the TOKEN name
    abbreviations = ['ETH', 'BTC', 'NFT', 'USD', 'ERC20', 'BEP20', 'APY', 'POOL', 'Million', 'BUSD', 'KYC']
    # Symbols that should not be in a TOKEN name
    symbols = ['$', '*', '@', ',']

    for abbreviation in abbreviations:
        if abbreviation == word_to_analyse:
            return False

    for symbol in symbols:
        if symbol in word_to_analyse:
            return False

    if word_to_analyse.isdigit():
        return False

    return True
