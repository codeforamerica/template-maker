import datetime
from template_maker_test.unit.test_base import BaseTestCase
from template_maker.app import db
from template_maker.builder.models import (
    TemplateBase
)

class TestBuilder(BaseTestCase):
    render_templates = False
    def test_list_view(self):
        now = datetime.datetime.utcnow()
        template = TemplateBase(created_at=now, updated_at=now, title='test', description='test')
        db.session.add(template)
        db.session.commit()

        assert template in db.session

        response = self.client.get('/build/')
        assert response.status_code == 200
        self.assertEquals(len(self.get_context_variable('templates')), 1)

