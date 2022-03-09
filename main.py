from control import control
from web_scraping import scrape_forum_post_comments

# Run testing
if __name__ == '__main__':

    # Create a database table from the home page information
    # "one" - one home page of posts
    # "all" - all post pages
    #control.populate_database_main_page("one")

    # Create a database table from the comment section
    # "one_one" - one post, once comment page
    # "one_all" - one post, all comment pages
    # "all_one" - all pages, one comment page
    # "all_all" - all posts, all comment pages
    control.populate_database_comment_page("all_one")