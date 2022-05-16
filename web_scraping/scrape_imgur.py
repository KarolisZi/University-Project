import urllib.request
from os.path import exists
from image_to_text import image_to_text

absolute_path = 'C:/Users/kikar.LAPTOP-Q25785DG/OneDrive/Desktop/University-Project/images/'

"""
================================================================================================

RETRIEVE IMAGES FROM IMGUR

================================================================================================
"""


# Retrieve and store images found in author comments
def insert_image_data(author_comments):
    author_comments_text = []

    for comment in author_comments:

        topic_id, image_urls, raw_text = comment[0], comment[2], comment[3]

        if image_urls:
            number_of_images = len(image_urls)
            for i in range(0, number_of_images):
                no_errors = True
                name = str(topic_id) + "_" + str(i) + ".png"
                image_path = absolute_path + name
                if not exists(image_path):
                    try:
                        urllib.request.urlretrieve(image_urls[i], image_path)
                    except Exception as error:
                        no_errors = False
                        print("Encountered an error when retrieving image number: %s topic_id: %s url: %s: " % (
                        str(i), topic_id, image_urls[i]), error)

                    if no_errors:
                        image_insert_string = ('image_insert_here: %s' % image_urls[i])
                        image_text = image_to_text.convert(topic_id, i)
                        raw_text = raw_text.replace(image_insert_string, image_text)
        else:
            print("No image urls provided for topic %s" % topic_id)

        author_comments_text.append(raw_text)

    return author_comments_text
