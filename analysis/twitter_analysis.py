from textblob import TextBlob
from values import regex
import re
from wordcloud import WordCloud

from database import crud_analysis
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from analysis import helper_functions

"""
================================================================================================

FUNCTIONS FOR TWITTER RELATED DATA ANALYSIS

================================================================================================
"""


def user_account_age(order):
    times, results = crud_analysis.read('[twitter_user[created_at]', []), []

    now = datetime.now()

    for time in times:
        results.append((now - time[0]).days)

    average = int(sum(results) / len(results))
    print(results)
    print(average)
    median = results[int(len(results) / 2)]
    print(median)

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(results, [i for i in range(0, len(results))], color='purple')
    plt.xticks((np.arange(0, max(results), 400)))
    plt.yticks((np.arange(0, len(results), 100)))

    helper_functions.grid_and_spines(ax)
    if order == 'asc':
        helper_functions.ticks(ax, 5, 5, {}, False)
    elif order == 'desc':
        helper_functions.ticks(ax, 5, 5, {}, True)
    helper_functions.labels('Account age (days)', 10, 'User', 10, 'Account age of twitter users', 14)

    name = 'plots/twitter_user_account_age.png'
    plt.savefig(name)
    plt.show()


def tweet_count(order):
    data, tweets, tweet_sum = crud_analysis.read('[twitter_user[tweet_count]', []), [], 0
    tweet_sum_upper, tweet_sum_lower = [], []

    for entry in data:
        tweets.append(entry[0])
        if entry[0] > 30000:
            tweet_sum_upper.append(entry[0])
        else:
            tweet_sum_lower.append(entry[0])

    print(tweet_sum_lower)

    print('Average: %s' % (sum(tweets) / len(tweets)))
    print('Median: %s' % (tweets[int(len(tweets) / 2)]))
    print('Total: %s' % (sum(tweets)))


    """ TWEETS LOWER DISTRIBUTION """
    fig2, ax2 = plt.subplots(figsize=(9, 5))
    ax2.plot(tweet_sum_lower, [i for i in range(0, len(tweet_sum_lower))], color='purple')
    plt.xticks((np.arange(0, max(tweet_sum_lower), 2500)))
    plt.yticks((np.arange(0, len(tweet_sum_lower), 100)))
    helper_functions.grid_and_spines(ax2)
    if order == 'asc':
        helper_functions.ticks(ax2, 5, 5, {}, False)
    elif order == 'desc':
        helper_functions.ticks(ax2, 5, 5, {}, True)
    helper_functions.labels('Tweet count', 10, 'User', 10, 'User tweet count', 14)

    name = 'plots/twitter_user_tweet_count_lower.png'
    plt.savefig(name)
    plt.show()


