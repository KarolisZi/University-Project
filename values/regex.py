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

'''
========================================================================================================================
INFORMATION_CLEANING_TOPIC
========================================================================================================================
'''

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


'''
========================================================================================================================
INFORMATION_CLEANING_SHEETS
========================================================================================================================
'''

profile_url_format = re.compile('https:\/\/bitcointalk.org\/index.php\?action=profile;u=\d\d\d\d\d\d\d')