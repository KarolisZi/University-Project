from values import regex
import helper_functions


def extract_data_from_proof_comments(proof_comments):
    results = []

    for comment in proof_comments:

        address, telegram_username = "", ""
        data, campaigns = [], []

        # Retrieve forum username and link
        poster_info = comment.find('td', class_="poster_info")
        forum_username = poster_info.find('a').text
        profile_url = poster_info.find('a').get('href')

        # Retrieve post and header
        header_post = comment.find('td', class_="td_headerandpost")

        # Retrieve comment_id from the header
        comment_id = header_post.find('a', class_='message_number').text.replace("#", "")

        # Retrieve time from the header
        time = header_post.find('div', class_='smalltext').text

        if 'Last edit:' in time:
            temp = time.split('Last edit:')
            time = temp[0].strip()

        time = helper_functions.convert_time(time)

        # Retrieve post from header and post
        post = header_post.find('div', class_='post').text.split("\n")

        for text in post:

            # Telegram user name
            if "TELEGRAM" and "USER" and "NAME" in text.upper():
                temp = text.replace(":", " : ")
                temp = temp.split(":")
                telegram_username = temp[-1].rstrip().lstrip()

            elif "CAMPAIGN" in text.upper():

                if "TWITTER" in text.upper() or "TWIITER" in text.upper():
                    campaigns.append('Twitter')
                if "FACEBOOK" in text.upper():
                    campaigns.append('Facebook')
                if "REDDIT" in text.upper():
                    campaigns.append('Reddit')
                if "YOUTUBE" in text.upper():
                    campaigns.append('YouTube')
                if "LINKEDIN" in text.upper():
                    campaigns.append('LinkedIn')
                if "INSTAGRAM" in text.upper():
                    campaigns.append('Instagram')
                if "TELEGRAM" in text.upper() or "TELIGRAM" in text.upper():
                    campaigns.append('Telegram')
                if "TIKTOK" in text.upper() or 'TIK TOK' in text.upper():
                    campaigns.append('TikTok')
                if "ARTICLE" in text.upper() or "ARTICAL" in text.upper():
                    campaigns.append('Article')
                if "VIDEO" in text.upper():
                    campaigns.append('Video')
                if "BLOG" in text.upper():
                    campaigns.append('Blog')

            elif "ADDRESS" in text.upper():
                temp = text.split(":")
                if regex.eth_patter.match(temp[-1].rstrip().lstrip()):
                    address = temp[-1].rstrip().lstrip()
            else:
                data.append(text)

        results.append([comment_id, forum_username, profile_url, telegram_username, campaigns, time, address])

    return results
