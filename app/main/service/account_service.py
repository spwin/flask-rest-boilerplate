import datetime
import secrets

from app.main import db
from app.main.model.forgot_password import ForgotPassword
from app.main.model.user import User
from app.main.service.auth_helper import Auth
from app.main.util.validate import validate_fields, validate_password

from ..util.dto import AccountDto

reset_password = AccountDto.reset_password
create_password = AccountDto.create_password
change_password = AccountDto.change_password


def on_reset_password(data=None):
    try:
        validate_fields(reset_password.keys(), data)
    except AssertionError as error:
        response_object = {
            'status': 'error',
            'message': str(error)
        }
        return response_object, 400

    user = User.query.filter_by(email=data['email']).first()
    if not user:
        response_object = {
            'status': 'error',
            'message': 'User with this email not found.'
        }
        return response_object, 404

    try:
        forgot_password = ForgotPassword(
            hash=secrets.token_urlsafe(60),
            user_id=user.id
        )
    except AssertionError as error:
        response_object = {
            'status': 'error',
            'message': str(error)
        }
        return response_object, 400

    save_changes(forgot_password)
    response_object = {
        'status': 'success',
        'message': 'Password reset email has been sent.'
    }
    return response_object, 200


def on_create_password(data=None):
    try:
        validate_fields(create_password.keys(), data)
        validate_password(data['password'])
    except AssertionError as error:
        response_object = {
            'status': 'error',
            'message': str(error)
        }
        return response_object, 400

    forgot_password = ForgotPassword.query.filter_by(hash=data['secret']).first()
    if not forgot_password:
        response_object = {
            'status': 'error',
            'message': 'Invalid secret.'
        }
        return response_object, 400

    token_age = datetime.datetime.now() - forgot_password.created_at
    if token_age.seconds > 60 * 60 * 24:
        response_object = {
            'status': 'error',
            'message': 'Secret expired.'
        }
        return response_object, 400

    user = forgot_password.user
    if not user:
        response_object = {
            'status': 'error',
            'message': 'User not found for given secret.'
        }
        return response_object, 404

    user.password = data["password"]
    save_changes()

    response_object = {
        'status': 'error',
        'message': 'Password has been changed.'
    }
    return response_object, 200


def on_change_password(data, request):
    user, status, error = Auth.get_logged_in_user(request)

    if not user:
        response_object = {
            'status': 'error',
            'message': error
        }
        return response_object, status

    try:
        validate_fields(change_password.keys(), data)
        validate_password(data["new_password"])
    except AssertionError as error:
        response_object = {
            'status': 'error',
            'message': str(error)
        }
        return response_object, 400

    if not user.check_password(data["old_password"]):
        response_object = {
            'status': 'error',
            'message': 'Incorrect old password.'
        }
        return response_object, 400

    if data["old_password"] == data["new_password"]:
        response_object = {
            'status': 'error',
            'message': 'New password must be different to old one.'
        }
        return response_object, 400

    user.password = data["new_password"]
    save_changes()

    response_object = {
        'status': 'success',
        'message': 'Password has been changed.'
    }
    return response_object, 200


def save_changes(data=None):
    if data:
        db.session.add(data)
    db.session.commit()
