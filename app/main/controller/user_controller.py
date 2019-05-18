from flask import request
from flask_restplus import Resource

from app.main.util.decorator import token_required
from app.main.util.limiter import rate_limited
from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user, update_user

api = UserDto.api

user_create = UserDto.user_create
user_read = UserDto.user_read
user_update = UserDto.user_update


@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_read, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

    @rate_limited(limit=10, minutes=1)
    @api.response(201, 'User successfully created.')
    @api.response(400, 'Bad request.')
    @api.response(401, 'Error generating authorization.')
    @api.response(409, 'User already exists.')
    @api.response(429, 'Too many requests.')
    @api.doc('create a new user')
    @api.expect(user_create, validate=True)
    def post(self):
        """
        Creates a new User
        Limited to 10 requests per 1 minute.
        """
        data = request.json
        return save_new_user(data=data)

    @token_required
    @api.response(201, 'User successfully updated.')
    @api.response(400, 'Bad request.')
    @api.response(401, 'Unauthorized request.')
    @api.response(403, 'Forbidden request.')
    @api.doc('update user details', security='apikey')
    @api.expect(user_update, validate=True)
    def patch(self):
        """Update my details"""
        data = request.json
        return update_user(data=data, request=request)


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
class User(Resource):
    @api.response(404, 'User not found.')
    @api.marshal_with(user_read)
    def get(self, public_id):
        """Get a user given its identifier"""
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user