def followers_following_real_fake(order):
    data = crud_analysis.read('[twitter_user[followers, following, real, fake]', [])
    followers, following, real, fake = [], [], [], []
    followers_upper, followers_lower = [], []
    following_upper, following_lower = [], []
    real_upper, real_lower = [], []
    fake_upper, fake_lower = [], []

    for entry in data:
        if entry[0] is not None:
            followers.append(entry[0])
            if entry[0] > 30000:
                followers_upper.append(entry[0])
            else:
                followers_lower.append(entry[0])
        if entry[1] is not None:
            following.append(entry[1])
            if entry[1] > 10000:
                following_upper.append(entry[1])
            else:
                following_lower.append(entry[1])
        if entry[2] is not None:
            real.append(entry[2])
            if entry[2] > 10000:
                real_upper.append(entry[2])
            else:
                real_lower.append(entry[2])
        if entry[3] is not None:
            fake.append(entry[3])
            if entry[3] > 200:
                fake_upper.append(entry[3])
            else:
                fake_lower.append(entry[3])

    followers.sort(), following.sort(), real.sort(), fake.sort()
    followers_upper.sort(), followers_lower.sort(), following_upper.sort(), following_lower.sort()
    real_upper.sort(), real_lower.sort(), fake_upper.sort(), fake_lower.sort()

    print(following_lower)


    print('Followers total: %s, average %s, minimum: %s, maximum: %s, median %s' % (
        sum(followers), int(sum(followers) / len(followers)), min(followers), max(followers),
        followers[int(len(followers) / 2)]))
    print('Following total: %s, average %s, minimum: %s, maximum: %s, median %s' % (
        sum(following), int(sum(following) / len(following)), min(following), max(following),
        following[int(len(following) / 2)]))
    print('Real followers total: %s, average %s, minimum: %s, maximum: %s, median %s' % (
        sum(real), int(sum(real) / len(real)), min(real), max(real), real[int(len(real) / 2)]))
    print('Fake followers total: %s, average %s, minimum: %s, maximum: %s, median %s' % (
        sum(fake), int(sum(fake) / len(fake)), min(fake), max(fake), fake[int(len(fake) / 2)]))

    for index, results in enumerate([followers_upper, followers_lower, following_upper, following_lower, real_upper, real_lower, fake_lower, fake_upper]):

        if index == 0:
            x_label, y_label, title, fname, progression_x, progression_y = 'Number of followers', 'Users', 'Number of followers per user (highest)', 'twitter_followers_highest', 1000000, 5
        elif index == 1:
            x_label, y_label, title, fname, progression_x, progression_y = 'Number of followers', 'Users', 'Number of followers per user (lowest)', 'twitter_followers_lowest', 5000, 100
        elif index == 2:
            x_label, y_label, title, fname, progression_x, progression_y = 'Number of users following', 'Users', 'Number of users following (highest)', 'twitter_following_highest', 5000, 25
        elif index == 3:
            x_label, y_label, title, fname, progression_x, progression_y = 'Number of users following', 'Users', 'Number of users following (lowest)', 'twitter_following_lowest', 1000, 100
        elif index == 4:
            x_label, y_label, title, fname, progression_x, progression_y = 'Number of real followers', 'Users', 'Number of real followers per user (highest)', 'twitter_real_followers_highest', 25000, 25
        elif index == 5:
            x_label, y_label, title, fname, progression_x, progression_y = 'Number of real followers', 'Users', 'Number of real followers per user (lowest)', 'twitter_real_followers_lowest', 1000, 100
        elif index == 6:
            x_label, y_label, title, fname, progression_x, progression_y = 'Number of fake followers', 'Users', 'Number of fake followers per user (lowest)', 'twitter_fake_followers_lowest', 20, 100
        elif index == 7:
            x_label, y_label, title, fname, progression_x, progression_y = 'Number of fake followers', 'Users', 'Number of fake followers per user (highest)', 'twitter_fake_followers_lowest', 1500, 5


        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(results, [i for i in range(0, len(results))], color='purple')
        plt.xticks((np.arange(0, max(results), progression_x)))
        plt.yticks((np.arange(0, len(results), progression_y)))
        helper_functions.grid_and_spines(ax)
        if order == 'asc':
            helper_functions.ticks(ax, 5, 5, {}, False)
        elif order == 'desc':
            helper_functions.ticks(ax, 5, 5, {}, True)
        helper_functions.labels(x_label, 10, y_label, 10, title, 14)

        name = 'plots/' + fname + '.png'
        plt.savefig(name)
        plt.show()


