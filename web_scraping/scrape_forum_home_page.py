from bs4 import BeautifulSoup
import requests
from web_scraping import infromation_cleaning

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/98.0.4758.102 Safari/537.36 '
}


# Returns the URL of the last post pages
def fetch_last_post_page_id(url):
    html_content = requests.get(url, headers).text
    soup = BeautifulSoup(html_content, "lxml")
    links = soup.find_all('a', class_='navPages')

    largest = 0

    # Main page number format in url: "board=238.00"
    #                                       id_1 id_2
    # (id_1) is the board number and (id_2) is the board page number

    for i in range(0, len(links)):
        topic_id_12 = links[i].get('href').split(".")
        topic_id_2 = topic_id_12[-1]
        topic_id_1_temp = topic_id_12[-2].split("=")
        topic_id_1 = topic_id_1_temp[-1]

        # Fetch the last entry topic_id_2
        if int(topic_id_2) > int(largest):
            largest = topic_id_2

    result = [topic_id_1, largest]

    return result


# Calculates all pages links from first one to the last because their ending goes up by 40 per each page
def generate_all_post_page_links(numbers):
    links = []
    number_of_pages = int(int(numbers[1]) / 40) + 1

    for i in range(0, number_of_pages):
        links.append("https://bitcointalk.org/index.php?board=" + str(numbers[0]) + "." + str(i * 40))
    return links


# Returns all posts from a given URL
# [Link, Topix, Started by, Replies, Views, Last post time, Last post author]
def fetch_post_from_url(url):
    results = []
    html_content = requests.get(url, headers).text
    soup = BeautifulSoup(html_content, "lxml")

    table = soup.find_all('table', class_='bordercolor')

    for tr in table:
        row = tr.find_all('tr')
        for td in row:
            col = td.find_all('td')
            if len(col) == 7:
                cleaned_data = infromation_cleaning.clean_post_information_data(col)
                if "BOUNTY" in cleaned_data[2].upper():
                    results.append(cleaned_data)

    return results