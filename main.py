from control import control_topic
from control import control_comments
from control import control_sheets
from control import control_author_images
from control import control_twitter
from analysis import comment_analysis
from analysis import topic_analysis
from analysis import spreadsheet_analysis
from analysis import twitter_analysis
from database import create_table


if __name__ == '__main__':
    """CREATE ALL DATABASE TABLES"""
    # create_table.create_all_tables()

    """ TOPIC - create a database table from the home page information """
    # FIRST ARGUMENT (TOPICS): 'one', 'all', 'update', '[page_id_2, page_id_3,...]', 'yyyy/mm/dd - yyyy/mm/dd' or 'yyyy/mm/dd'
    # control_topic.populate_database('update')

    """ COMMENTS - create a database table from the comment section"""
    # FIRST ARGUMENT (TOPICS): 'one', 'all', 'update', '[id, id_2, id_3, ...]', 'yyyy/mm/dd - yyyy/mm/dd' or 'yyyy/mm/dd'
    # SECOND ARGUMENT (COMMENTS): 'all' or number
    # THIRD ARGUMENT (REVERSE): True, False
    # FOURTH ARGUMENT (TABLES): ['participation', 'proof', 'author']
    # control_comments.populate_database('all', 'all', False, ['participation', 'proof', 'author'])

    """ AUTHOR IMAGES - extract data from author images """
    # "one" - extract data from the first entry in the topic database
    # "all_new" - extracts only the entries that have not been extracted before
    # "all_new_failed" - extracts the failed entries
    # control_author_images.populate_database_author('all_new')

    """ GOOGLE SHEETS - create a database table from Google sheets """
    # "all" - create records from all topics
    # "any_number" - creates records of that many topics. I.e. number 3 would create records from 3 topics
    # control_sheets.populate_database_sheets("all")

    """ TWITTER - create database records from twitter tweets"""
    # control_twitter.populate_database_twitter()
    # control_twitter.analyse_followers()

    """COMMENT ANALYSIS"""
    # Analyse how many comments are made by the same user in proof/participation tables
    # comment_analysis.proof_participation_username_frequency('participation', 'asc', 10)
    # Analyse how often a social media campaign is detected in proof table
    # comment_analysis.proof_participation_campaigns_frequency('participation', 'asc')
    # Analyse how many replies are there per topic in proof/participation tables
    # comment_analysis.replies_max_min('participation')
    # Analyse participation comments social media URL's
    # comment_analysis.participation_urls('asc')

    """TOPIC ANALYSIS"""
    # Analyse when topics were seen active for the last time or were created
    # topic_analysis.topic_creation_last_post('month', 'last_seen_active')
    # Analyse how many posts are made by the same author
    # topic_analysis.author_frequency('asc', 10)
    # Calculate the topic lifespans
    # topic_analysis.topic_lifespan('desc')
    # Reward allocation
    topic_analysis.reward_allocation()

    """SHEET ANALYSIS"""
    # spreadsheet_analysis.spreadsheet_campaigns('asc')

    """TWITTER ANALYSIS"""
    # twitter_analysis.user_account_age('asc')
    # twitter_analysis.tweet_count('asc')
    # twitter_analysis.followers_following_real_fake('asc')
    # twitter_analysis.sentiment_analysis()
    # twitter_analysis.tweet_likes_comments_retweets()







