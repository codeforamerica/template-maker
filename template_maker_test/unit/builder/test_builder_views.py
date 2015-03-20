from werkzeug.datastructures import ImmutableMultiDict
from template_maker_test.unit.test_base import BaseTestCase
from template_maker.app import db
from template_maker.builder.models import (
    TemplateBase, TemplateSection, TextSection
)
from template_maker_test.unit.util import (
    create_a_template, create_a_text_section, insert_new_template
)

class TestBuilder(BaseTestCase):
    render_templates = False
    def test_list_view(self):
        template = insert_new_template()

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
        self.assertEquals(len(TemplateBase.query.all()), 1)
        assert post.status_code == 302
        assert post.location == 'http://localhost/build/1/section/'

    def test_publish_template(self):
        template = create_a_template()
        db.session.add(template)
        db.session.commit()

        # assert that the right template is used
        response = self.client.get('/build/1/publish')
        self.assert_template_used('builder/preview.html')

        # assert that the post sets the publish flag to true
        post = self.client.post('/build/1/publish')
        template = TemplateBase.query.get(1)
        self.assertTrue(template.published)
        assert post.location == 'http://localhost/generate/1/generate'

class TestEditTemplate(BaseTestCase):
    render_templates = False
    def setUp(self):
        # setUp the super class
        super(TestEditTemplate, self).setUp()

        template = create_a_template()
        db.session.add(template)
        db.session.commit()

        sections = [['title1', 'text1'], ['title2', 'text2']]
        for section in sections:
            section = create_a_text_section(section[0], section[1])
            db.session.add(section)
            db.session.commit()

        self.assertEquals(len(TemplateSection.query.all()), 2)

    def test_new_section(self):
        self.client.get('/build/1/section/new/text')
        # we can add new blank sections
        self.assertEquals(len(TemplateSection.query.all()), 3)
        # we can add new sections with titles
        self.client.get('/build/1/section/new/text?section_title=foo')
        self.assertEquals(len(TemplateSection.query.all()), 4)
        self.assertEquals(TemplateSection.query.get(4).title, 'foo')
        # we can add new boilerplate sections
        self.client.get('/build/1/section/new/text?boilerplate=true')
        self.assertEquals(len(TemplateSection.query.all()), 5)
        self.assertEquals(TemplateSection.query.get(5).text, 'Please insert your text here.')

        self.assert403(self.client.get('/build/1/section/new/foobarbaz'))

    def test_edit_template_metadata(self):
        self.assertEquals(len(TemplateBase.query.all()), 1)
        # trigger the delete through the spoofed "get" request
        self.client.get('/build/1/edit?method=DELETE')
        self.assertEquals(len(TemplateBase.query.all()), 0)
        self.assertEquals(len(TemplateSection.query.all()), 0)

    def test_edit_template_get(self):
        response = self.client.get('/build/1/section/1')
        self.assert_200(response)
        self.assertEquals(self.get_context_variable('current_section').id, 1)
        self.assertEquals(self.get_context_variable('current_section').text, 'text1')
        self.assertEquals(self.get_context_variable('template').id, 1)
        self.assertEquals(len(self.get_context_variable('sections')), 2)

        response = self.client.get('/build/1/')
        self.assertEquals(response.location, 'http://localhost/build/1/section/')

    def test_edit_template_post(self):
        # update a section's title and text content
        post = self.client.post('/build/1/section/1', data=dict(
            type='text',
            title='bar',
            widget='foo'
        ))

        self.assert_flashes('Successfully saved!', expected_category='alert-success')

        request = self.client.get('/build/1/section/1')
        self.assertEquals(self.get_context_variable('current_section').id, 1)
        self.assertEquals(self.get_context_variable('current_section').title, 'bar')
        self.assertEquals(self.get_context_variable('current_section').text, 'foo')

    def test_reorder_sections(self):
        # make sure the two are in the right order
        order = [i.id for i in TemplateSection.query.all()]
        self.assertEquals(order, [1,2])

        # make a post request with a different order of sections
        post = self.client.post('/build/1/section/', data=ImmutableMultiDict(
            [('id', '2'), ('id', '1')]
        ))

        # Ensure that saved flashes
        self.assert_flashes('Successfully saved!', expected_category='alert-success')
        self.assertEquals(post.location, 'http://localhost/build/1/section/')

        # ensure the TemplateBase was updated properly
        self.assertEquals(TemplateBase.query.get(1).section_order, [2,1])
        # ensure that the returning template was updated properly
        request = self.client.get('/build/1/section/1')
        new_order = [i.id for i in self.get_context_variable('sections')]
        self.assertEquals(new_order, [2,1])

        # ensure you can delete a section
        self.client.get('/build/1/section/2/delete')
        self.assertEquals(TemplateBase.query.get(1).section_order, [1])
        self.assertEquals(len(TemplateSection.query.all()), 1)

        # ensure POSTing when there is no section id still works
        post = self.client.post('/build/1/section/0')
        self.assertEquals(post.location, 'http://localhost/build/1/section/')

    def test_delete_section(self):
        request = self.client.get('/build/1/section/2/delete')
        self.assertEquals(len(TemplateSection.query.all()), 1)
        assert request.location == 'http://localhost/build/1/section/'
        self.assert_flashes('Section successfully deleted!', expected_category='alert-success')
