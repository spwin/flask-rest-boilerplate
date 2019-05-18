import re


def validate_update(model, data):
    update_fields = model.__update__

    # check if there are some unexpected fields
    if not set(data.keys()).issubset(update_fields):
        raise AssertionError('Unexpected fields.')

    # check if no intersection between received and existing fields
    intersection = [field for field in update_fields if field in data.keys()]
    if len(intersection) == 0:
        raise AssertionError('No fields to update.')

    # check if values changed
    values_changed = False
    for key in intersection:
        if getattr(model, key) != data[key]:
            values_changed = True
    if not values_changed:
        raise AssertionError('New values are the same')

    return {key: data[key] for key in intersection}


def validate_fields(fields, data):
    # check if there are some unexpected fields
    if not set(data.keys()).issubset(fields):
        raise AssertionError('Unexpected fields.')

    # check if no intersection between received and existing fields
    intersection = [field for field in fields if field in data.keys()]
    if len(intersection) == 0:
        raise AssertionError('No fields to update.')

    # check if there's email field and validate
    for field in fields:
        if field == 'email':
            validate_email(data[field])

    return {key: data[key] for key in intersection}


def validate_email(email):
    if not re.match("[^@]+@[^@]+\.[^@]+", email):
        raise AssertionError('Provided email is incorrect.')


def validate_password(password):
    if len(password) < 8:
        raise AssertionError('Password must be at least 8 digits.')
    if ' ' in password:
        raise AssertionError('Password must not contains whitespaces.')
