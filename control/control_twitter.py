from database import crud_analysis
from database import crud_twitter
from web_scraping import scrape_twitter
import time
from alive_progress import alive_bar

"""
================================================================================================

CONTROL OPERATIONS FOR RETRIEVING TWITTER DATA

================================================================================================
"""


# Retrieve and store Twitter data in the database
def populate_database_twitter():
    data = crud_analysis.read('participation[twitter_links]', [])

    for index, user in enumerate(data):

        topic_id = user[0]
        comment_id = user[1]
        twitter_urls = user[2]

        with alive_bar(len(twitter_urls), title='Comment: %s/%s' % (index + 1, len(data))) as bar:
            for url in twitter_urls:

                tweet_id = get_post_id_from_url(url)

                if tweet_id:

                    exist_check = crud_twitter.read('twitter_tweet[tweet_id]', tweet_id)

                    if not exist_check:

                        try:
                            tweet_user = scrape_twitter.retrieve_data_from_id(tweet_id)
                            if tweet_user[0].get_author_id():
                                crud_twitter.create('populate_twitter_tweet', [topic_id, comment_id, tweet_user[0]])
                            if tweet_user[1].get_author_id():
                                crud_twitter.create('populate_twitter_user', tweet_user[1])
                        except Exception as error:
                            if '429 Too Many Requests' in str(error):
                                print('Reached the maximum number of requests, sleeping for 16 minutes')
                                time.sleep(16 * 60)
                            else:
                                print('Caught an error while retrieving tweet data: ' + str(error))
                bar()


# Retrieve Twitter post id from the collected URL's
def get_post_id_from_url(url):
    post_id = ''

    url_decomposed = url.split('/')
    for i in range(0, len(url_decomposed)):
        if url_decomposed[i] == 'status' and len(url_decomposed) - 1 > i > 0:
            post_id = url_decomposed[i + 1]
            if '?' in post_id:
                post_id = post_id.split('?')[0]

    return post_id


# Retrieve real/fake followers based on the Twitter username
def analyse_followers():
    usernames = crud_twitter.read('twitter_user[username]', [])

    with alive_bar(len(usernames), title='Twitter followers') as bar:
        for username in usernames:

            check = crud_twitter.read('twitter_user[real,fake]', username[0])

            if not check[0][0] and not check[0][1]:
                try:
                    real_fake = scrape_twitter.retrieve_followers(username[1])
                    crud_twitter.update('twitter_user[real, fake]', [username[0], real_fake[0], real_fake[1]])
                except Exception as exception:
                    if exception == 'Breaking':
                        print('Load the entry from the website manually')
                        return

            bar()
