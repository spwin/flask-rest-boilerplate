from flask import request
from flask_restplus import Resource

from app.main.service.auth_helper import Auth
from app.main.util.limiter import rate_limited
from ..util.dto import AuthDto

api = AuthDto.api
user_auth = AuthDto.user_auth


@api.route('/login')
class UserLogin(Resource):
    @rate_limited(limit=10, minutes=1)
    @api.response(200, 'Successfully logged in.')
    @api.response(401, 'Email or password does not match.')
    @api.response(429, 'Too many requests.')
    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    def post(self):
        """
        Receive Authorization token given user credentials
        Limited to 10 requests per 1 minute.
        """
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route('/logout')
class LogoutAPI(Resource):
    @api.response(200, 'Successfully logged out.')
    @api.response(401, 'Unauthorized request.')
    @api.response(403, 'Forbidden request.')
    @api.doc('logout a user')
    def post(self):
        """Log out user"""
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)
