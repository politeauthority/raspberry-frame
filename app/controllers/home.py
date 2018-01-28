"""Home - Controller

"""

from flask import Blueprint, render_template


home = Blueprint('Home', __name__, url_prefix='/')


@home.route('')
def index():
    """
    Index

    """
    d = {}
    return render_template('home/index.html', **d)

# End File: raspberry-frame/app/controllers/home.py
