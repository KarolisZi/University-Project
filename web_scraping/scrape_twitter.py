from API import twitter_keys
import tweepy
from classes.twitter_user import TUser
from classes.twitter_tweet import TTweet
from database import crud_twitter
from values import regex
from values import constant
import requests
from bs4 import BeautifulSoup

"""
================================================================================================

FUNCTIONS FOR RETRIEVING DATA FROM TWITTER

================================================================================================
"""

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/98.0.4758.102 Safari/537.36 '
}


# Retrieve data about the tweet and about the user
def retrieve_data_from_id(tweet_id):
    client = tweepy.Client(bearer_token=twitter_keys.BEARER_TOKEN)

    twitter_tweet = TTweet(None, None, None, None, None, None, None, None)
    twitter_user = TUser(None, None, None, None, None, None, None, None)

    try:
        """================================================= TWEET =================================================="""

        tweet_response = client.get_tweet(id=tweet_id, tweet_fields=["created_at", "public_metrics", "author_id"])

        if tweet_response.data:

            """ Tweet text """
            twitter_tweet.set_text(str(tweet_response.data))

            if regex.retweet.match(twitter_tweet.get_text()):
                twitter_tweet.set_retweet(True)
            else:
                twitter_tweet.set_retweet(False)
            """ Tweet author_id """
            author_id = tweet_response.data.author_id
            twitter_tweet.set_author_id(author_id)

            """ Tweet_id """
            twitter_tweet.set_tweet_id(tweet_id)
            """ Tweet creation date """
            twitter_tweet.set_created_at(tweet_response.data.created_at)
            """ Tweet public metrics """
            tweet_public_metrics = tweet_response.data.public_metrics
            twitter_tweet.set_retweet_count(tweet_public_metrics["retweet_count"])
            twitter_tweet.set_reply_count(tweet_public_metrics["reply_count"])
            twitter_tweet.set_like_count(tweet_public_metrics["like_count"])
            twitter_tweet.set_quote_count(tweet_public_metrics["quote_count"])
            """================================================ USER ===================================================="""

            user_check = crud_twitter.read('twitter_user[author_id]', author_id)

            if not user_check:
                user = client.get_user(id=author_id, user_fields=["public_metrics", "created_at"])
                """ Author id"""
                twitter_user.set_author_id(author_id)
                """ Author account name and username  """
                twitter_user.set_name(user.data.name)
                twitter_user.set_username(user.data.username)
                """ Author account creation date """
                twitter_user.set_created_at(user.data.created_at)
                """ Author account public metrics """
                author_public_metrics = user.data.public_metrics
                twitter_user.set_followers(author_public_metrics['followers_count'])
                twitter_user.set_following(author_public_metrics['following_count'])
                twitter_user.set_tweet_count(author_public_metrics['tweet_count'])
                twitter_user.set_listed_count(author_public_metrics['listed_count'])

    except tweepy.TweepyException as error:
        if '429 Too Many Requests' in str(error):
            raise error
        else:
            print(error)

    return [twitter_tweet, twitter_user]


# Retrieve the number of real and fake followers
def retrieve_followers(username):
    url = constant.TWITTER_AUDIT + username

    print(url)

    html_content = requests.get(url, headers).text
    soup = BeautifulSoup(html_content, "lxml")
    number_real = soup.find('span', class_='real number')
    number_fake = soup.find('span', class_='fake number')

    if number_real is None and number_fake is None:
        raise 'Breaking'
    else:
        return [number_real.get_text().replace(',', ''), number_fake.get_text().replace(',', '')]
