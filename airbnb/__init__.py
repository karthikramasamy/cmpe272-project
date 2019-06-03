from os import environ as env
from os import path as path
from flask import Flask, jsonify, request, session, redirect, render_template, url_for, send_from_directory
from werkzeug.exceptions import HTTPException
from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode
from dotenv import load_dotenv

from airbnb.version import API_VERSION
from airbnb import constants
from airbnb.core import requires_auth
from airbnb.core import jsonify_error

import json
import jwt
import datetime


def create_app(app_config=None):
    """Create and configure an instance of the Flask application."""


    dotenv_path = path.join(path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    app = Flask(__name__, static_url_path='/static', static_folder='./static', instance_relative_config=True)
    
    FLASK_SECRET_KEY = env.get('FLASK_SECRET_KEY')
    if not FLASK_SECRET_KEY:
        FLASK_SECRET_KEY = "secretdev"

    AUTH0_CALLBACK_URL = env.get(constants.AUTH0_CALLBACK_URL)
    AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
    AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
    AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
    AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
    AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)
    if AUTH0_AUDIENCE is '':
        AUTH0_AUDIENCE = AUTH0_BASE_URL + '/userinfo'


    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY=FLASK_SECRET_KEY,
    )

    if app_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(app_config)

    oauth = OAuth(app)
    auth0 = oauth.register(
        'auth0',
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        api_base_url=AUTH0_BASE_URL,
        access_token_url=AUTH0_BASE_URL + '/oauth/token',
        authorize_url=AUTH0_BASE_URL + '/authorize',
        client_kwargs={
            'scope': 'openid profile',
        },
    )

    @app.route('/status')
    def status():
        message = {
            'apiVersion': API_VERSION,
            'status_code': 200,
            'message': 'OK'
        }
        return jsonify(message)


    @app.route('/callback')
    def callback_handling():
        auth0.authorize_access_token()
        resp = auth0.get('userinfo')
        userinfo = resp.json()

        session[constants.JWT_PAYLOAD] = userinfo
        session[constants.PROFILE_KEY] = {
            'user_id': userinfo['sub'],
            'name': userinfo['name'],
            'picture': userinfo['picture']
        }
        return redirect('/home')
        
    @app.route('/favicon.ico')
    def favicon():
        print("favicon")
        return send_from_directory(path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.route('/login')
    def login():
        return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)

    @app.route('/logout')
    def logout():
        session.clear()
        params = {'returnTo': url_for('home', _external=True), 'client_id': AUTH0_CLIENT_ID}
        return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

    @app.route('/')
    @app.route('/home')
    @requires_auth
    def home():
        if session and session[constants.PROFILE_KEY]:
            user_info_json = session[constants.JWT_PAYLOAD]
            user_id_string = user_info_json.get('sub', '0|0')
            user_id = user_id_string.split('|')[1]
            return render_template('home.html', userinfo=session[constants.PROFILE_KEY], userid=user_id)
        else:
            return render_template('home.html')
            
    @app.route('/listings/<listing_id>')
    @requires_auth
    def render_listing_page(listing_id):
        user_info_json = session[constants.JWT_PAYLOAD]
        user_id_string = user_info_json.get('sub', '0|0')
        user_id = user_id_string.split('|')[1]
        api_response = airbnb_api.get_listing(listing_id)

        listing = None
        try:
            listing = api_response.get_json()
        except Exception as ex:
            return api_response

        iframe = listing['listing_url']
        return render_template('listing.html', userinfo=session[constants.PROFILE_KEY], userid=user_id, listing=listing, iframe=iframe)
        
    @app.route('/details/<listing_id>')
    @requires_auth
    def render_details_page(listing_id):
        user_info_json = session[constants.JWT_PAYLOAD]
        user_id_string = user_info_json.get('sub', '0|0')
        user_id = user_id_string.split('|')[1]
        api_response = airbnb_api.get_listing(listing_id)

        listing = None
        try:
            listing = api_response.get_json()
        except Exception as ex:
            return api_response

        return render_template('view.html', userinfo=session[constants.PROFILE_KEY], userid=user_id, listing_id=listing['_id'], listing=json.dumps(listing, indent=4))

    @app.errorhandler(404)
    def page_not_found(e):
        """Send message to the user with notFound 404 status."""
        return jsonify_error("Page Not Found. Refer to the API documentation.", 404)

    @app.errorhandler(Exception)
    def error_handler(ex):
        print(ex)
        status_code = (ex.code if isinstance(ex, HTTPException) else 500)
        message = {
            'apiVersion': API_VERSION,
            'status_code': status_code,
            'message': str(ex)
        }
        response = jsonify(message)
        response.status_code = status_code
        return response


    # register the database commands
    from airbnb import airbnb_db
    airbnb_db.init_app(app)

    # apply the blueprints to the app
    from airbnb import airbnb_api
    app.register_blueprint(airbnb_api.bp)

    return app
