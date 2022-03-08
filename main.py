from control import control
from values import constant

# Run testing
if __name__ == '__main__':

    # Create a database table from the home page information
    # "one" - one home page of posts
    # "all" - all post pages
    control.populate_database_main_page("one", constant.TABLE_NAME_HOME_PAGE, constant.FIRST_PAGE_URL)

    # Create a database table from the comment section
    # "one_one" - one post, once comment page
    # "one_all" - one post, all comment pages
    # "all_all" - all posts, all comment pages
    control.populate_database_comment_page("one_one", constant.TABLE_NAME_COMMENT_PAGE)