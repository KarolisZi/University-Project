from bs4 import BeautifulSoup
import requests

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
    html_content = requests.get(url, headers).text
    soup = BeautifulSoup(html_content, "lxml")
    links = soup.find_all('a', class_='navPages')

    largest, topic_id_1 = 0, 0

    # Post id number format in url: "topic=5386857.00"
    #                                       id_1  id_2
    # (id_1) is the topic number and (id_2) is the comment page number
    for link in links:

        topic_id_12 = link.get('href').split(".")
        topic_id_2 = topic_id_12[-1]
        topic_id_1_temp = topic_id_12[-2].split("=")
        topic_id_1 = topic_id_1_temp[-1]

        # Fetch the last entry topic_id_2
        if int(topic_id_2) > int(largest):
            largest = topic_id_2

    result = [topic_id_1, largest]

    return result


# Given the topic and comment section numbers generate all comment page links
def generate_comment_links(url):

    numbers, links = fetch_last_page_id(url), []

    number_of_pages = int(int(numbers[1]) / 20) + 1

    for i in range(0, number_of_pages):
        links.append("https://bitcointalk.org/index.php?topic=" + str(numbers[0]) + "." + str(i * 20))

    return links


def fetch_comments(url):

    comments = []

    html_content = requests.get(url, headers).text
    soup = BeautifulSoup(html_content, "lxml")

    information = soup.find_all("td", class_="windowbg")

    for record in information:

        for br in record('br'):
            br.replace_with('\n')

        comments.append(record)

    return comments
