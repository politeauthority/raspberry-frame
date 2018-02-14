"""Content - Controller

"""
import os

from flask import Blueprint, Response, redirect


content = Blueprint('Content', __name__, url_prefix='/content')

EXT_MAP = {
    'jpg': 'image/jpg',
    'mp4': 'video/type'
}


@content.route('/<path:path>')
def fetch(path):
    """
    Fetches a file from the local system if a match can be found, and it fits an allowed Extension Map

    :param path: Any GET url paramater send through the /content URI
    :type path: str
    """
    content_type = None
    if '.' in path:
        ext = path[path.rfind('.') + 1:]
        if ext in EXT_MAP:
            content_type = EXT_MAP[ext]

    if not content_type:
        redirect('/error')

    return Response(get_file(path), mimetype=content_type)


def get_file(filename):
    """
    Gets the file from the file system or returns and IO Error if nothing can be found.

    :param filename: Local file path from the RF image dir
    :type filename: str
    :returns: The opened file object or the error.
    :rtype: Open File
    """
    try:
        src = os.path.join(
            os.environ.get('RASPBERRY_FRAME_APP_DATA_PATH'),
            'images',
            filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)

# End File: raspberry-frame/app/controllers/content.py
