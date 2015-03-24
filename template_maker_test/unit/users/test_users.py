from mock import Mock, patch
from flask.ext.login import current_user, login_user

from template_maker_test.unit.test_base import BaseTestCase
from template_maker_test.unit.util import insert_a_user
from template_maker.users.models import User
from template_maker.app import db

class TestUserAuth(BaseTestCase):
    render_templates = False
    def setUp(self):
        super(TestUserAuth, self).setUp()
        self.email = 'foo@foo.com'
        insert_a_user(is_admin=True, email=self.email)

    @patch('urllib2.urlopen')
    def test_auth_persona_failure(self, urlopen):
        mock_open = Mock()
        mock_open.read.side_effect = ['{"status": "error"}']
        urlopen.return_value = mock_open

        post = self.client.post('/users/auth', data=dict(
            assertion='test'
        ))

        self.assert403(post)

    @patch('urllib2.urlopen')
    def test_auth_no_user(self, urlopen):
        mock_open = Mock()
        mock_open.read.side_effect = ['{"status": "okay", "email": "not_a_valid_email"}']
        urlopen.return_value = mock_open

        post = self.client.post('/users/auth', data=dict(
            assertion='test'
        ))

        self.assert403(post)

    @patch('urllib2.urlopen')
    def test_auth_success(self, urlopen):
        mock_open = Mock()
        mock_open.read.side_effect = ['{"status": "okay", "email": "' + self.email + '"}']
        urlopen.return_value = mock_open

        post = self.client.post('/users/auth?next=/build/8/sections/', data=dict(
            assertion='test'
        ))

        self.assert200(post)
        self.assertEquals(post.data, '/build/8/sections/')

    @patch('urllib2.urlopen')
    def test_logout(self, urlopen):

        login_user(User.query.all()[0])

        logout = self.client.get('/users/logout', follow_redirects=True)
        self.assert_flashes('Logged out successfully!', 'alert-success')
        self.assert_template_used('users/logout.html')

        login_user(User.query.all()[0])
        logout = self.client.post('/users/logout?persona=True', follow_redirects=True)
        self.assertTrue(logout.data, 'OK')
