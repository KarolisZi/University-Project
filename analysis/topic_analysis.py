from database import crud_analysis
import matplotlib.pyplot as plt
from values import constant
from values import regex
from analysis import helper_functions
import numpy as np

"""
================================================================================================

FUNCTIONS FOR TOPIC (THREAD) RELATED DATA ANALYSIS

================================================================================================
"""


def author_frequency(order, number_of_entries):
    username_frequency = crud_analysis.read('topic[author_frequency]', order)

    amount_freq = {}

    if order == 'asc':
        x_label = 'Number of users'
        y_label = 'Number of topics created'
        title = 'The least frequent post authors'
        for entry in username_frequency:
            if not entry[1] in amount_freq:
                amount_freq[entry[1]] = 1
            elif entry[1] in amount_freq:
                amount_freq[entry[1]] += 1
            if len(amount_freq) > number_of_entries:
                # amount_freq.pop(entry[1])
                break
        # Add strings with 0 data for missing values
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
        x_label = 'Number of posts'
        y_label = 'User'
        title = 'The most frequent post authors'
        for i in range(0, number_of_entries):
            key = 'user_%s' % str(i + 1)
            amount_freq[key] = username_frequency[i][1]

    # Create the figure
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(list(amount_freq.keys()), list(amount_freq.values()), color='lightblue')

    helper_functions.grid_and_spines(ax)
    helper_functions.labels(x_label, 10, y_label, 10, title, 16)
    helper_functions.ticks(ax, 5, 5, amount_freq, True)

    for i in ax.patches:
        plt.text(i.get_width() + 0.1, i.get_y() + 0.5, str(round((i.get_width()), 2)), fontsize=10, color='black')

    name = 'plots/topic_author_frequency_' + order + '.png'

    plt.savefig(name)
    plt.show()


def topic_creation_last_post(scale_mode, data_mode):
    match data_mode:
        case 'created':
            title = 'Number of topics created during the period'
            xlabel = 'Number of topics'
            dates = crud_analysis.read('topic[creation_time]', [])
        case 'last_seen_active':
            title = 'Number of topics last seen active during the period'
            xlabel = 'Number of topics'
            dates = crud_analysis.read('topic[last_post_time]', [])

    results = {}

    for creation_date in dates:

        if creation_date[0]:

            match scale_mode:
                case "year":
                    ylabel = "Year"
                    year = creation_date[0].year
                    if year in results:
                        results[year] += 1
                    else:
                        results[year] = 1
                case 'month':
                    ylabel = "Year / month"
                    year = str(creation_date[0].year)
                    month = str(creation_date[0].month)

                    if int(month) < 10:
                        month = '0' + month
                    year_month = year + '/' + month
                    if year_month in results:
                        results[year_month] += 1
                    else:
                        results[year_month] = 1

    if scale_mode == 'year':
        max, min = -9999999999, 9999999999
        for key in results.keys():
            if key > max:
                max = key
            if key < min:
                min = key

        for i in range(min, max):
            if not i in results:
                results[i] = 0

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(list(results.keys()), list(results.values()), color='lightblue')

    helper_functions.grid_and_spines(ax)
    helper_functions.ticks(ax, -5, 10, results, True)
    helper_functions.labels(xlabel, 10, ylabel, 10, title, 16)

    # Add annotation to bars
    for i in ax.patches:
        plt.text(i.get_width() + 1, i.get_y() + 0.65, str(round((i.get_width()), 2)), fontsize=10, color='black')

    name = 'plots/' + constant.DB_TOPIC + '_' + data_mode + '_' + scale_mode + '.png'

    plt.savefig(name)

    plt.show()


