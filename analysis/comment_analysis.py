from database import db_crud_analysis
from values import constant


# ANALYSE USERNAME COLUMN IN PROOF AND PARTICIPATION TABLES TO SEE THE FREQUENCY
def proof_participation_username_frequency(table, order):
    if table == 'proof':
        table_name = constant.DB_PROOF
    elif table == 'participation':
        table_name = constant.DB_PARTICIPATION
    else:
        print('1st argument should be proof or participation')
        return

    username_frequency = db_crud_analysis.retrieve_username_frequency(table_name)

    match order:
        case 'asc':
            sorted_by_username = sorted(username_frequency, key=lambda tup: tup[1])
        case 'desc':
            sorted_by_username = sorted(username_frequency, key=lambda tup: tup[1], reverse=True)

    return sorted_by_username


# ANALYSE CAMPAIGNS COLUMN IN PROOF TABLE TO SEE MOST POPULAR SOCIAL MEDIA SOURCES
def proof_campaigns_frequency(order):
    campaign_counter = [['Twitter', 0], ['Facebook', 0], ['Reddit', 0], ['YouTube', 0], ['LinkedIn', 0],
                        ['Instagram', 0],
                        ['Telegram', 0], ['TikTok', 0], ['Article', 0], ['Video', 0], ['Blog', 0]]

    campaigns = db_crud_analysis.retrieve_campaign_frequency()

    for campaign_set in campaigns:

        if "Twitter" in campaign_set[0]:
            campaign_counter[0][1] += 1
        if "Facebook" in campaign_set[0]:
            campaign_counter[1][1] += 1
        if "Reddit" in campaign_set[0]:
            campaign_counter[2][1] += 1
        if "YouTube" in campaign_set[0]:
            campaign_counter[3][1] += 1
        if "LinkedIn" in campaign_set[0]:
            campaign_counter[4][1] += 1
        if "Instagram" in campaign_set[0]:
            campaign_counter[5][1] += 1
        if "Telegram" in campaign_set[0]:
            campaign_counter[6][1] += 1
        if "TikTok" in campaign_set[0]:
            campaign_counter[7][1] += 1
        if "Article" in campaign_set[0]:
            campaign_counter[8][1] += 1
        if "Video" in campaign_set[0]:
            campaign_counter[9][1] += 1
        if "Blog" in campaign_set[0]:
            campaign_counter[10][1] += 1

    match order:
        case 'asc':
            sorted_by_frequency = sorted(campaign_counter, key=lambda tup: tup[1])
        case 'desc':
            sorted_by_frequency = sorted(campaign_counter, key=lambda tup: tup[1], reverse=True)

    return sorted_by_frequency

# IDEA: ANALYSE THE PROOF AND PARTICIPATION TABLES TO SEE HOW MANY COMMENTS ARE IN EACH (SORTED BY TOPIC_ID)


