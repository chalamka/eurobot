import time
import praw
import praw.helpers
import logging
import json

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

HISTORY_FILE = "history.json"


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
            time.sleep(2)


def main():
    r = praw.Reddit('eurobots')
    r.login('s-moresModBot')
    key_words = ["jap"]
    already_commented = load_commented(HISTORY_FILE)

    try:
        while True:
            subreddit = r.get_subreddit('wotcirclejerk')
            for submission in subreddit.get_top_from_month():
                comments = praw.helpers.flatten_tree(submission.comments)
                logger.info("Scanning %d comments in submission %s" % (len(comments), submission.url))
                for comment in comments:
                    find_words(comment, key_words, already_commented)
            time.sleep(600)
    except KeyboardInterrupt:
        write_commented(HISTORY_FILE, already_commented)

if __name__ == '__main__':
    main()