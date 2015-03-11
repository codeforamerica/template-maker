from flask.ext.testing import TestCase

from template_maker.settings import TestingConfig
from template_maker.app import create_app as _create_app, db

class BaseTestCase(TestCase):
    '''
    A base test case that boots our app
    '''
    def create_app(self):
        return _create_app(TestingConfig)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()