def topic_lifespan(mode):
    data = crud_analysis.read('topic[last_post,creation]', [])

    points, tics = [], []
    points_sorted = {}

    for index, date in enumerate(data):
        if data[0] is not None and date[1] is not None:
            td = date[0] - date[1]
            points.append(td.days)
            tics.append(index)

    points.sort()
    lifespan_sum = 0
    for entry in points:
        lifespan_sum += entry
        if not entry in points_sorted:
            points_sorted[entry] = 1
        elif entry in points_sorted:
            points_sorted[entry] += 1

    print(lifespan_sum / len(data))

    print(points_sorted)

    x_label = 'Topic number'
    y_label = 'Topic lifespan (days)'
    title = 'The lifespan distribution of topics seen active from 2021/01/01'

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(tics, points, color='lightblue')

    helper_functions.grid_and_spines(ax)
    if mode == 'asc':
        reverse = True
    elif mode == 'desc':
        reverse = False
    helper_functions.ticks(ax, 5, 5, {}, reverse)
    plt.xticks(np.arange(min(tics), max(tics), 100))
    plt.yticks(np.arange(min(points) + 1, max(points), 150))
    helper_functions.labels(x_label, 10, y_label, 10, title, 14)

    name = 'plots/topic_lifespan_distribution.png'
    plt.savefig(name)
    plt.show()


