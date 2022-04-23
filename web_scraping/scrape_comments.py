from bs4 import BeautifulSoup
import requests
import time

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/98.0.4758.102 Safari/537.36 '
}


# Retrieve topic the highest comment section number
def fetch_last_page_id(url):
    topic_id_1 = url.replace('https://bitcointalk.org/index.php?topic=', '').split('.')[0]

    # RETRIEVE TOPIC_ID_2
    topic_id_2_max = 0

    html_content = requests.get(url, headers).text

    while 'Too fast / overloaded (503)' in html_content:
        time.sleep(1)
        html_content = requests.get(url, headers).text

    soup = BeautifulSoup(html_content, "lxml")
    links = soup.find_all('a', class_='navPages')

    for link in links:

        topic_id_2 = link.get('href').split(".")[-1]

        # Fetch the last entry topic_id_2
        if int(topic_id_2) > int(topic_id_2_max):
            topic_id_2_max = topic_id_2

    result = [topic_id_1, topic_id_2_max]

    return result


# Given the topic and comment section numbers generate all comment page links
def generate_comment_links(url, mode):
    numbers, links = fetch_last_page_id(url), []

    print('URL: %s, numbers :%s' % (url, numbers))

    number_of_pages = int(int(numbers[1]) / 20) + 1

    if mode.isnumeric():
        mode = int(mode)
        if mode <= number_of_pages:
            for i in range(0, mode):
                links.append("https://bitcointalk.org/index.php?topic=" + str(numbers[0]) + "." + str(i * 20))
        else:
            print('The topic %s, only has %s page(s). Generating all links' % (numbers[0], number_of_pages))
            for i in range(0, number_of_pages):
                links.append("https://bitcointalk.org/index.php?topic=" + str(numbers[0]) + "." + str(i * 20))
    elif mode == 'all':
        for i in range(0, number_of_pages):
            links.append("https://bitcointalk.org/index.php?topic=" + str(numbers[0]) + "." + str(i * 20))

    return links


def fetch_comments(url):
    comments = []

    html_content = requests.get(url, headers).text

    while 'Too fast / overloaded (503)' in html_content:
        time.sleep(1)
        html_content = requests.get(url, headers).text

    soup = BeautifulSoup(html_content, "lxml")

    information_1 = soup.find_all("td", class_="windowbg")
    information_2 = soup.find_all("td", class_="windowbg2")

    for record in information_1:

        for br in record('br'):
            br.replace_with('\n')

        comments.append(record)

    for record in information_2:

        for br in record('br'):
            br.replace_with('\n')
        comments.append(record)

    return comments
