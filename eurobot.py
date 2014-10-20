import time
import praw
import praw.helpers
import logging
import json
import sys


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

HISTORY_FILE = "history.json"
CONFIG_FILE = "config.json"

def load_config(filename):
    try:
        with open(filename) as fp:
            return json.load(fp)
    except IOError:
        logger.info("Failed to load configuration file")
        #exits program with code 2
        sys.exit(2)


def load_commented(filename):
    try:
        with open(filename) as fp:
            return json.load(fp)
    except IOError:
        return []


def write_commented(filename, already_commented):
    with open(filename, 'w') as fp:
        return json.dump(already_commented, fp)


def find_words(comment, key_words, already_commented):
    for keys in key_words:
        if keys in comment.body.lower() and comment.id not in already_commented:
            logger.info("Replying to %s" % comment.id)
            comment.reply("Keep it respectful, please")
            already_commented.append(comment.id)
            time.sleep(5)


def main():
    r = praw.Reddit('eurobot')
    config_dict = load_config(CONFIG_FILE)
    r.login(config_dict['username'], config_dict['password'])
    key_words = config_dict['keywords']
    already_commented = load_commented(HISTORY_FILE)

    try:
        while True:
            subreddit = r.get_subreddit(config_dict['subreddit'])
            for submission in subreddit.get_top_from_month():
                comments = praw.helpers.flatten_tree(submission.comments)
                logger.info("Scanning %d comments in submission %s" % (len(comments), submission.url))
                for comment in comments:
                    find_words(comment, key_words, already_commented)
            logger.info("Submissions scanned, entering 10min sleep")
            time.sleep(600)
    except KeyboardInterrupt:
        write_commented(HISTORY_FILE, already_commented)

if __name__ == '__main__':
    main()