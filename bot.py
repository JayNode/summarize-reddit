"""
NOTES: Fix rate limiter by stopping run after first success
"""

import praw
import requests
import tldextract

import config
import scraper
import summary

# We don't reply to posts which have a very small or very high reduction.
MINIMUM_REDUCTION_THRESHOLD = 20
MAXIMUM_REDUCTION_THRESHOLD = 68

# File locations
POSTS_LOG = "./processed_posts.txt"
WHITELIST_FILE = "./assets/whitelist.txt"
ERROR_LOG = "./error.log"

# Templates.
TEMPLATE = open("./templates/template.txt", "r", encoding="utf-8").read()


HEADERS = {"User-Agent": "Summarizer v2.0"}


def load_whitelist():
    # Reads the processed posts log file and creates it if it doesn't exist. A list of domains that are confirmed to have an 'article' tag.
    with open(WHITELIST_FILE, "r", encoding="utf-8") as log_file:
        return log_file.read().splitlines()


def load_log():
    # Reads the processed posts log file and creates it if it doesn't exist. A list of Reddit posts ids.
    try:
        with open(POSTS_LOG, "r", encoding="utf-8") as log_file:
            return log_file.read().splitlines()

    except FileNotFoundError:
        with open(POSTS_LOG, "a", encoding="utf-8") as log_file:
            return []


def update_log(post_id):
    # Updates the processed posts log with the given post id. A Reddit post id.
    with open(POSTS_LOG, "a", encoding="utf-8") as log_file:
        log_file.write("{}\n".format(post_id))


def log_error(error_message):
    # Updates the error log. A string containing the faulty url and the exception message.
    with open(ERROR_LOG, "a", encoding="utf-8") as log_file:
        log_file.write("{}\n".format(error_message))


def init():
    # Inits the bot
    reddit = praw.Reddit(client_id=config.APP_ID, client_secret=config.APP_SECRET,
                         user_agent=config.USER_AGENT, username=config.REDDIT_USERNAME,
                         password=config.REDDIT_PASSWORD)

    processed_posts = load_log()
    whitelist = load_whitelist()

    # for subreddit in config.SUBREDDITS:

    for submission in reddit.subreddit('nasa').new(limit=50):

        if submission.id not in processed_posts:
            # use tldextract to seperate url into respective parts
            clean_url = submission.url.replace("amp.", "")
            ext = tldextract.extract(clean_url)
            domain = "{}.{}".format(ext.domain, ext.suffix)

            if domain in whitelist:

                try:
                    with requests.get(clean_url, headers=HEADERS, timeout=10) as response:
                        # Checks for edge cases where encoding is not in utf-8, use ISO-8859-1  
                        if "iso-8859-1" in response.text.lower():
                            response.encoding = "iso-8859-1"
                        elif response.encoding == "ISO-8859-1":
                            response.encoding = "utf-8"

                        html_source = response.text

                    article_title, article_date, article_body = scraper.scrape_html(
                        html_source)

                    summary_dict = summary.get_summary(article_body)
                except Exception as e:
                    log_error("{},{}".format(clean_url, e))
                    update_log(submission.id)
                    print("Failed:", submission.id)
                    continue

                # To reduce low quality submissions, we only process those that made a meaningful summary.
                if summary_dict["reduction"] >= MINIMUM_REDUCTION_THRESHOLD and summary_dict["reduction"] <= MAXIMUM_REDUCTION_THRESHOLD:

                    # We start creating the comment body.
                    post_body = "\n\n".join(
                        ["> " + item for item in summary_dict["top_sentences"]])

                    top_words = ""

                    for index, word in enumerate(summary_dict["top_words"]):
                        top_words += "{}^#{} ".format(word, index+1)

                    post_message = TEMPLATE.format(
                        article_title, clean_url, summary_dict["reduction"], article_date, post_body)

                    reddit.submission(submission.id).reply(post_message)
                    update_log(submission.id)
                    print("Replied to:", submission.id)
                else:
                    update_log(submission.id)
                    print("Skipped:", submission.id)


if __name__ == "__main__":
    init()
