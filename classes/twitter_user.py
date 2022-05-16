class TUser:
    def __init__(self, author_id=None, name=None, username=None, created_at=None, followers=None, following=None,
                 tweet_count=None, listed_count=None):
        self.author_id = author_id
        self.name = name
        self.username = username
        self.created_at = created_at
        self.followers = followers
        self.following = following
        self.tweet_count = tweet_count
        self.listed_count = listed_count

    def get_author_id(self):
        return self.author_id

    def set_author_id(self, author_id):
        self.author_id = author_id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_username(self):
        return self.username

    def set_username(self, username):
        self.username = username

    def get_created_at(self):
        return self.created_at

    def set_created_at(self, created_at):
        self.created_at = created_at

    def get_followers(self):
        return self.followers

    def set_followers(self, followers):
        self.followers = followers

    def get_following(self):
        return self.following

    def set_following(self, following):
        self.following = following

    def get_tweet_count(self):
        return self.tweet_count

    def set_tweet_count(self, tweet_count):
        self.tweet_count = tweet_count

    def get_listed_count(self):
        return self.listed_count

    def set_listed_count(self, listed_count):
        self.listed_count = listed_count
