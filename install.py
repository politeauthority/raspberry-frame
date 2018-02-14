"""Install

"""
from app import app
from app import db

from app.models.option import Option

DEFAULT_OPTIONS = ['INSTAGRAM_CLIENT_ID' 'INSTAGRAM_CLIENT_SECRET', 'INSTAGRAM_TOKEN']

if __name__ == '__main__':
    app.logger.info('Runing Installer')
    Option.set_defaults(DEFAULT_OPTIONS)
    db.create_all()
    print 'done'
