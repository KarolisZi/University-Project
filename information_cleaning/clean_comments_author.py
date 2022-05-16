import urllib.parse
from values import regex
from classes.comment_author import Author
from classes.topic import Topic
from information_cleaning import helper_functions
from database import crud_topic
import re

"""
========================================================================================================================

DATA EXTRACTION FOR AUTHOR COMMENTS

========================================================================================================================
"""


# Prepare author comments for storage in the database, check if it contains any images or not
def clean_comments(author_comments, topic_id):
    author_object_array = extract_post_data(author_comments)
    images, comments_text = False, []

    for author_object in author_object_array:

        if author_object.get_image_check():
            images = True

        comments_text.append(author_object.get_text_data())

    if not images and author_comments:
        analysed_comment = analyse_author_comment_text(comments_text)
        crud_topic.create('populate_reward_rules', [topic_id, analysed_comment.get_campaign()])

    return author_object_array


# Retrieve post data of the author comment
def extract_post_data(author_comments):
    results = []

    if author_comments:

        for i in range(0, len(author_comments)):

            author = Author(None, None, [], [], None, [])

            # Get post_time and comment_id
            time_id = helper_functions.extract_post_time_and_id(author_comments[i])
            author.set_post_time(time_id[0])
            author.set_comment_id(time_id[1])

            # Retrieve the post form post & header
            post = author_comments[i].find('div', class_='post')

            # Get all post links
            href_tags = post.find_all(href=True)
            for tag in href_tags:
                author.set_urls(tag['href'])

            # Get the post and image_urls
            images_comment = extract_image_urls(post)

            # Add the text data to the file
            author.set_image_urls(images_comment[0])
            author.set_text_data(images_comment[1].text)

            if not author.get_image_urls():
                author.set_image_check(False)
            elif author.get_image_urls():
                author.set_image_check(True)

            results.append(author)

    return results


# Retrieve image URLS from a comment containing images
def extract_image_urls(comment):
    image_urls = []

    img_tags = comment.find_all('img')

    for tag in img_tags:

        src = tag.get('src')

        if regex.image_proxy_pattern.match(src):
            url = src.replace('https://ip.bitcointalk.org/?u=', '')
            url = urllib.parse.unquote(url)
            image_urls.append(url.split('&')[0])
            tag.insert(0, 'image_insert_here: %s' % url.split('&')[0])

    return [image_urls, comment]


"""
========================================================================================================================

DATA ANALYSIS FOR AUTHOR COMMENTS (with images and with no images)

========================================================================================================================
"""