def sentiment_analysis():
    polarity, subjectivity = [], []
    negative, positive, neutral = 0, 0, 0

    data = crud_analysis.read('twitter_tweet[text]', [])
    text, allWords = [i[0] for i in data], ''

    for i in range(0, len(text)):
        text[i] = re.sub(r'@[A-Za-z0-9]+', '', text[i])
        text[i] = re.sub(r'#', ' ', text[i])
        text[i] = re.sub(r'https\:\/\/t.co\/\w+', '', text[i])
        text[i] = re.sub(r'https?:\/\/\S+', '', text[i])
        text[i] = text[i].replace('  ', ' ')
        text[i] = text[i].replace('.', ' ')
        text[i] = text[i].replace(',', ' ')
        text[i] = text[i].replace('\n', ' ')
        text[i] = regex.emoji_pattern.sub(' ', text[i])

    for string in text:
        words = string.split(' ')
        for word in words:
            if word != ' ' and word != '' and word is not None:
                allWords += word + ' '

    # Polarity analysis
    for entry in text:
        pol = TextBlob(entry).sentiment.polarity
        polarity.append(pol)
        if pol > 0:
            positive += 1
        elif pol < 0:
            negative += 1
        else:
            neutral += 1
    polarity.sort()

    # Subjectivity analysis
    for entry in text:
        subjectivity.append(TextBlob(entry).sentiment.subjectivity)
    subjectivity.sort()

    wordCloud = WordCloud(collocations=False, background_color='white').generate(allWords)
    plt.imshow(wordCloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

    # POLARITY PLOT
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot([i for i in range(0, len(polarity))], polarity, color='orange')
    helper_functions.grid_and_spines(ax)
    helper_functions.ticks(ax, 5, 5, {}, False)
    helper_functions.labels('Tweet', 10, 'Polarity', 10, 'Tweet polarity distribution', 14)
    plt.xticks(np.arange(0, len(polarity), 10000))
    plt.yticks(np.arange(-1, 1.1, 0.1))
    name = 'plots/tweets_polarity.png'
    plt.savefig(name)
    plt.show()

    fig2, ax2 = plt.subplots(figsize=(9, 5))
    ax2.barh(['Neutral', 'Positive', 'Negative'], [neutral, positive, negative], color='orange')
    helper_functions.grid_and_spines(ax2)
    helper_functions.ticks(ax2, 5, 5, {}, False)
    helper_functions.labels('Count', 10, 'Tweet polarity', 10, 'Tweet polarity distribution', 14)

    # Add annotation to bars
    for i in ax2.patches:
        plt.text(i.get_width() + 1.5, i.get_y() + 0.35, str(round((i.get_width()), 2)), fontsize=10, color='orange')

    print('Negative: %s, Positive %s, Neutral: %s' % (negative, positive, neutral))
    name = 'plots/tweets_polarity_pnn.png'
    plt.savefig(name)
    plt.show()

    # SUBJECTIVITY PLOT
    fig3, ax3 = plt.subplots(figsize=(9, 5))
    ax3.plot([i for i in range(0, len(subjectivity))], subjectivity, color='orange')
    helper_functions.grid_and_spines(ax3)
    helper_functions.ticks(ax3, 5, 5, {}, False)
    helper_functions.labels('Tweet', 10, 'Subjectivity', 10, 'Tweet subjectivity distribution', 14)
    plt.xticks(np.arange(0, len(subjectivity), 10000))
    plt.yticks(np.arange(0, 1, 0.1))
    name = 'plots/tweets_subjectivity.png'
    plt.savefig(name)
    plt.show()


# TOP 10, BOTTOM 10
def tweet_likes_comments_retweets():
    data = crud_analysis.read('twitter_tweet[reply_count, retweet_count, like_count]', [])
    replies, retweets, likes = [], [], []

    for entry in data:
        replies.append(entry[0])
        retweets.append(entry[1])
        likes.append(entry[2])


    print('Replies total: %s, average %s, minimum: %s, maximum: %s, median %s' % (
            sum(replies), sum(replies) / len(replies), min(replies), max(replies),
            replies[int(len(replies) / 2)]))
    print('Retweets total: %s, average %s, minimum: %s, maximum: %s, median %s' % (
        sum(retweets), sum(retweets) / len(retweets), min(retweets), max(retweets),
        retweets[int(len(retweets) / 2)]))
    print('Likes total: %s, average %s, minimum: %s, maximum: %s, median %s' % (
        sum(likes), sum(likes) / len(likes), min(likes), max(likes),
        likes[int(len(likes) / 2)]))



    """ REPLIES """
    replies_ascending, replies_descending = {}, {}

    replies.sort()
    for entry in replies:

        if entry not in replies_ascending:
            replies_ascending[entry] = 1
        elif entry in replies_ascending:
            replies_ascending[entry] += 1
        if len(replies_ascending) > 10:
            replies_ascending.pop(entry)
            break

    replies.sort(reverse=True)
    for i in range(0, 10):
        key = 'user_%s' % str(i + 1)
        replies_descending[key] = replies[i]
    """ LIKES """
    likes_ascending, likes_descending = {}, {}

    likes.sort()
    for entry in likes:

        if entry not in likes_ascending:
            likes_ascending[entry] = 1
        elif entry in likes_ascending:
            likes_ascending[entry] += 1
        if len(likes_ascending) > 10:
            likes_ascending.pop(entry)
            break

    likes.sort(reverse=True)
    for i in range(0, 10):
        key = 'user_%s' % str(i + 1)
        likes_descending[key] = likes[i]

    """ RETWEETS """
    retweets_ascending, retweets_descending = {}, {}

    retweets.sort()
    for entry in retweets:

        if entry not in retweets_ascending:
            retweets_ascending[entry] = 1
        elif entry in retweets_ascending:
            retweets_ascending[entry] += 1
        if len(retweets_ascending) > 10:
            retweets_ascending.pop(entry)
            break

    retweets.sort(reverse=True)

    for i in range(0, 10):
        key = 'user_%s' % str(i + 1)
        retweets_descending[key] = retweets[i]

    # tweet_replies(replies_ascending, replies_descending)
    # tweet_likes(likes_ascending, likes_descending)
    tweet_retweets(retweets_ascending, retweets_descending)


def tweet_replies(ascending, descending):
    """ ASCENDING """
    fig_asc, ax_asc = plt.subplots(figsize=(9, 5))
    ax_asc.barh(list(ascending.keys()), list(ascending.values()), color='orange')
    helper_functions.grid_and_spines(ax_asc)
    helper_functions.ticks(ax_asc, 5, 5, {}, True)
    helper_functions.labels('Number of replies on tweet', 10, 'Number of tweets', 10, 'Lowest replies distribution', 14)
    plt.yticks(list(ascending.keys()))
    for i in ax_asc.patches:
        plt.text(i.get_width() + 1, i.get_y() + 0.5, str(round((i.get_width()), 2)), fontsize=10, color='black')
    name = 'plots/tweets_replies_asc.png'
    plt.savefig(name)
    plt.show()

    """ DESCENDING """
    fig_desc, ax_desc = plt.subplots(figsize=(9, 5))
    ax_desc.barh(list(descending.keys()), list(descending.values()), color='orange')
    helper_functions.grid_and_spines(ax_desc)
    helper_functions.ticks(ax_desc, 5, 5, {}, True)
    helper_functions.labels('User', 10, 'Number of replies on a tweet', 10, 'Highest replies distribution', 14)
    for i in ax_desc.patches:
        plt.text(i.get_width() + 1, i.get_y() + 0.5, str(round((i.get_width()), 2)), fontsize=10, color='black')
    name = 'plots/tweets_replies_desc.png'
    plt.savefig(name)
    plt.show()
    """============================================================================="""


def tweet_retweets(ascending, descending):
    """ ASCENDING """
    fig_asc, ax_asc = plt.subplots(figsize=(9, 5))
    ax_asc.barh(list(ascending.keys()), list(ascending.values()), color='orange')
    helper_functions.grid_and_spines(ax_asc)
    helper_functions.ticks(ax_asc, 5, 5, {}, True)
    helper_functions.labels('Number of retweets on a tweet', 10, 'Number of tweets', 10, 'Lowest retweet distribution',
                            14)
    plt.yticks(list(ascending.keys()))
    for i in ax_asc.patches:
        plt.text(i.get_width() + 1, i.get_y() + 0.5, str(round((i.get_width()), 2)), fontsize=10, color='black')
    name = 'plots/tweets_retweets_asc.png'
    plt.savefig(name)
    plt.show()

    """ DESCENDING """
    fig_desc, ax_desc = plt.subplots(figsize=(9, 5))
    ax_desc.barh(list(descending.keys()), list(descending.values()), color='orange')
    helper_functions.grid_and_spines(ax_desc)
    helper_functions.ticks(ax_desc, 5, 5, {}, True)
    helper_functions.labels('User', 10, 'Number of retweets on a tweet', 10, 'Highest retweet distribution', 14)
    for i in ax_desc.patches:
        plt.text(i.get_width() + 1, i.get_y() + 0.5, str(round((i.get_width()), 2)), fontsize=10, color='black')
    name = 'plots/tweets_retweets_desc.png'
    plt.savefig(name)
    plt.show()
    """============================================================================="""


def tweet_likes(ascending, descending):
    """ ASCENDING """
    fig_asc, ax_asc = plt.subplots(figsize=(9, 5))
    ax_asc.barh(list(ascending.keys()), list(ascending.values()), color='orange')
    helper_functions.grid_and_spines(ax_asc)
    helper_functions.ticks(ax_asc, 5, 5, {}, True)
    helper_functions.labels('Number of likes on tweet', 10, 'Number of tweets', 10, 'Lowest likes distribution', 14)
    plt.yticks(list(ascending.keys()))
    for i in ax_asc.patches:
        plt.text(i.get_width() + 1, i.get_y() + 0.5, str(round((i.get_width()), 2)), fontsize=10, color='black')
    name = 'plots/tweets_likes_asc.png'
    plt.savefig(name)
    plt.show()

    """ DESCENDING """
    fig_desc, ax_desc = plt.subplots(figsize=(9, 5))
    ax_desc.barh(list(descending.keys()), list(descending.values()), color='orange')
    helper_functions.grid_and_spines(ax_desc)
    helper_functions.ticks(ax_desc, 5, 5, {}, True)
    helper_functions.labels('User', 10, 'Number of likes on a tweet', 10, 'Highest likes distribution', 14)
    for i in ax_desc.patches:
        plt.text(i.get_width() + 1, i.get_y() + 0.5, str(round((i.get_width()), 2)), fontsize=10, color='black')
    name = 'plots/tweets_likes_desc.png'
    plt.savefig(name)
    plt.show()
    """============================================================================="""
