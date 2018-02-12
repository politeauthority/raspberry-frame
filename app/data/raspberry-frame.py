"""Raspberry Frame
https://scs.bad-at.life/insta?code=55c8c4725ee841de9028d913db46b5e3
https://api.instagram.com/oauth/authorize/?client_id=c767989d473b48b9947e6f451c8a76fc&redirect_uri=https%3A%2F%2Fscs.bad-at.life%2Finsta&response_type=code


Usage:
    raspberry-frame.py <action> [options]

"""

from docopt import docopt

from instagram_feed import InstagramFeed
from reddit_feed import RedditFeed

if __name__ == "__main__":
    args = docopt(__doc__)
    if args['<action>'] == 'instagram':
        InstagramFeed().run()
    elif args['<action>'] == 'reddit':
        RedditFeed().run()
