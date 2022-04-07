from web_scraping import scrape_imgur
from database import db_crud_comments
from image_to_text import image_to_text
from alive_progress import alive_bar

"""
================================================================================================

CONTROL OPERATIONS FOR AUTHOR COMMENTS (IMAGE) ANALYSIS

================================================================================================
"""


def populate_database_author(check):
    data = db_crud_comments.fetch_all_id_image_urls()

    match check:
        case 'one':
            create_one_image_topic_entry(data)
        case 'all':
            create_all_image_topic_entries(data)


def create_one_image_topic_entry(data):
    if data[0][2]:
        # Download images
        len_images = scrape_imgur.retrieve_imgur_image(data[0][0], data[0][1])

        if len_images > 0:
            # Convert images to text
            text = image_to_text.convert(data[0][0], len_images)

            db_crud_comments.insert_image_text(data[0][0], text)


def create_all_image_topic_entries(data):
    with alive_bar(len(data)) as bar:

        for entry in data:

            if entry[2]:
                # Download images
                len_images = scrape_imgur.retrieve_imgur_image(entry[0], entry[1])

                if len_images > 0:
                    # Convert images to text
                    text = image_to_text.convert(entry[0], len_images)

                    db_crud_comments.insert_image_text(data[0][0], text)
        bar()