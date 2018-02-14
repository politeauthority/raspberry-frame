"""Reddit Feed

"""

import sys

import praw

sys.path.append("../..")
from app.models.option import Option


class RedditFeed(object):

    def __init__(self):
        self.api = praw.Reddit(
            client_id=Option.get('REDDIT_CLIENT_ID'),
            username=Option.get('REDDIT_USER'),
            password=Option.get('REDDIT_PASSWORD'),
            client_secret=Option.get('REDDIT_CLIENT_SECRET'),
            user_agent='RaspberryFrame')
        self.api.read_only = True

    def run(self):
        exit()
        print 'Running Reddit'
        self.get_user_feed()

    def get_user_feed(self):
        print self.api
        for post in self.api.subreddit('all').top('hour'):
            print post
