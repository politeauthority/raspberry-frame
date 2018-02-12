"""Content - Controller

"""
import os

from flask import Blueprint, send_from_directory

# from app.models.media import Media

content = Blueprint('Content', __name__, url_prefix='/content')


@content.route('/<path:path>')
def fetch(path):
    """
    fetch

    """
    # if '../' in path:
    #     return str(), 403
    file_path = os.path.join(
        'images',
        path)
    # return str(file_path)
    # if not os.path.exists(file_path):
    #     return str(file_path)

    return send_from_directory('data', file_path)

# End File: raspberry-frame/app/controllers/content.py
