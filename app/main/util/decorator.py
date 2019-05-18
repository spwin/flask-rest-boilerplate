from functools import wraps
from flask import request

from app.main.service.auth_helper import Auth


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        user, status, error = Auth.get_logged_in_user(request)

        if not user:
            response_object = {
                'status': 'error',
                'message': error
            }
            return response_object, status

        return f(*args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        admin = token.get('admin')
        if not admin:
            response_object = {
                'status': 'error',
                'message': 'admin token required'
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated
