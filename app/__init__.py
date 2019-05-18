# app/__init__.py

from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.account_controller import api as account_ns

version = '1.0'

blueprint = Blueprint('api', __name__, url_prefix="/api/{v}".format(v=version))

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(blueprint,
          title='Flask API',
          version=version,
          description='Public api endpoints.',
          authorizations=authorizations
          )

api.add_namespace(user_ns)
api.add_namespace(auth_ns)
api.add_namespace(account_ns)
