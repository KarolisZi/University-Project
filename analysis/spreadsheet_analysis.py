from database import crud_analysis
from analysis import helper_functions
import matplotlib.pyplot as plt
import numpy as np

"""
================================================================================================

FUNCTIONS FOR GOOGLE SPREADSHEET RELATED DATA ANALYSIS

================================================================================================
"""


def spreadsheet_campaigns(order):
    data = crud_analysis.read('google_sheets[sheet_name]', [])

    campaign_counter = {'Twitter': 0, 'Facebook': 0, 'Reddit': 0, 'YouTube': 0, 'LinkedIn': 0,
                        'Instagram': 0, 'Telegram': 0, 'TikTok': 0, 'Article': 0, 'Video': 0, 'Blog': 0,
                        'Medium': 0, 'Discord': 0, 'Signature': 0, 'Translation': 0, 'Other': 0}

    for sheet_name in data:

        if "TWITTER" in sheet_name[0].upper():
            campaign_counter['Twitter'] += sheet_name[1]
        elif "FACEBOOK" in sheet_name[0].upper():
            campaign_counter['Facebook'] += sheet_name[1]
        elif "REDDIT" in sheet_name[0].upper():
            campaign_counter['Reddit'] += sheet_name[1]
        elif "YOUTUBE" in sheet_name[0].upper():
            campaign_counter['YouTube'] += sheet_name[1]
        elif "LINKEDIN" in sheet_name[0].upper():
            campaign_counter['LinkedIn'] += sheet_name[1]
        elif "INSTAGRAM" in sheet_name[0].upper():
            campaign_counter['Instagram'] += sheet_name[1]
        elif "TELEGRAM" in sheet_name[0].upper():
            campaign_counter['Telegram'] += sheet_name[1]
        elif "TIKTOK" in sheet_name[0].upper():
            campaign_counter['TikTok'] += sheet_name[1]
        elif "ARTICLE" in sheet_name[0].upper():
            campaign_counter['Article'] += sheet_name[1]
        elif "VIDEO" in sheet_name[0].upper():
            campaign_counter['Video'] += sheet_name[1]
        elif "BLOG" in sheet_name[0].upper():
            campaign_counter['Blog'] += sheet_name[1]
        elif "MEDIUM" in sheet_name[0].upper():
            campaign_counter['Medium'] += sheet_name[1]
        elif "DISCORD" in sheet_name[0].upper():
            campaign_counter['Discord'] += sheet_name[1]
        elif "SIGNATURE" in sheet_name[0].upper():
            campaign_counter['Signature'] += sheet_name[1]
        elif "TRANSLATION" in sheet_name[0].upper():
            campaign_counter['Translation'] += sheet_name[1]
        else:
            campaign_counter['Other'] += sheet_name[1]

    if order == 'asc':
        results = {k: v for k, v in sorted(campaign_counter.items(), key=lambda item: item[1], reverse=False)}
    elif order == 'desc':
        results = {k: v for k, v in sorted(campaign_counter.items(), key=lambda item: item[1], reverse=True)}

    # Creating horizontal graph
    fig, ax = plt.subplots(figsize=(9, 5))

    ax.barh(list(results.keys()), list(results.values()), color='lightgreen')
    helper_functions.labels('Number of entries', 10, 'Social media campaign', 10, 'Records per different types of campaigns', 14)
    helper_functions.grid_and_spines(ax)
    helper_functions.ticks(ax, 5, 5, results, False)

    plt.xticks(np.arange(0, max(list(results.values())), 50000))

    plt.yticks(list(results.keys()))

    for i in ax.patches:
        plt.text(i.get_width() + 0.1, i.get_y() + 0.20, str(round((i.get_width()), 2)), fontsize=10, color='black')

    name = 'plots/google_sheets.png'

    plt.savefig(name)
    plt.show()