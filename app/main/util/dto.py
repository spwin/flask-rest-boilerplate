from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('users', description='user related operations')
    user_create = api.model('user_create', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'first_name': fields.String(required=False, description='user first name'),
        'last_name': fields.String(required=False, description='user last name'),
    })
    user_read = api.model('user_read', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'first_name': fields.String(required=False, description='user first name'),
        'last_name': fields.String(required=False, description='user last name'),
        'public_id': fields.String(readonly=True, description='user unique identifier'),
        'registered_on': fields.String(readonly=True, description='user registration date')
    })
    user_update = api.model('user_update', {
        'email': fields.String(required=False, description='user email address'),
        'username': fields.String(required=False, description='user username'),
        'first_name': fields.String(required=False, description='user first name'),
        'last_name': fields.String(required=False, description='user last name'),
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })


class AccountDto:
    api = Namespace('account', description='account management operations')
    reset_password = api.model('reset_password', {
        'email': fields.String(required=True, description='The email address'),
    })
    create_password = api.model('create_password', {
        'secret': fields.String(required=True, description='Password change secret'),
        'password': fields.String(required=True, description='New user password'),
    })
    change_password = api.model('change_password', {
        'old_password': fields.String(required=True, description='Old user password'),
        'new_password': fields.String(required=True, description='New user password'),
    })
