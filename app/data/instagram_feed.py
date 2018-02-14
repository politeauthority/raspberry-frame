"""Instagram Feed

"""

import os
import sys
import shutil
import hashlib

import arrow
import requests
from instagram.client import InstagramAPI
from sqlalchemy.orm.exc import NoResultFound

sys.path.append("../..")
from app import app
from app.models.media import Media
from app.models.option import Option

INSTAGRAM_CLIENT_ID = os.environ.get('INSTAGRAM_CLIENT_ID')
INSTAGRAM_CLIENT_SECRET = os.environ.get("INSTAGRAM_CLIENT_SECRET")
INSTAGRAM_USER_ID = '374169053'


class InstagramFeed(object):

    def __init__(self):
        self.connect()

    def connect(self):
        """
        Gets the Option table item for INSTAGRAM_TOKEN and logs in.
        """
        self.INSTAGRAM_TOKEN = Option.get('INSTAGRAM_TOKEN').value
        self.api = InstagramAPI(
            access_token=self.INSTAGRAM_TOKEN,
            client_id=INSTAGRAM_CLIENT_ID,
            client_secret=INSTAGRAM_CLIENT_SECRET)

    def run(self):
        print 'Running instagram'
        # self.get_user_followers()
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
