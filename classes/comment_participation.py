class Participation:
    def __init__(self, topic_id=None, page_id=None, comment_id=None, forum_username=None, forum_profile_url=None,
                 week=[], social_media_handle=None, participation=None, post_time=None, twitter_links=None,
                 facebook_links=None,
                 instagram_links=None, telegram_links=None, reddit_links=None, other_links=None):
        self.topic_id = topic_id
        self.page_id = page_id
        self.comment_id = comment_id
        self.forum_username = forum_username
        self.forum_profile_url = forum_profile_url
        self.week = week
        self.social_media_handle = social_media_handle
        self.twitter_links = twitter_links
        self.facebook_links = facebook_links
        self.instagram_links = instagram_links
        self.telegram_links = telegram_links
        self.reddit_links = reddit_links
        self.other_links = other_links
        self.participation = participation
        self.post_time = post_time

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

    def get_week(self):
        return self.week

    def set_week(self, week):
        self.week.append(week)

    def get_social_media_handle(self):
        return self.social_media_handle

    def set_social_media_handle(self, social_media_handle):
        self.social_media_handle = social_media_handle

    def get_participation(self):
        return self.participation

    def set_participation(self, participation):
        self.participation = participation

    def get_post_time(self):
        return self.post_time

    def set_post_time(self, post_time):
        self.post_time = post_time

    def get_twitter_links(self):
        return self.twitter_links

    def set_twitter_links(self, twitter_links):
        self.twitter_links = twitter_links

    def get_facebook_links(self):
        return self.facebook_links

    def set_facebook_links(self, facebook_links):
        self.facebook_links = facebook_links

    def get_instagram_links(self):
        return self.instagram_links

    def set_instagram_links(self, instagram_links):
        self.instagram_links = instagram_links

    def get_telegram_links(self):
        return self.telegram_links

    def set_telegram_links(self, telegram_links):
        self.telegram_links = telegram_links

    def get_reddit_links(self):
        return self.reddit_links

    def set_reddit_links(self, reddit_links):
        self.reddit_links = reddit_links

    def get_other_links(self):
        return self.other_links

    def set_other_links(self, other_links):
        self.other_links = other_links
