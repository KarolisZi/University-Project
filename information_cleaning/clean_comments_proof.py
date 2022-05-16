from values import regex
from information_cleaning import helper_functions
from classes.comment_proof import Proof

"""
========================================================================================================================

DATA CLEANING FOR COMMENTS OF PROOF

========================================================================================================================
"""


# Clean comments and prepare for storage in the database
def clean_comments(proof_comments):
    results = []

    for comment in proof_comments:

        proof = Proof(None, None, None, None, None, None, [], None, None)

        # RETRIEVE FORUM USERNAME AND LINK
        poster_info = comment.find('td', class_="poster_info")
        proof.set_forum_username(poster_info.find('a').text)
        proof.set_forum_profile_url(poster_info.find('a').get('href'))

        # RETRIEVE COMMENT ID AND POST TIME
        time_id = helper_functions.extract_post_time_and_id(comment)
        proof.set_post_time(time_id[0])
        proof.set_comment_id(time_id[1])

        # RETRIEVE POST FROM THE COMMENT
        post = comment.find('div', class_='post').text.split("\n")

        for line in post:

            # Telegram user name
            if "TELEGRAM" in line.upper() and "USER" in line.upper() and "NAME" in line.upper():
                if ':' in line:
                    temp = line.replace(":", " : ")
                    proof.set_telegram_username(temp.split(":")[-1].strip())
                else:
                    temp = line.split(" ")
                    proof.set_telegram_username(temp[-1].strip())
            elif "CAMPAIGN" in line.upper():
                if "TWITTER" in line.upper() or "TWIITER" in line.upper() and 'Twitter' not in proof.get_campaigns():
                    proof.set_campaigns('Twitter')
                if "FACEBOOK" in line.upper() and 'Facebook' not in proof.get_campaigns():
                    proof.set_campaigns('Facebook')
                if "REDDIT" in line.upper() and 'Reddit' not in proof.get_campaigns():
                    proof.set_campaigns('Reddit')
                if "YOUTUBE" in line.upper() and 'YouTube' not in proof.get_campaigns():
                    proof.set_campaigns('YouTube')
                if "LINKEDIN" in line.upper() and 'LinkedIn' not in proof.get_campaigns():
                    proof.set_campaigns('LinkedIn')
                if "INSTAGRAM" in line.upper() and 'Instagram' not in proof.get_campaigns():
                    proof.set_campaigns('Instagram')
                if "TELEGRAM" in line.upper() or "TELIGRAM" in line.upper() and 'Telegram' not in proof.get_campaigns():
                    proof.set_campaigns('Telegram')
                if "TIKTOK" in line.upper() or 'TIK TOK' in line.upper() and 'TikTok' not in proof.get_campaigns():
                    proof.set_campaigns('TikTok')
                if "ARTICLE" in line.upper() or "ARTICAL" in line.upper() and 'Article' not in proof.get_campaigns():
                    proof.set_campaigns('Article')
                if "VIDEO" in line.upper() and 'Video' not in proof.get_campaigns():
                    proof.set_campaigns('Video')
                if "BLOG" in line.upper() and 'Blog' not in proof.get_campaigns():
                    proof.set_campaigns('Blog')
                if "MEDIUM" in line.upper() and 'Medium' not in proof.get_campaigns():
                    proof.set_campaigns('Medium')
                if "DISCORD" in line.upper() and 'Discord' not in proof.get_campaigns():
                    proof.set_campaigns('Discord')
                if "SIGNATURE" in line.upper() and 'Signature' not in proof.get_campaigns():
                    proof.set_campaigns('Signature')
                if "TRANSLATION" in line.upper() and 'Translation' not in proof.get_campaigns():
                    proof.set_campaigns('Translation')
                if not proof.get_campaigns():
                    proof.set_campaigns('Other')
            elif "ADDRESS" in line.upper():
                if regex.eth_patter.match(line.split(":")[-1].strip()):
                    # Ether address
                    proof.set_wallet_address(line.split(":")[-1].strip())
                else:
                    # Other addresses (find regex for BTC)
                    proof.set_wallet_address(line.split(":")[-1].strip())

        results.append(proof)

    return results
