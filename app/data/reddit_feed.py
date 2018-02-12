"""Instagram Feed

"""

import os
import sys
import shutil

import praw
import requests
from sqlalchemy.orm.exc import NoResultFound

sys.path.append("../..")
from app import app
from app.models.media import Media

INSTAGRAM_CLIENT_ID = os.environ.get('INSTAGRAM_CLIENT_ID')
INSTAGRAM_CLIENT_SECRET = os.environ.get("INSTAGRAM_CLIENT_SECRET")
INSTAGRAM_TOKEN = os.environ.get("INSTAGRAM_TOKEN")
INSTAGRAM_USER_ID = '374169053'


class RedditFeed(object):

    def __init__(self):
        self.api = praw.Reddit(
            client_id='my client id',
            client_secret='my client secret',
            user_agent='my user agent')

    def run(self):
        print 'Running Reddit'
        self.get_user_feed()

    def get_user_feed(self):
        print self.api

