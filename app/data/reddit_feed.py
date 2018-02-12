"""Reddit Feed

"""

import sys

import praw

sys.path.append("../..")
from app import app
from app.models.media import Media


class RedditFeed(object):

    def __init__(self):
        self.api = praw.Reddit(
            client_id='KghxWVF-O4l6hA',
            username='politeauthority',
            password='BNjepuTQ4n!@',
            client_secret=None,
            user_agent='RaspberryFrame')
        self.api.read_only = True

    def run(self):
        print 'Running Reddit'
        self.get_user_feed()

    def get_user_feed(self):
        print self.api
        for post in self.api.subreddit('all').top('hour'):
            print post
