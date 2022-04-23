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

twitter_username_url_pattern = re.compile('https\:\/\/(www.)?(mobile.)?twitter\.com\/\w*$')
facebook_username_url_pattern = re.compile('https\:\/\/(www.)?(web.)?(m.)?facebook\.com\/\w*$')

spreadsheet_pattern = re.compile('https\:\/\/(www.)?docs\.google\.com\/spreadsheets\/.*')


eth_patter = re.compile('/^0x[a-fA-F0-9]{40}$/g')

#url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
url_regex = re.compile('(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})')

image_proxy_pattern = re.compile('https\:\/\/ip.bitcointalk.org\/\?u=')

day_number = re.compile('[d,D]ay\:? ?\d{1,2}')
week_number = re.compile('[w,W]eek\:? ?\d{1,2}')
day_month = re.compile('((0[1-9]|1[0-2])\/([01][1-9]|10|2[0-8]))|((0[13-9]|1[0-2])\/(29|30))|((0[13578]|1[0-2])\/31)')
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

number_letter_format = re.compile('[0-9]*K?M?k?m?B?b?Ƀ?$')

'''
========================================================================================================================
INFORMATION_CLEANING_SHEETS
========================================================================================================================
'''

profile_url_format = re.compile('https:\/\/bitcointalk.org\/index.php\?action=profile;u=\d\d\d\d\d\d\d')

'''
========================================================================================================================
INFORMATION_CLEANING_AUTHOR
========================================================================================================================
'''

reward_pool_amount = re.compile('(\$)?(\$ )?[0-9,. ]{2,15}( ?[A-Z]{3,12})?')
