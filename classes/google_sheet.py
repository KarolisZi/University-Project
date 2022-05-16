class Sheet:
    def __init__(self, topic_id=None, row=None, sheet_id=None, sheet_name=None, timestamp=None, forum_username=None,
                 profile_url=None, social_media_username=None, followers=None, telegram_username = None):
        self.topic_id = topic_id
        self.row = row
        self.sheet_id = sheet_id
        self.sheet_name = sheet_name
        self.timestamp = timestamp
        self.forum_username = forum_username
        self.profile_url = profile_url
        self.social_media_username = social_media_username
        self.followers = followers
        self.telegram_username = telegram_username


    def get_topic_id(self):
        return self.topic_id

    def set_topic_id(self, topic_id):
        self.topic_id = topic_id

    def get_row(self):
        return self.row

    def set_row(self, row):
        self.row = row

    def get_sheet_id(self):
        return self.sheet_id

    def set_sheet_id(self, sheet_id):
        self.sheet_id = sheet_id

    def get_sheet_name(self):
        return self.sheet_name

    def set_sheet_name(self, sheet_name):
        self.sheet_name = sheet_name

    def get_timestamp(self):
        return self.timestamp

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def get_forum_username(self):
        return self.forum_username

    def set_forum_username(self, forum_username):
        self.forum_username = forum_username

    def get_profile_url(self):
        return self.profile_url

    def set_profile_url(self, profile_url):
        self.profile_url = profile_url

    def get_social_media_username(self):
        return self.social_media_username

    def set_social_media_username(self, social_media_username):
        self.social_media_username = social_media_username

    def get_followers(self):
        return self.followers

    def set_followers(self, followers):
        self.followers = followers

    def get_telegram_username(self):
        return self.telegram_username

    def set_telegram_username(self, telegram_username):
        self.telegram_username = telegram_username
