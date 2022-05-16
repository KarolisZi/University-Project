import numpy as np

from database import crud_analysis
from values import constant
import matplotlib.pyplot as plt
from analysis import helper_functions

"""
================================================================================================

FUNCTIONS FOR COMMENT RELATED DATA ANALYSIS

================================================================================================
"""


def proof_participation_username_frequency(table, order, number_of_entries):
    amount_freq = {}

    if table == 'proof':
        table_name = constant.DB_PROOF
    elif table == 'participation':
        table_name = constant.DB_PARTICIPATION

    username_frequency = crud_analysis.read('proof/participation[username_frequency]', [table_name, order])

    if order == 'asc':
        mode = 'lowest'
        title = 'User comment frequency distribution (lowest) in %s' % table_name
        x_label, y_label = 'Number users', 'Number of replies'

        # Calculate the frequency
        for entry in username_frequency:
            number_of_proof = entry[1]

            if not number_of_proof in amount_freq:
                amount_freq[number_of_proof] = 1
            elif number_of_proof in amount_freq:
                amount_freq[number_of_proof] += 1
            if len(amount_freq) >= number_of_entries + 1:
                amount_freq.pop(number_of_proof)
                break
        max, min = -9999999999, 9999999999
        for key in amount_freq.keys():
            if key > max:
                max = key
            if key < min:
                min = key

        for i in range(min, max):
            if not i in amount_freq:
                amount_freq[i] = 0
    elif order == 'desc':
        mode = 'highest'
        title = 'Distribution and frequency of comments (highest) in %s' % table_name
        x_label, y_label = 'Number of replies', 'User'
        for i in range(0, number_of_entries):
            key = 'user_%s' % str(i + 1)
            amount_freq[key] = username_frequency[i][1]

    # Creating the plot
    fig, ax = plt.subplots(figsize=(8, 5))
    # Creating the horizontal bar
    ax.barh(list(amount_freq.keys()), list(amount_freq.values()), color='lightgreen')
    helper_functions.grid_and_spines(ax)
    helper_functions.ticks(ax, 5, 5, amount_freq, True)
    helper_functions.labels(x_label, 10, y_label, 10, title, 14)

    for i in ax.patches:
        plt.text(i.get_width() + 0.1, i.get_y() + 0.5, str(round((i.get_width()), 2)), fontsize=10, color='black')

    name = 'plots/' + table_name + '_user_reply_frequency_' + mode + '.png'

    plt.savefig(name)
    plt.show()


# ANALYSE CAMPAIGNS COLUMN IN PROOF TABLE TO SEE MOST POPULAR SOCIAL MEDIA SOURCES
def proof_participation_campaigns_frequency(table, order):
    if table == 'participation':
        title = 'Campaign participation in participation comments'
        campaign_sets = crud_analysis.read('participation[participation]', [])
    elif table == 'proof':
        title = 'Campaign participation in proof comments'
        campaign_sets = crud_analysis.read('proof[campaigns]', [])

    results = {}

    sum = 0

    for campaign_set in campaign_sets:

        for campaign in campaign_set[0].replace('{', '').replace('}', '').split(','):

            if not campaign in results and campaign != '':
                results[campaign] = 1
                sum += 1
            elif campaign in results and campaign != '':
                sum += 1
                results[campaign] += 1

    if order == 'asc':
        results = {k: v for k, v in sorted(results.items(), key=lambda item: item[1], reverse=False)}
    elif order == 'desc':
        results = {k: v for k, v in sorted(results.items(), key=lambda item: item[1], reverse=True)}

    # Creating horizontal graph
    fig, ax = plt.subplots(figsize=(9, 5))

    ax.barh(list(results.keys()), list(results.values()), color='lightgreen')
    helper_functions.labels('Frequency', 10, 'Social media platform', 10, title, 14)
    helper_functions.grid_and_spines(ax)
    helper_functions.ticks(ax, 5, 5, results, False)

    plt.xticks(np.arange(0, max(list(results.values())), 100000))

    plt.yticks(list(results.keys()))

    for i in ax.patches:
        plt.text(i.get_width() + 0.1, i.get_y() + 0.20, str(round((i.get_width()), 2)), fontsize=10, color='black')

    name = 'plots/campaigns_' + table + '.png'

    plt.savefig(name)
    plt.show()


def analyse_twitter_post_urls():
    entries = crud_analysis.read('participation[twitter_links]', [])

    return entries


def replies_max_min(mode):
    entries = crud_analysis.read('proof/participation[count]', mode)

    x_label = 'Topic number'
    y_label = 'Number of replies in topic'
    title = 'Number of replies per topic in %s table' % mode

    points, tics = [], []

    for index, entry in enumerate(entries):
        points.append(entry[1])
        tics.append(index)

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(tics, points, color='lightgreen')

    helper_functions.grid_and_spines(ax)
    helper_functions.ticks(ax, 5, 5, {}, False)
    if mode == 'partcipation':
        plt.yticks(np.arange(min(points) - 1, max(points), 1500))
        plt.xticks(np.arange(min(tics), max(tics), 50))
    if mode == 'proof':
        plt.yticks(np.arange(min(points) - 1, max(points), 500))
        plt.xticks(np.arange(min(tics), max(tics), 75))
    helper_functions.labels(x_label, 10, y_label, 10, title, 14)

    name = 'plots/campaigns_comments_' + mode + '_per_topic.png'
    plt.savefig(name)
    plt.show()


def participation_urls(order):

    platforms = ['twitter', 'facebook', 'instagram', 'telegram', 'reddit', 'other']

    platform_frequency = {'twitter': 0, 'facebook': 0, 'instagram': 0, 'telegram': 0, 'reddit': 0, 'other': 0, }

    for platform in platforms:
        entries = crud_analysis.read('participation[links]', platform)
        for entry in entries:
            platform_frequency[platform] += len(entry[0])

    if order == 'asc':
        results = {k: v for k, v in sorted(platform_frequency.items(), key=lambda item: item[1], reverse=False)}
    elif order == 'desc':
        results = {k: v for k, v in sorted(platform_frequency.items(), key=lambda item: item[1], reverse=True)}

    # Creating horizontal graph
    fig, ax = plt.subplots(figsize=(9, 5))

    ax.barh(list(results.keys()), list(results.values()), color='lightgreen')
    helper_functions.labels('Number of links', 10, 'Social media platform', 10, 'Collected social media links count', 14)
    helper_functions.grid_and_spines(ax)
    helper_functions.ticks(ax, 5, 5, results, False)

    plt.xticks(np.arange(min(list(results.values())), max(list(results.values())), 1000000))

    plt.yticks(list(results.keys()))

    for i in ax.patches:
        plt.text(i.get_width() + 0.1, i.get_y() + 0.20, str(round((i.get_width()), 2)), fontsize=10, color='black')

    name = 'plots/participation_links.png'

    plt.savefig(name)
    plt.show()
