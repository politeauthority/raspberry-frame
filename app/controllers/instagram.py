"""Instagram - Controller
Mostly for authenticating and saving a token with Instagram so we can access instagram features.

"""
import urllib
import requests
import json

from flask import Blueprint, request

from app.models.option import Option

instagram = Blueprint('Instagram', __name__, url_prefix='/instagram')


@instagram.route('')
def auth_url():
    """
    Creates and displays the url for authorization

    """
    url = "https://api.instagram.com/oauth/authorize/?client_id=%s&redirect_uri=%s&response_type=code" % (
        Option.get('INSTAGRAM_CLIENT_ID').value,
        urllib.quote_plus('https://scs.bad-at.life/insta'),
    )
    return str(url)


@instagram.route('/auth')
def auth():
    """
    Callback method from Instagram after a user accepts the app.

    """
    payload = {
        'client_id': Option.get('INSTAGRAM_CLIENT_ID').value,
        'client_secret': Option.get('INSTAGRAM_CLIENT_SECRET').value,
        'grant_type': 'authorization_code',
        'redirect_uri': 'https://scs.bad-at.life/insta',
        'code': request.args.get("code")
    }
    token_url = "https://api.instagram.com/oauth/access_token"
    r = requests.post(token_url, data=payload)
    if not r.status_code == 200:
        return 'Error!: %s\n %s' % (r.status_code, r.text)

    json_resp = json.loads(r.text)
    token = Option.get('INSTAGRAM_TOKEN')
    if not token:
        token = Option()
        token.name = "INSTAGRAM_TOKEN"
    token.value = json_resp['access_token']
    token.save()

    return 'We good'

# End File: raspberry-frame/app/controllers/instagram.py
