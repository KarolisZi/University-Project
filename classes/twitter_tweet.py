class TTweet:
    def __init__(self, tweet_id=None, author_id=None, text=None, retweet=None, created_at=None, retweet_count=None, reply_count=None,
                 like_count=None, quote_count=None):
        self.tweet_id = tweet_id
        self.author_id = author_id
        self.text = text
        self.retweet = retweet
        self.created_at = created_at
        self.retweet_count = retweet_count
        self.reply_count = reply_count
        self.like_count = like_count
        self.quote_count = quote_count

    def get_tweet_id(self):
        return self.tweet_id

    def set_tweet_id(self, tweet_id):
        self.tweet_id = tweet_id

    def get_author_id(self):
        return self.author_id

    def set_author_id(self, author_id):
        self.author_id = author_id

    def get_text(self):
        return self.text

    def set_text(self, text):
        self.text = text

    def get_retweet(self):
        return self.retweet

    def set_retweet(self, retweet):
        self.retweet = retweet

    def get_created_at(self):
        return self.created_at

    def set_created_at(self, created_at):
        self.created_at = created_at

    def get_retweet_count(self):
        return self.retweet_count

    def set_retweet_count(self, retweet_count):
        self.retweet_count = retweet_count

    def get_reply_count(self):
        return self.reply_count

    def set_reply_count(self, reply_count):
        self.reply_count = reply_count

    def get_like_count(self):
        return self.like_count

    def set_like_count(self, like_count):
        self.like_count = like_count

    def get_quote_count(self):
        return self.quote_count

    def set_quote_count(self, quote_count):
        self.quote_count = quote_count
