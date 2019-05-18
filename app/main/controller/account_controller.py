from flask import request
from flask_restplus import Resource

from app.main.service.account_service import on_reset_password, on_create_password, on_change_password
from app.main.util.decorator import token_required
from app.main.util.limiter import rate_limited
from ..util.dto import AccountDto

api = AccountDto.api

reset_password = AccountDto.reset_password
create_password = AccountDto.create_password
change_password = AccountDto.change_password


@api.route('/password')
class Account(Resource):
    @rate_limited(limit=10, minutes=1440)
    @api.response(200, 'Password successfully updated.')
    @api.response(400, 'Bad request.')
    @api.response(404, 'Not found.')
    @api.response(429, 'Too many requests.')
    @api.doc('reset password')
    @api.expect(reset_password, validate=True)
    def delete(self):
        """
        Send reset password link to email.
        Limited to 10 requests per 24h.
        """
        data = request.json
        return on_reset_password(data=data)

    @rate_limited(limit=10, minutes=60)
    @api.response(200, 'Password has been changed.')
    @api.response(400, 'Bad request.')
    @api.response(404, 'Not found.')
    @api.response(429, 'Too many requests.')
    @api.doc('create password')
    @api.expect(create_password, validate=True)
    def post(self):
        """
        Create new user password.
        Limited to 10 requests per 1h.
        """
        data = request.json
        return on_create_password(data=data)

    @token_required
    @api.response(200, 'Password has been changed.')
    @api.response(400, 'Bad request.')
    @api.doc('change password', security='apikey')
    @api.expect(change_password, validate=True)
    def put(self):
        """Change email address."""
        data = request.json
        return on_change_password(data=data, request=request)
