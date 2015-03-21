import os

class Config(object):
    SECRET_KEY = os.environ.get('TEMPLATE_MAKER_SECRET', 'template-maker') # todo: change me

class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://localhost/template_maker')
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    BROWSERID_URL = os.environ.get('BROWSERID_URL', 'http://localhost:9000')

class ProdConfig(Config):
    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    BROWSERID_URL = os.environ.get('BROWSERID_URL')

class TestingConfig(Config):
    ENV = 'test'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_template_maker'
    WTF_CSRF_ENABLED = False
    TESTING = True