# Retrieve information from the author comment (with images inserted as text)
def analyse_author_comment_text(author_comments):
    topic = Topic(None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
    reward_pool, reward_allocation, token_names, urls, campaigns_info, event_list = [], [], [], [], [], []

    if len(author_comments) >= 1:

        lines = author_comments[0].split('\n')

        for i in range(0, len(lines)):

            if lines[i] is not None and lines[i] != '':

                # REWARD POOL
                if 'REWARD' in lines[i].upper() or 'BOUNTY' in lines[i].upper() and 'POOL' in lines[i].upper():
                    for temp_i in range(i, i + 2):
                        if temp_i <= len(lines) - \
                                1:
                            for match in re.finditer(regex.reward_pool_amount, lines[temp_i]):
                                amount = match.group(0)
                                if amount not in ['.', '. ', '.  ', ',', '$', ' ']:
                                    reward_pool.append(amount.strip())

                # REWARD ALLOCATION
                if 'ALLOCATION' in lines[i].upper() or 'DISLOCATION' in lines[i].upper():

                    counter = 0
                    for temp_i in range(i, len(lines)):
                        if '%' in lines[temp_i]:
                            entry = regex.emoji_pattern.sub(' ', lines[temp_i])
                            reward_allocation.append(entry.strip())
                            counter = 0
                        else:
                            counter += 1
                        if counter >= 5:
                            break
                # TOKEN NAME
                if 'TOKEN' in lines[i].upper() or 'BOUNTY' in lines[i].upper() or 'CAMPAIGN' in lines[i].upper():
                    tokens = helper_functions.extract_token_name(lines[i])
                    for token in tokens:
                        token_clen = regex.emoji_pattern.sub(' ', token)
                        token_clen = token_clen.replace('#', '').strip()
                        token_names.append(token_clen)
                if 'CAMPAIGN' in lines[i].upper():
                    words, event = lines[i].split(' '), ''
                    for word in words:
                        if word.upper() in ['FACEBOOK', 'TWITTER', 'REDDIT', 'YOUTUBE', 'LINKEDIN', 'INSTAGRAM',
                                            'TELEGRAM', 'TIKTOK', 'ARTICLE', 'VIDEO', 'BLOG', 'MEDIUM', 'DISCORD',
                                            'SIGNATURE', 'TRANSLATION']:
                            event = word.upper()

                    if event:

                        reward_stakes, rules, complete = [], [], []

                        if i + 20 > len(lines):
                            buffer = 20
                        else:
                            buffer = len(lines) - i - 1

                        for temp_i in range(i, i + buffer):

                            if temp_i <= len(lines) - 1:

                                if 'REWARDS' in lines[temp_i].upper() and len(lines[temp_i]) < 20:
                                    empty_lines, check, index = 0, True, 1,

                                    # STOP WHEN: Find 'RULES' or pass an empty array
                                    while check and index < len(lines) - temp_i:

                                        if lines[temp_i + index]:

                                            clean_line = regex.emoji_pattern.sub(' ', lines[temp_i + index])

                                            reward_stakes.append(clean_line.strip())

                                            if not lines[temp_i + index - 1] and index >= 3:
                                                empty_lines += 1

                                        if 'RULES' in lines[temp_i].upper() and len(lines[temp_i]) < 20:
                                            check = False
                                            complete.append('Rewards')
                                        elif empty_lines >= 2:
                                            check = False
                                            complete.append('Rewards')

                                        index += 1

                                if 'RULES' in lines[temp_i].upper() and len(lines[temp_i]) < 20:

                                    empty_lines, check, index = 0, True, 1
                                    # STOP WHEN: Find 'RULES' or pass an empty array
                                    while check and index < len(lines) - temp_i:

                                        if lines[temp_i + index]:

                                            clean_line = regex.emoji_pattern.sub(' ', lines[temp_i + index])

                                            rules.append(clean_line.strip())

                                            if not lines[temp_i + index - 1] and index > 3:
                                                empty_lines += 1

                                        if 'REWARDS' in lines[temp_i].upper() and len(lines[temp_i]) < 20:
                                            check = False
                                            complete.append('Rules')
                                        elif empty_lines >= 3:
                                            check = False
                                            complete.append('Rules')

                                        index += 1
                                if 'Rules' in complete and 'Rewards' in complete:
                                    break

                        if reward_stakes or rules:

                            if event in event_list:
                                for i in range(0, len(event_list)):
                                    string = event + '-' + str(i + 2)
                                    if string not in event_list:
                                        event = string
                                        break

                            event_list.append(event)
                            campaigns_info.append([event, reward_stakes, rules])

        topic.set_reward_pool(reward_pool)
        topic.set_reward_allocation(reward_allocation)
        if token_names:
            topic.set_token_name(max(set(token_names), key=token_names.count))
        topic.set_campaign(campaigns_info)

    return topic


"""
========================================================================================================================

FUNCTIONS TO EXTRACT SPREADSHEET LINKS AND IDS FROM AUTHOR COMMENTS

========================================================================================================================
"""


# extracts spreadsheet ids from spreadsheet links
def extract_spreadsheet_ids(author_comments):
    sheet_ids = []

    links = extract_spreadsheet_links(author_comments)

    for link in links:
        # FIX ERROR sheet_ids.append(link.split('/')[5]). IndexError: list index out of range

        link_decomposed = link.split('/')

        if len(link_decomposed) >= 6:
            sheet_ids.append(link_decomposed[5])

    return sheet_ids

# extract spreadsheet links from author comments
def extract_spreadsheet_links(author_comments):
    spreadsheet_links = []

    for comment in author_comments:

        # Retrieve post and header
        header_post = comment.find('td', class_="td_headerandpost")

        # Retrieve comment_id from the header
        # comment_id = header_post.find('a', class_='message_number').text.replace("#", "")
        # if comment_id == 1:

        comment_lines = header_post.find('div', class_='post')

        if (len(comment_lines)) > 0:

            post_links = comment_lines.find_all('a', class_='ul')

            for link in post_links:

                if regex.spreadsheet_pattern.match(link.get('href')):
                    spreadsheet_links.append(link.get('href'))

    return spreadsheet_links
