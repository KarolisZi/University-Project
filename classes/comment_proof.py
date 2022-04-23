class Proof:
    def __init__(self, topic_id=None, page_id=None, comment_id=None, forum_username=None, forum_profile_url=None,
                 telegram_username=None, campaigns=[], post_time=None, wallet_address=None):
        self.topic_id = topic_id
        self.page_id = page_id
        self.comment_id = comment_id
        self.forum_username = forum_username
        self.forum_profile_url = forum_profile_url
        self.telegram_username = telegram_username
        self.campaigns = campaigns
        self.post_time = post_time
        self.wallet_address = wallet_address

    def get_topic_id(self):
        return self.topic_id

    def set_topic_id(self, topic_id):
        self.topic_id = topic_id

    def get_page_id(self):
        return self.page_id

    def set_page_id(self, page_id):
        self.page_id = page_id

    def get_comment_id(self):
        return self.comment_id

    def set_comment_id(self, comment_id):
        self.comment_id = comment_id

    def get_forum_username(self):
        return self.forum_username

    def set_forum_username(self, forum_username):
        self.forum_username = forum_username

    def get_forum_profile_url(self):
        return self.forum_profile_url

    def set_forum_profile_url(self, forum_profile_url):
        self.forum_profile_url = forum_profile_url

    def get_telegram_username(self):
        return self.telegram_username

    def set_telegram_username(self, telegram_username):
        self.telegram_username = telegram_username

    def get_campaigns(self):
        return self.campaigns

    def set_campaigns(self, campaigns):
        self.campaigns.append(campaigns)

    def get_post_time(self):
        return self.post_time

    def set_post_time(self, post_time):
        self.post_time = post_time

    def get_wallet_address(self):
        return self.wallet_address

    def set_wallet_address(self, wallet_address):
        self.wallet_address = wallet_address
