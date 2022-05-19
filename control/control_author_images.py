from web_scraping import scrape_imgur
from database import crud_comments
from database import crud_topic
from information_cleaning import clean_comments_author
from alive_progress import alive_bar


def populate_database_author(mode):
    data = crud_comments.read('author[topic_id, comment_id=1, image_urls, raw_text]', [])

    match mode:
        case 'one':
            create_entries(data, 'all_new')
        case 'all_new':
            create_entries(data, 'all_failed')
        case 'all_new_failed':
            create_entries(data, 'all_new_failed')


# Extract, clean and store data from author comments which include pictures
def create_entries(data, mode):
    with alive_bar(len(data), title='Author post + image') as bar:

        for entry in data:

            complete, no_errors, check = False, True, False

            successful_check = crud_topic.read('successful_transfers[images_successful]', entry[0])

            if entry[1] == 1:

                match mode:
                    case 'all_new':
                        if successful_check[0][0] is None:
                            check = True
                    case 'all_failed':
                        if not successful_check[0][0]:
                            check = True
                    case 'all_new_failed':
                        if successful_check[0][0] is None or not successful_check[0][0]:
                            check = True

                if check:

                    try:
                        text = scrape_imgur.insert_image_data([entry])
                        topic = clean_comments_author.analyse_author_comment_text(text)

                        crud_topic.update('topic[author]', [entry[0], topic])
                        crud_topic.create('populate_reward_rules', [entry[0], topic.get_campaign()])

                        if mode == 'one':
                            return
                    except Exception as error:
                        print(error)
                        no_errors = False

                    if no_errors:
                        crud_topic.update('successful_transfers[images_successful=True]', entry[0])
                    elif not no_errors:
                        crud_topic.update('successful_transfers[images_successful=False]', entry[0])
                bar()