def reward_allocation():
    data, clean_data = crud_analysis.read('topic[reward_allocation]', []), []

    campaign_counter = {'Twitter': [], 'Facebook': [], 'Reddit': [], 'YouTube': [], 'LinkedIn': [],
                        'Instagram': [], 'Telegram': [], 'TikTok': [], 'Article': [], 'Video': [], 'Blog': [],
                        'Medium': [], 'Discord': [], 'Signature': [], 'Translation': [], 'Other': []}

    for index, entry in enumerate(data):
        temp = entry[0].replace(u'\xa0', u' ')
        temp = temp.replace('{', '')
        temp = temp.replace('{', '')
        temp = temp.replace('"', '')
        temp = temp.replace('\'', '')
        words = temp.split(',')
        for word in words:
            percentage = regex.percentage.search(word)
            if 'TWITTER' in word.upper():
                if percentage:
                    campaign_counter['Twitter'].append(percentage.group(0))
            elif "FACEBOOK" in word.upper():
                if percentage:
                    campaign_counter['Facebook'].append(percentage.group(0))
            elif "REDDIT" in word.upper():
                if percentage:
                    campaign_counter['Reddit'].append(percentage.group(0))
            elif "YOUTUBE" in word.upper():
                if percentage:
                    campaign_counter['YouTube'].append(percentage.group(0))
            elif "LINKEDIN" in word.upper():
                if percentage:
                    campaign_counter['LinkedIn'].append(percentage.group(0))
            elif "INSTAGRAM" in word.upper():
                if percentage:
                    campaign_counter['Instagram'].append(percentage.group(0))
            elif "TELEGRAM" in word.upper():
                if percentage:
                    campaign_counter['Telegram'].append(percentage.group(0))
            elif "TIKTOK" in word.upper():
                if percentage:
                    campaign_counter['TikTok'].append(percentage.group(0))
            elif "ARTICLE" in word.upper():
                if percentage:
                    campaign_counter['Article'].append(percentage.group(0))
            elif "VIDEO" in word.upper():
                if percentage:
                    campaign_counter['Video'].append(percentage.group(0))
            elif "BLOG" in word.upper():
                if percentage:
                    campaign_counter['Blog'].append(percentage.group(0))
            elif "MEDIUM" in word.upper():
                if percentage:
                    campaign_counter['Medium'].append(percentage.group(0))
            elif "DISCORD" in word.upper():
                if percentage:
                    campaign_counter['Discord'].append(percentage.group(0))
            elif "SIGNATURE" in word.upper():
                if percentage:
                    campaign_counter['Signature'].append(percentage.group(0))
            elif "TRANSLATION" in word.upper():
                if percentage:
                    campaign_counter['Translation'].append(percentage.group(0))
            else:
                if percentage:
                    campaign_counter['Other'].append(percentage.group(0))

    temp = []
    for entry in campaign_counter['Twitter']:
        temp.append(int(entry.replace('%', '')))
    temp.sort()
    campaign_counter['Twitter'] = temp

    temp = []
    for entry in campaign_counter['Facebook']:
        temp.append(int(entry.replace('%', '')))
    temp.sort()
    campaign_counter['Facebook'] = temp

    temp = []
    for entry in campaign_counter['Reddit']:
        temp.append(int(entry.replace('%', '')))
    temp.sort()
    campaign_counter['Reddit'] = temp

    temp = []
    for entry in campaign_counter['YouTube']:
        temp.append(int(entry.replace('%', '')))
    temp.sort()
    campaign_counter['YouTube'] = temp

    temp = []
    for entry in campaign_counter['LinkedIn']:
        temp.append(int(entry.replace('%', '')))
    temp.sort()
    campaign_counter['LinkedIn'] = temp

    temp = []
    for entry in campaign_counter['Instagram']:
        temp.append(int(entry.replace('%', '')))
    temp.sort()
    campaign_counter['Instagram'] = temp

    temp = []
    for entry in campaign_counter['Telegram']:
        temp.append(int(entry.replace('%', '')))
    temp.sort()
    campaign_counter['Telegram'] = temp

    temp = []
    for entry in campaign_counter['TikTok']:
        temp.append(int(entry.replace('%', '')))
    temp.sort()
    campaign_counter['TikTok'] = temp

    temp = []
    for entry in campaign_counter['Article']:
        temp.append(int(entry.replace('%', '')))
    temp.sort()
    campaign_counter['Article'] = temp

    temp = []
    for entry in campaign_counter['Video']:
        temp.append(int(entry.replace('%', '')))
    temp.sort()
    campaign_counter['Video'] = temp

    temp = []
    for entry in campaign_counter['Blog']:
        temp.append(int(entry.replace('%', '')))
    temp.sort()
    campaign_counter['Blog'] = temp

    temp = []
    for entry in campaign_counter['Medium']:
        temp.append(int(entry.replace('%', '')))
    temp.sort()
    campaign_counter['Medium'] = temp

    temp = []
    for entry in campaign_counter['Discord']:
        temp.append(int(entry.replace('%', '')))
    temp.sort()
    campaign_counter['Discord'] = temp

    temp = []
    for entry in campaign_counter['Signature']:
        temp.append(int(entry.replace('%', '')))
    temp.sort()
    campaign_counter['Signature'] = temp

    temp = []
    for entry in campaign_counter['Translation']:
        temp.append(int(entry.replace('%', '')))
    temp.sort()
    campaign_counter['Translation'] = temp

    temp = []
    for entry in campaign_counter['Other']:
        temp.append(int(entry.replace('%', '')))
    temp.sort()
    campaign_counter['Other'] = temp

    # Highest, Lowest, Median, Average, Length

    print('Twitter: %s, %s, %s, %s, %s' % (max(campaign_counter['Twitter']), min(campaign_counter['Twitter']), campaign_counter['Twitter'][int(len(campaign_counter['Twitter'])/2)], round(sum(campaign_counter['Twitter'])/len(campaign_counter['Twitter']), 2), len(campaign_counter['Twitter'])))
    print('Facebook: %s, %s, %s, %s, %s' % (max(campaign_counter['Facebook']), min(campaign_counter['Facebook']), campaign_counter['Facebook'][int(len(campaign_counter['Facebook'])/2)], round(sum(campaign_counter['Facebook'])/len(campaign_counter['Facebook']), 2), len(campaign_counter['Facebook'])))
    print('Reddit: %s, %s, %s, %s, %s' % (max(campaign_counter['Reddit']), min(campaign_counter['Reddit']), campaign_counter['Reddit'][int(len(campaign_counter['Reddit'])/2)], round(sum(campaign_counter['Reddit'])/len(campaign_counter['Reddit']), 2), len(campaign_counter['Reddit'])))
    print('YouTube: %s, %s, %s, %s, %s' % (max(campaign_counter['YouTube']), min(campaign_counter['YouTube']), campaign_counter['YouTube'][int(len(campaign_counter['YouTube'])/2)], round(sum(campaign_counter['YouTube'])/len(campaign_counter['YouTube']), 2), len(campaign_counter['YouTube'])))
    print('LinkedIn: %s, %s, %s, %s, %s' % (max(campaign_counter['LinkedIn']), min(campaign_counter['LinkedIn']), campaign_counter['LinkedIn'][int(len(campaign_counter['LinkedIn'])/2)], round(sum(campaign_counter['LinkedIn'])/len(campaign_counter['LinkedIn']), 2), len(campaign_counter['LinkedIn'])))
    print('Instagram: %s, %s, %s, %s, %s' % (max(campaign_counter['Instagram']), min(campaign_counter['Instagram']), campaign_counter['Instagram'][int(len(campaign_counter['Instagram'])/2)], round(sum(campaign_counter['Instagram'])/len(campaign_counter['Instagram']), 2), len(campaign_counter['Instagram'])))
    print('TikTok: %s, %s, %s, %s, %s' % (max(campaign_counter['TikTok']), min(campaign_counter['TikTok']), campaign_counter['TikTok'][int(len(campaign_counter['TikTok'])/2)], round(sum(campaign_counter['TikTok'])/len(campaign_counter['TikTok']), 2), len(campaign_counter['TikTok'])))
    print('Article: %s, %s, %s, %s, %s' % (max(campaign_counter['Article']), min(campaign_counter['Article']), campaign_counter['Article'][int(len(campaign_counter['Article'])/2)], round(sum(campaign_counter['Article'])/len(campaign_counter['Article']), 2), len(campaign_counter['Article'])))
    print('Video: %s, %s, %s, %s, %s' % (max(campaign_counter['Video']), min(campaign_counter['Video']), campaign_counter['Video'][int(len(campaign_counter['Video'])/2)], round(sum(campaign_counter['Video'])/len(campaign_counter['Video']), 2), len(campaign_counter['Video'])))
    print('Blog: %s, %s, %s, %s, %s' % (max(campaign_counter['Blog']), min(campaign_counter['Blog']), campaign_counter['Blog'][int(len(campaign_counter['Blog'])/2)], round(sum(campaign_counter['Blog'])/len(campaign_counter['Blog']), 2), len(campaign_counter['Blog'])))
    print('Medium: %s, %s, %s, %s, %s' % (max(campaign_counter['Medium']), min(campaign_counter['Medium']), campaign_counter['Medium'][int(len(campaign_counter['Medium'])/2)], round(sum(campaign_counter['Medium'])/len(campaign_counter['Medium']), 2), len(campaign_counter['Medium'])))
    print('Discord: %s, %s, %s, %s, %s' % (max(campaign_counter['Discord']), min(campaign_counter['Discord']), campaign_counter['Discord'][int(len(campaign_counter['Discord'])/2)], round(sum(campaign_counter['Discord'])/len(campaign_counter['Discord']), 2), len(campaign_counter['Discord'])))
    print('Signature: %s, %s, %s, %s, %s' % (max(campaign_counter['Signature']), min(campaign_counter['Signature']), campaign_counter['Signature'][int(len(campaign_counter['Signature'])/2)], round(sum(campaign_counter['Signature'])/len(campaign_counter['Signature']), 2), len(campaign_counter['Signature'])))
    print('Translation: %s, %s, %s, %s, %s' % (max(campaign_counter['Translation']), min(campaign_counter['Translation']), campaign_counter['Translation'][int(len(campaign_counter['Translation'])/2)], round(sum(campaign_counter['Translation'])/len(campaign_counter['Translation']), 2), len(campaign_counter['Translation'])))
    print('Other: %s, %s, %s, %s, %s' % (max(campaign_counter['Other']), min(campaign_counter['Other']), campaign_counter['Other'][int(len(campaign_counter['Other'])/2)], round(sum(campaign_counter['Other'])/len(campaign_counter['Other']), 2), len(campaign_counter['Other'])))
