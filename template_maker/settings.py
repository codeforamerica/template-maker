import os

class Config(object):
    SECRET_KEY = os.environ.get('TEMPLATE_MAKER_SECRET', 'template-maker') # todo: change me

class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://localhost/template_maker')
    DEBUG_TB_INTERCEPT_REDIRECTS = False

class ProdConfig(Config):
    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class TestingConfig(Config):
    ENV = 'test'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    TESTING = True