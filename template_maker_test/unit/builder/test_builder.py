import datetime
from template_maker_test.unit.test_base import BaseTestCase
from template_maker.app import db
from template_maker.builder.models import (
    TemplateBase
)

def create_a_template():
    now = datetime.datetime.utcnow()
    return TemplateBase(created_at=now, updated_at=now, title='test', description='test')

class TestBuilder(BaseTestCase):
    render_templates = False
    def test_list_view(self):
        template = create_a_template()
        db.session.add(template)
        db.session.commit()

        assert template in db.session

        response = self.client.get('/build/')
        assert response.status_code == 200
        self.assertEquals(len(self.get_context_variable('templates')), 1)


    def test_new_template(self):
        # it should get the proper template
        response = self.client.get('/build/new')
        assert response.status_code == 200
        self.assert_template_used('builder/new.html')

        post = self.client.post('/build/new', data=dict(
            title='title',
            description = 'description'
        ))
        # it should successfully add to the db and redirect us 
        # to the right section page
        assert post.status_code == 302
        assert post.location == 'http://localhost/build/1/section/new'
