import os

class Config(object):
    SECRET_KEY = os.environ.get('WEXPLORER_SECRET', 'template-maker') # todo: change me

class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True

class ProdConfig(Config):
    ENV = 'prod'
    DEBUG = False
