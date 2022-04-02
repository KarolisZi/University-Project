import re

'''
========================================================================================================================
INFORMATION_CLEANING_COMMENTS
========================================================================================================================
'''
twitter_url_pattern = re.compile('https\:\/\/(www.)?(mobile.)?twitter\.com\/\w*')
facebook_url_pattern = re.compile('https\:\/\/(www.)?(web.)?(m.)?facebook\.com\/\w*')
telegram_url_pattern = re.compile('https\:\/\/(www.)?t\.me\/\w*')
instagram_url_pattern = re.compile('https\:\/\/(www.)?instagram\.com\/\w*')
reddit_url_pattern = re.compile('https\:\/\/(www.)reddit\.com\/\w*')

twitter_username_url_pattern = re.compile('https\:\/\/(www.)reddit\.com\/\w*$')
facebook_username_url_pattern = re.compile('https\:\/\/(www.)?(web.)?(m.)?facebook\.com\/\w*$')
# IDEA https://www.facebook.com/profile.php?id =

spreadsheet_pattern = re.compile('https\:\/\/(www.)?docs\.google\.com\/spreadsheets\/\w*')

eth_patter = re.compile('/^0x[a-fA-F0-9]{40}$/g')

url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

image_proxy_pattern = re.compile('https\:\/\/ip.bitcointalk.org\/\?u=')
'''
========================================================================================================================
INFORMATION_CLEANING_TOPIC
========================================================================================================================
'''

emoji_pattern = re.compile(u"(["
                           u"\U0001F600-\U0001F64F"  # Emoticons
                           u"\U0001F300-\U0001F5FF"  # Miscellaneous Symbols and Pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002B00-\U00002BFF"  # Miscellaneous Symbols and Arrows
                           u"\U00002700-\U000027BF"  # Dingbats
                           u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                           u"\U00002600-\U000026FF"  # Miscellaneous Symbols
                           u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended 
                           u"\U00002600-\U000026FF"  # Miscellaneous Symbols 
                           u"\U000025A0-\U000025FF"  # Geometric Shapes
                           u"\U00002300-\U000023FF"  # Miscellaneous Technical
                           u"\U00002580-\U0000259F"  # Block Elements
                           u"\U0001F100-\U0001F1FF"  # Enclosed Alphanumeric Supplement
                           u"\U00003000-\U0000303F"  # CJK Symbols and Punctuation
                           u"\U0001F0A0-\U0001F0FF"  # Playing Cards
                           u"\U0000FFF0-\U0000FFFF"  # Specials
                           "])", flags= re.UNICODE)


token_all_capitals = re.compile("[A-Z]{3,10}")
token_all_capitals_short = re.compile("[A-Z]{3,5}")


'''
========================================================================================================================
INFORMATION_CLEANING_SHEETS
========================================================================================================================
'''

profile_url_format = re.compile('https:\/\/bitcointalk.org\/index.php\?action=profile;u=\d\d\d\d\d\d\d')
