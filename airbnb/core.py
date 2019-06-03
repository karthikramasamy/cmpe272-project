from functools import wraps
from flask import jsonify, session, redirect
from airbnb import constants
from airbnb.version import API_VERSION

def jsonify_error(message, staus_code):
    error = {
        'apiVersion': API_VERSION,
        'status_code': staus_code,
        'message': message
    }
    return (jsonify(error), staus_code)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if constants.PROFILE_KEY not in session:
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated

