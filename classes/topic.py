class Topic:
    def __init__(self, topic_id=None, url=None, original_topic=None, topic=None, token_name=None, author=None,
                 replies=None, views=None, last_post_time=None, last_post_author=None, sheet_ids=None, image_urls=None,
                 image_check=None, reward_pool=None, reward_allocation=None, campaign=None):
        self.topic_id = topic_id
        self.url = url
        self.original_topic = original_topic
        self.topic = topic
        self.token_name = token_name
        self.author = author
        self.replies = replies
        self.views = views
        self.last_post_time = last_post_time
        self.last_post_author = last_post_author
        self.sheet_ids = sheet_ids
        self.image_urls = image_urls
        self.image_check = image_check
        self.reward_pool = reward_pool
        self.reward_allocation = reward_allocation
        self.campaign = campaign

    def get_topic_id(self):
        return self.topic_id

    def set_topic_id(self, topic_id):
        self.topic_id = topic_id

    def get_url(self):
        return self.url

    def set_url(self, url):
        self.url = url

    def get_original_topic(self):
        return self.original_topic

    def set_original_topic(self, original_topic):
        self.original_topic = original_topic

    def get_topic(self):
        return self.topic

    def set_topic(self, topic):
        self.topic = topic

    def get_token_name(self):
        return self.token_name

    def set_token_name(self, token_name):
        self.token_name = token_name

    def get_author(self):
        return self.author

    def set_author(self, author):
        self.author = author

    def get_replies(self):
        return self.replies

    def set_replies(self, replies):
        self.replies = replies

    def get_views(self):
        return self.views

    def set_views(self, views):
        self.views = views

    def get_last_post_time(self):
        return self.last_post_time

    def set_last_post_time(self, last_post_time):
        self.last_post_time = last_post_time

    def get_last_post_author(self):
        return self.last_post_author

    def set_last_post_author(self, last_post_author):
        self.last_post_author = last_post_author

    def get_sheet_ids(self):
        return self.sheet_ids

    def set_sheet_ids(self, sheet_ids):
        self.sheet_ids = sheet_ids

    def get_image_urls(self):
        return self.image_urls

    def set_image_urls(self, image_urls):
        self.image_urls = image_urls

    def get_image_check(self):
        return self.last_post_author

    def set_image_check(self, image_check):
        self.image_check = image_check

    def get_reward_pool(self):
        return self.reward_pool

    def set_reward_pool(self, reward_pool):
        self.reward_pool = reward_pool

    def get_reward_allocation(self):
        return self.reward_allocation

    def set_reward_allocation(self, reward_allocation):
        self.reward_allocation = reward_allocation

    def get_campaign(self):
        return self.campaign

    def set_campaign(self, campaign):
        self.campaign = campaign

