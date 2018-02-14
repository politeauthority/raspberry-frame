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


class InstagramFeed(object):

    def __init__(self):
        self.connect()
        self.base_image_dir = os.path.join(
            os.environ.get('RASPBERRY_FRAME_APP_DATA_PATH'),
            'images')

    def connect(self):
        """
        Gets the Option table item for INSTAGRAM_TOKEN and logs in.

        """
        INSTAGRAM_CLIENT_ID = Option.get('INSTAGRAM_CLIENT_ID').value
        INSTAGRAM_CLIENT_SECRET = Option.get("INSTAGRAM_CLIENT_SECRET").value
        INSTAGRAM_TOKEN = Option.get('INSTAGRAM_TOKEN').value
        if not INSTAGRAM_CLIENT_ID or not INSTAGRAM_CLIENT_SECRET or not INSTAGRAM_TOKEN:
            app.logger.error('Missing Instagram option values!')
            print 'INSTAGRAM_CLIENT_ID     %s' % INSTAGRAM_CLIENT_ID
            print 'INSTAGRAM_CLIENT_SECRET %s' % INSTAGRAM_CLIENT_SECRET
            print 'INSTAGRAM_TOKEN:        %s' % INSTAGRAM_TOKEN
            exit(1)
        self.INSTAGRAM_USER_ID = '374169053'

        self.api = InstagramAPI(
            access_token=INSTAGRAM_TOKEN,
            client_id=INSTAGRAM_CLIENT_ID,
            client_secret=INSTAGRAM_CLIENT_SECRET)

    def run(self):
        print 'Running instagram'
        # self.get_user_followers()
        self.get_user_feed()

    def get_user_feed(self):
        """
        Gets the users own feed.

        """
        recent_media, next_ = self.api.user_recent_media(user_id=self.INSTAGRAM_USER_ID, count=100)
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
            local_file_path = self.download_and_store_media(m.url, m.id, content_type)
            if local_file_path:
                m.file = local_file_path
                m.file_size = os.path.getsize(os.path.join(self.base_image_dir, local_file_path))
                m.downloaded = 1
            m.save()
            print m

    def download_and_store_media(self, url, media_id, content_type):
        """
        Downloads media from url and returns the saved file path.

        :param url: The url to download the media at.
        :type url: str
        :param media_id: The Media object's id.
        :type media_id: int
        :returns: The local file path to the downloaded file or False
        :rtype: str or bool
        """
        if not os.path.exists(self.base_image_dir):
            os.makedirs(self.base_image_dir)
        file_name = self._get_media_md5(media_id)
        local_file_path = "%s.%s" % (file_name, content_type)
        full_path = os.path.join(self.base_image_dir, local_file_path)

        try:
            response = requests.get(url, stream=True)
            with open(full_path, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
        except Exception, e:
            print 'Error %s' % e
            return False
        return local_file_path

    def get_user_followers(self):
        """
        Still waiting on approval from Instgram to be able to run this one.

        """
        users = self.api.user_follows(user_id=self.INSTAGRAM_USER_ID)
        print users

    def _get_media_md5(self, the_string):
        """
        Creates a md5 hash from a str

        :param the_string: The string to be hashed.
        :type the_string: str
        :returns: The hash equivillent
        :rtype: str
        """
        the_hash = hashlib.new('ripemd160')
        the_hash.update(str(the_string))
        return the_hash.hexdigest()

    def _convert_utc_to_local(self, utc_date):
        """
        Takes a UTC date and converts it to local time.

        :param utc_date: The UTC date to convert.
        :type utc_date: Datetime obj
        :returns: The local Datetime obj
        :rtype: Datetime obj
        """
        the_time = arrow.get(utc_date)
        the_time = the_time.to(os.environ.get('TZ', 'America/Denver'))
        return the_time.date()
