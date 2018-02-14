"""Install

"""
from app import app
from app import db

from app.models.option import Option


def create_default_options():
    if not Option.get('INSTAGRAM_TOKEN'):
        o = Option()
        o.name = 'INSTAGRAM_TOKEN'
        o.save()

    if not Option.get('INSTAGRAM_TOKEN_2'):
        o = Option()
        o.name = 'INSTAGRAM_TOKEN_2'
        o.save()

    if not Option.get('INSTAGRAM_TOKEN_3'):
        o = Option()
        o.name = 'INSTAGRAM_TOKEN_3'
        o.save()

if __name__ == '__main__':
    app.logger.info('Runing Installer')
    db.create_all()
    create_default_options()
