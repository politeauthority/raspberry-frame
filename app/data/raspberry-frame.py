"""Raspberry Frame
https://scs.bad-at.life/insta?code=55c8c4725ee841de9028d913db46b5e3
https://api.instagram.com/oauth/authorize/?client_id=c767989d473b48b9947e6f451c8a76fc&redirect_uri=https%3A%2F%2Fscs.bad-at.life%2Finsta&response_type=code


Usage:
    raspberry-frame.py <action> [options]

"""

import os
import sys
import shutil
import hashlib

import arrow
from docopt import docopt
import requests
from instagram.client import InstagramAPI
from sqlalchemy.orm.exc import NoResultFound

sys.path.append("../..")
from app import app
from app.models.media import Media

INSTAGRAM_CLIENT_ID = os.environ.get('INSTAGRAM_CLIENT_ID')
INSTAGRAM_CLIENT_SECRET = os.environ.get("INSTAGRAM_CLIENT_SECRET")
INSTAGRAM_TOKEN = os.environ.get("INSTAGRAM_TOKEN")
INSTAGRAM_USER_ID = '374169053'


class InstagramFeed(object):

    def __init__(self):
        self.api = InstagramAPI(
            access_token=INSTAGRAM_TOKEN,
            client_id=INSTAGRAM_CLIENT_ID,
            client_secret=INSTAGRAM_CLIENT_SECRET)

    def run(self):
        print 'Running instagram'
        self.get_user_followers()
        exit()
        self.get_user_feed()

    def get_user_followers(self):
        users = self.api.user_follows(user_id=INSTAGRAM_USER_ID)
        print users

    def get_user_feed(self):
        recent_media, next_ = self.api.user_recent_media(user_id="374169053", count=100)
        for i_media in recent_media:
            if hasattr(i_media, 'videos'):
                url = i_media.videos['standard_resolution'].url
            else:
                url = i_media.images['standard_resolution'].url
            content_type = url[url.rfind('.') + 1:]
            try:
                m = Media.query.filter(Media.url == url).one()
            except NoResultFound:
                m = Media()
            m.domain = 'instagram'
            m.url = url
            m.content_type = content_type
            m.media_created = self._convert_utc_to_local(i_media.created_time)
            m.author = i_media.user.username
            m.save()
            local_file_path = self.download_and_store_media(m.url, m.id)
            if local_file_path:
                m.file = local_file_path
                m.file_size = os.path.getsize(local_file_path)
                m.downloaded = 1
            m.save()
            print m
            print ''

    def download_and_store_media(self, url, media_id):
        """
        Downloads media from url and returns the saved file path.

        """
        local_file_path = os.path.join(
            os.environ.get('RASPBERRY_FRAME_APP_DATA_PATH', '/data'),
            'images')
        if not os.path.exists(local_file_path):
            os.makedirs(local_file_path)
        file_name = self._get_media_md5(media_id)
        local_file_path = os.path.join(local_file_path, file_name)

        try:
            response = requests.get(url, stream=True)
            with open(local_file_path, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
        except Exception, e:
            print 'Error %s' % e
            return False
        return local_file_path

    def _get_media_md5(self, media_id):
        """
        """
        the_hash = hashlib.new('ripemd160')
        the_hash.update(str(media_id))
        return the_hash.hexdigest()

    def _convert_utc_to_local(self, utc_date):
        """
        Takes a UTC date and converts it to local time.

        """
        the_time = arrow.get(utc_date)
        the_time = the_time.to(os.environ.get('TZ', 'America/Denver'))
        return the_time.date()

if __name__ == "__main__":
    args = docopt(__doc__)
    if args['<action>'] == 'instagram':
        InstagramFeed().run()
