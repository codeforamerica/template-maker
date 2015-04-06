from template_maker.generator.models import DocumentBase, DocumentPlaceholder
from template_maker.generator.views import create_rivets_bindings
from template_maker.data.documents import get_document_placeholders
from template_maker_test.unit.util import insert_new_template, insert_new_document, create_document_with_placeholders
from template_maker_test.unit.test_base import BaseTestCase

class TestGenerator(BaseTestCase):
    render_templates = False
    def test_list_view(self):
        # should only show published templates
        insert_new_template(published=True)
        insert_new_template(published=False)

        response = self.client.get('/generate/')
        assert response.status_code == 200
        self.assertEquals(len(self.get_context_variable('templates')), 1)

    def test_in_progress_documents(self):
        template = insert_new_template(published=True)
        insert_new_document(template.id, name='test')
        insert_new_document(template.id, name='test2')

        response = self.client.get('/generate/edit')
        assert response.status_code == 200
        self.assertEquals(len(self.get_context_variable('documents')), 2)

    def test_edit_in_progress_documents(self):
        template = insert_new_template(published=True)
        document = insert_new_document(template.id, name='test')
        insert_new_document(template.id, name='test2')

        self.assertEquals(len(DocumentBase.query.all()), 2)

        response = self.client.post('/generate/edit/' + str(document.id) + '?method=DELETE')
        self.assertEquals(len(DocumentBase.query.all()), 1)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.location, 'http://localhost/generate/edit')

    def test_new_document(self):
        template = insert_new_template(published=True)

        url = '/generate/new/from-template-' + str(template.id)
        new = self.client.get(url)
        self.assertEquals(new.status_code, 200)

        post = self.client.post(url, data=dict(
            name='test'
        ))

        self.assertEquals(len(DocumentBase.query.all()), 1)
        self.assertEquals(post.status_code, 302)
        self.assertEquals(post.location, 'http://localhost/generate/1/edit')

    def test_create_rivets_bindings(self):
        document = create_document_with_placeholders()
        placeholder = get_document_placeholders(document.id)[0]
        placeholder.display_name = '[[BAZ]]'
        section_text = 'foo bar foobar [[BAR||BAZ]]'

        self.assertEquals(
            create_rivets_bindings(placeholder, section_text),
            'foo bar foobar <input id="[[BAZ]]" placeholder="BAZ" name="[[BAZ]]" class="template-placeholder" rv-value="template.placeholder_BAZ"value="None">'
        )

        # assert that datepickers are added with the proper type
        placeholder.type = 2
        self.assertEquals(
            create_rivets_bindings(placeholder, section_text),
            'foo bar foobar <input id="[[BAZ]]" placeholder="BAZ" name="[[BAZ]]" class="template-placeholder datepicker" rv-value="template.placeholder_BAZ"value="None">'
        )

    def test_edit_document_sections(self):
        document = create_document_with_placeholders()
        request = self.client.get('/generate/' + str(document.id) + '/edit')
        self.assertEquals(request.status_code, 302)
        self.assertEquals(request.location, 'http://localhost/generate/1/edit/1')

        request = self.client.get('/generate/1/edit/1')
        document_placeholder = self.get_context_variable('form')._fields['[[BAZ]]']
        self.assertEquals(document_placeholder.rv_data_input, 'template.placeholder_BAZ')
        self.assertEquals(document_placeholder.name, '[[BAZ]]')

        post = self.client.post('/generate/1/edit/1', data={
            '[[BAZ]]': 'test'
        })

        # assert that the value has changed
        self.assertEquals(DocumentPlaceholder.query.first().value, 'test')
        self.assert_flashes('Changes successfully saved!', expected_category='alert-success')
        self.assertEquals(post.status_code, 302)
        self.assertEquals(post.location, 'http://localhost/generate/1/edit/1')
