import urllib.request
from os.path import exists

absolute_path = 'C:/Users/kikar.LAPTOP-Q25785DG/OneDrive/Desktop/University-Project/images/'


def retrieve_imgur_image(topic_id, image_urls):
    print("Retrieving images for topic %s" % topic_id)
    if image_urls:

        image_urls = image_urls.replace('{', '')
        image_urls = image_urls.replace('}', '')

        image_url = image_urls.split(',')
        number_of_images = len(image_url)

        for i in range(0, len(image_url)):
            name = str(topic_id) + "_" + str(i) + ".png"
            image_path = absolute_path + name
            if not exists(image_path):
                try:
                    urllib.request.urlretrieve(image_url[i], image_path)
                except Exception as error:
                    number_of_images -= 1
                    print("Encountered an error when retrieving image number %s for topic %s: " % (str(i+1), topic_id), error)
        return number_of_images
    else:
        print("No image urls provided for topic %s" % topic_id)
        return 0
