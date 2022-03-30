from control import control

# Run testing
if __name__ == '__main__':

    # Create a database table from the home page information
    # "one" - one home page of posts
    # "all" - all post pages
    # control.populate_database_main_page("one")

    # Create a database table from the comment section
    # "one_one" - one post, once comment page
    # "one_all" - one post, all comment pages
    # "all_one" - all pages, one comment page
    # "all_all" - all posts, all comment pages
    # Reverse True (read comments from the last page first), False (read comments from the first page)
    control.populate_database_comment_page("all_one", True)

    # Create a database table from Google sheets
    # "all" - create records from all topics
    # "any_number" - creates records of that many topics. I.e. number 3 would create records from 3 topics
    control.populate_database_sheets("1")



