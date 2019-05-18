import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
temp = basedir + '/temp'


def get_env_bool(variable, default=False):
    value = os.getenv(variable)
    return default if not value else value == '1'


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')


class DevelopmentConfig(Config):
    DEBUG = get_env_bool('DEBUG', True)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///' + os.path.join(temp, 'flask_main.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENABLE_REQUESTS_LIMITER = get_env_bool('ENABLE_REQUESTS_LIMITER', False)


class TestingConfig(Config):
    DEBUG = get_env_bool('DEBUG', True)
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///' + os.path.join(temp, 'flask_test.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    ENABLE_REQUESTS_LIMITER = get_env_bool('ENABLE_REQUESTS_LIMITER', True)


class ProductionConfig(Config):
    DEBUG = get_env_bool('DEBUG', False)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///' + os.path.join(temp, 'flask_prod.db'))
    ENABLE_REQUESTS_LIMITER = get_env_bool('ENABLE_REQUESTS_LIMITER', True)


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
