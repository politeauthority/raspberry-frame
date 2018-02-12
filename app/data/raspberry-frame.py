"""Raspberry Frame
https://scs.bad-at.life/insta?code=55c8c4725ee841de9028d913db46b5e3
https://api.instagram.com/oauth/authorize/?client_id=c767989d473b48b9947e6f451c8a76fc&redirect_uri=https%3A%2F%2Fscs.bad-at.life%2Finsta&response_type=code


Usage:
    raspberry-frame.py <action> [options]

"""

import os
import sys
import shutil
from datetime import datetime

import arrow
from docopt import docopt
import requests
from instagram.client import InstagramAPI

sys.path.append("../..")
from app import app
from app.models.media import Media

INSTAGRAM_CLIENT_ID = os.environ.get('INSTAGRAM_CLIENT_ID')
INSTAGRAM_CLIENT_SECRET = os.environ.get("INSTAGRAM_CLIENT_SECRET")
INSTAGRAM_TOKEN = os.environ.get("INSTAGRAM_TOKEN")


def instagram_run():
    print 'Running instagram'
    print app.config['SQLALCHEMY_DATABASE_URI']
    api = InstagramAPI(
        access_token=INSTAGRAM_TOKEN,
        client_id=INSTAGRAM_CLIENT_ID,
        client_secret=INSTAGRAM_CLIENT_SECRET)
    recent_media, next_ = api.user_recent_media(user_id="374169053", count=100)
    for i_media in recent_media:
        m = Media()
        m.domain = 'instagram'
        m.ts_created = datetime.now()
        m.ts_updated = datetime.now()
        m.media_created = _convert_utc_to_local(i_media.created_time)
        m.author = i_media.user.username
        if hasattr(i_media, 'videos'):
            m.url = i_media.videos['standard_resolution'].url
            m.content_type = m.url[m.url.rfind('.') + 1:]
        else:
            m.url = i_media.images['standard_resolution'].url
            m.content_type = m.url[m.url.rfind('.') + 1:]
        print m.author
        print m.content_type
        print m.url
        local_file_path = download_and_store_media(m.url)
        if local_file_path:
            m.file = local_file_path
            m.file_size = os.path.getsize(local_file_path)
        print m.save()
        print m
        print ''


def download_and_store_media(url):
    """
    Downloads media from url and returns the saved file path.

    """
    print 'Downloading: %s' % url
    local_file_path = os.path.join(
        os.environ.get('RASPBERRY_FRAME_APP_DATA_PATH', '/data'),
        'images')
    print local_file_path
    if not os.path.exists(local_file_path):
        os.makedirs(local_file_path)
    file_name = url[url.rfind('/') + 1:]
    local_file_path = os.path.join(local_file_path, file_name)

    try:
        response = requests.get(url, stream=True)
        with open(local_file_path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
    except Exception, e:
        print 'Error %s' % e
        return False
    return local_file_path


def _convert_utc_to_local(utc_date):
    """
    Takes a UTC date and converts it to local time.

    """
    the_time = arrow.get(utc_date)
    the_time = the_time.to(os.environ.get('TZ', 'America/Denver'))
    return the_time.date()

if __name__ == "__main__":
    args = docopt(__doc__)
    if args['<action>'] == 'instagram':
        instagram_run()
