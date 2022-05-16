from database import crud_analysis
import matplotlib.pyplot as plt
from values import constant
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

    for index, entry in enumerate(data):
        temp = entry[0].replace(u'\xa0', u' ')
        print(temp)
        clean_data.append(temp)

