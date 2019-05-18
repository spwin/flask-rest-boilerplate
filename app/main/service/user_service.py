import uuid
import sqlalchemy as sa

from app.main import db
from app.main.model.user import User
from app.main.service.auth_helper import Auth
from app.main.util.dto import UserDto
from app.main.util.validate import validate_update, validate_fields

user_create = UserDto.user_create


def update_user(data, request):
    user, status, error = Auth.get_logged_in_user(request)

    if not user:
        response_object = {
            'status': 'error',
            'message': error
        }
        return response_object, status

    try:
        fields = validate_update(model=user, data=data)

        # assign fields with extra validation for some attributes
        for field, value in fields.items():
            if field == 'email':
                User.validate_email(user, key='email', email=data['email'])
            setattr(user, field, data[field])

        save_changes()
    except AssertionError as error:
        response_object = {
            'status': 'error',
            'message': str(error)
        }
        return response_object, 400

    response_object = {
        'status': 'success',
        'message': 'User updated.',
    }
    return response_object, 200


def save_new_user(data):
    try:
        data = validate_fields(fields=user_create.keys(), data=data)
    except AssertionError as error:
        response_object = {
            'status': 'error',
            'message': str(error)
        }
        return response_object, 400

    user = User.query.filter_by(email=data['email']).first()
    if user:
        response_object = {
            'status': 'error',
            'message': 'User with this email already exists.',
        }
        return response_object, 409

    user = User.query.filter_by(username=data['username']).first()
    if user:
        response_object = {
            'status': 'error',
            'message': 'User with this username already exists.',
        }
        return response_object, 409

    try:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            first_name=data['first_name'] if 'first_name' in data else None,
            last_name=data['last_name'] if 'last_name' in data else None,
            registered_on=sa.func.now()
        )
    except AssertionError as error:
        response_object = {
            'status': 'error',
            'message': str(error)
        }
        return response_object, 400

    save_changes(new_user)
    return generate_token(new_user)


def generate_token(user):
    try:
        # generate the auth token
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'error',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def get_all_users():
    return User.query.all()


def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()


def save_changes(data=None):
    if data:
        db.session.add(data)
    db.session.commit()
