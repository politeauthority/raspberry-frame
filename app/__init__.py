"""App
Main file for the entire flask app.

"""
import os
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
import flask_restless


app = Flask(__name__)
if os.environ.get('RASPBERY_FRAME_BUILD') == 'LIVE':
    app.config.from_pyfile('config/live.py')
else:
    app.config.from_pyfile('config/dev.py')
db = SQLAlchemy(app)

# Models

# Helpers
# from app.helpers import misc_time
# from app.helpers import common
# from app.helpers import jinja_filters

# Controllers
from controllers.home import home as ctrl_home


def register_logging(app):
    """
    Connects the logging to the app.

    """
    log_dir = os.path.join(app.config['APP_DATA_PATH'], 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    app_log_file = os.path.join(log_dir, 'stocky.log')
    handler = TimedRotatingFileHandler(app_log_file, when='midnight', interval=1)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))

    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)


def register_blueprints(app):
    """
    Connect the blueprints to the router.

    """
    app.register_blueprint(ctrl_home)


def register_api(app):
    """
    Enables the API routes and configruation.

    """
    manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
    manager.create_api(Company, methods=['GET'])
    manager.create_api(Quote, methods=['GET'], max_results_per_page=365)

DebugToolbarExtension(app)
register_logging(app)
register_blueprints(app)
register_api(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


app.logger.info('Started App!')
