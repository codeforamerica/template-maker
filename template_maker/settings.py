import os

class Config(object):
    SECRET_KEY = os.environ.get('WEXPLORER_SECRET', 'template-maker') # todo: change me

class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://localhost/template_maker')
    DEBUG_TB_INTERCEPT_REDIRECTS = False

class ProdConfig(Config):
    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
