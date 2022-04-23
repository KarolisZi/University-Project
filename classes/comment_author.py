class Author:
    def __init__(self, topic_id=None, comment_id=None, text_data=[], image_data=[], image_check=None, image_urls=[], post_time=0):
        self.topic_id = topic_id
        self.comment_id = comment_id
        self.text_data = text_data
        self.image_data = image_data
        self.image_check = image_check
        self.image_urls = image_urls
        self.post_time = post_time

    def get_topic_id(self):
        return self.topic_id

    def set_topic_id(self, topic_id):
        self.topic_id = topic_id

    def get_comment_id(self):
        return self.comment_id

    def set_comment_id(self, comment_id):
        self.comment_id = comment_id

    def get_text_data(self):
        return self.text_data

    def set_text_data(self, text_data):
        self.text_data = text_data

    def get_image_data(self):
        return self.image_data

    def set_image_data(self, image_data):
        self.image_data.append(image_data)

    def get_image_check(self):
        return self.image_check

    def set_image_check(self, image_check):
        self.image_check = image_check

    def get_image_urls(self):
        return self.image_urls

    def set_image_urls(self, image_urls):
        self.image_urls = image_urls

    def get_post_time(self):
        return self.post_time

    def set_post_time(self, post_time):
        self.post_time = post_time
