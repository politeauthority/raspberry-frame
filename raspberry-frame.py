"""Raspberry Frame

Usage:
    raspberry-frame.py <action> [options]

"""

from docopt import docopt
from instagram.client import InstagramAPI

from config import config

INSTAGRAM_CLIENT_ID = config['instagram_client_id']
INSTAGRAM_CLIENT_SECRET = config['instagram_client_secret']


def instagram_run():
    print 'Running instagram'
    print INSTAGRAM_CLIENT_ID
    print INSTAGRAM_CLIENT_SECRET
    api = InstagramAPI(client_id=INSTAGRAM_CLIENT_ID, client_secret=INSTAGRAM_CLIENT_SECRET)
    popular_media = api.media_popular(count=20)
    for media in popular_media:
        print media.images['standard_resolution'].url

if __name__ == "__main__":
    args = docopt(__doc__)
    if args['<action>'] == 'instagram':
        instagram_run()
