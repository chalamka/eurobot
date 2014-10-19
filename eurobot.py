__author__ = 'ledif'

import time
import praw

pswd = None
r = praw.Reddit('eurobots')
r.login('s-moresModBot',pswd) 

already_checked = []
already_commented = set()

keyWords = ["jap"]

def findWords(comment, keyWords):
    print("in find words function")
    for keys in keyWords:
        if keys in temp and comment.id not in already_commented:
            print("Leaving a comment!")
            #comment.reply("Keep it respectful, please")
            already_commented.add(comment.id)
            time.sleep(2)

while True:
    subreddit = r.get_subreddit('wotcirclejerk')
    all_comments = []
    for submission in subreddit.get_top_from_week():
        all_comments.append(praw.helpers.flatten_tree(submission.comments))
    print("checking for comment")
    for comment in all_comments:
        temp = comment.comment.body.lower()
        findWords(temp, keyWords)
    time.sleep(600)



