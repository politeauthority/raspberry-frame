"""Home - Controller

"""

from flask import Blueprint, render_template

from app.models.media import Media

home = Blueprint('Home', __name__, url_prefix='/')


@home.route('')
def index():
    """
    Index

    """
    d = {}
    d['medias'] = Media.query.all()
    return render_template('home/index.html', **d)

# End File: raspberry-frame/app/controllers/home.py
