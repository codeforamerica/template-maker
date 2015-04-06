from bs4 import BeautifulSoup
from collections import defaultdict
from template_maker_test.unit.test_base import BaseTestCase
from template_maker.database import db
from template_maker.builder.models import TemplateSection, TemplatePlaceholders

from template_maker.data import sections as sc
from template_maker.data import placeholders as ph
from template_maker.data import documents as dm

from template_maker_test.unit import util

class SectionTest(BaseTestCase):
    render_templates = False
    def test_create_new_section(self):
        template = util.insert_new_template()

        section = {'type': 'text', 'title': 'foobar'}

        new_section_id = sc.create_new_section(section, template.id)
        # assert this is the first new section
        self.assertEquals(new_section_id, 1)
        # assert that the title and type were passed properly
        self.assertEquals(TemplateSection.query.get(new_section_id).__class__.__name__, 'TextSection')
        self.assertEquals(TemplateSection.query.get(new_section_id).title, 'foobar')

    def test_reorder_sections(self):
        template = util.insert_new_template()
        self.assertEquals(template.section_order, None)

        # insert some sections
        util.insert_new_section()
        util.insert_new_section()
        util.insert_new_section()

        new_order = [3,1,2]

        sc.reorder_sections(template, new_order)
        self.assertEquals(template.section_order, new_order)

    def test_update_section(self):
        # add the unicode placeholder type
        db.session.execute('''INSERT INTO placeholder_types VALUES (1, 'unicode')''')

        # generate a template, section, and document
        template = util.insert_new_template()
        section = util.insert_new_section()
        document_id = dm.create_new_document(template.id, {'name': 'foobar'})

        # add content to the section
        new_content = {
            'widget': 'this is a <span class="js-fr-placeholder">[[Text||foo]]</span>' +
            '<span class="js-fr-placeholder">[[Text||bar]]</span>' +
            '<span class="js-fr-placeholder">[[Text||baz]]</span>'
        }

        # update the section and document with our new content
        sc.update_section(section, [], template.id, new_content)
        dm.update_documents(template.id)

        # test that the placeholders made it in ok
        placeholders = TemplatePlaceholders.query.all()
        self.assertEquals(len(placeholders), 3)
        self.assertEquals(section.text, new_content.get('widget'))

        # add values to each of the placeholders
        dm.save_document_section(placeholders, {'[[foo]]': 'foo', '[[bar]]': 'foo', '[[baz]]': 'foo'})

        # test that the values were set properly
        document_placeholders = dm.get_document_placeholders(document_id)
        self.assertEquals(len(document_placeholders), 3)
        for placeholder in document_placeholders:
            self.assertEquals(placeholder.value, 'foo')

        # new content, deleting old placeholders
        new_content2 = {
            'widget': 'this is a section with fewer placeholders <span class="js-fr-placeholder">[[Text||foo]]</span>'
        }

        # update the section, documents
        sc.update_section(section, placeholders, template.id, new_content2)
        dm.update_documents(template.id)

        # test that everything is correct with the section
        self.assertEquals(len(TemplatePlaceholders.query.all()), 1)
        self.assertEquals(section.text, new_content2.get('widget'))

        # test that the documents were updated properly
        placeholders = TemplatePlaceholders.query.all()
        document_placeholders = dm.get_document_placeholders(document_id)
        self.assertEquals(len(document_placeholders), 1)
        self.assertEquals(document_placeholders[0].value, 'foo')

        # update the section, additional content
        # add content to the section
        new_content = {
            'widget': 'this is a <span class="js-fr-placeholder">[[Text||foo]]</span>' +
            '<span class="js-fr-placeholder">[[Text||bar]]</span>'
        }

        # update the section and document with our new content
        sc.update_section(section, placeholders, template.id, new_content)
        dm.update_documents(template.id)

        # test that the old value is still set
        document_placeholders = dm.get_document_placeholders(document_id)
        self.assertEquals(len(document_placeholders), 2)
        for placeholder in document_placeholders:
            if placeholder.display_name == '[[foo]]':
                self.assertEquals(placeholder.value, 'foo')

    def test_get_template_sections(self):
        template = util.insert_new_template()
        self.assertEquals(template.section_order, None)

        # insert some sections
        util.insert_new_section()
        util.insert_new_section()
        util.insert_new_section()

        # assert that we get the sections
        sections = sc.get_template_sections(template)
        self.assertEquals(len(sections), 3)

        # assert that if we have an order, the sections
        # are returned in that order
        new_order = [3,1,2]
        sc.reorder_sections(template, new_order)
        sections = sc.get_template_sections(template)
        self.assertEquals(len(sections), 3)
        self.assertEquals([i.id for i in sections], new_order)

class PlaceholderTest(BaseTestCase):
    def test_get_template_placeholders(self):
        template = util.insert_new_template()
        self.assertEquals(template.section_order, None)

        # insert some sections and some placeholders
        section1 = util.insert_new_section()
        section2 = util.insert_new_section()
        util.insert_new_placeholder(section1.id)
        util.insert_new_placeholder(section2.id)

        placeholders = ph.get_template_placeholders(template.id)
        self.assertEquals(len(placeholders), 2)

    def test_get_section_placeholders(self):
        template = util.insert_new_template()
        self.assertEquals(template.section_order, None)

        # insert some sections and some placeholders
        section1 = util.insert_new_section()
        section2 = util.insert_new_section()
        placeholder1 = util.insert_new_placeholder(section1.id)
        placeholder2 = util.insert_new_placeholder(section2.id)

        placeholders = ph.get_section_placeholders(placeholder1.id)
        self.assertEquals(len(placeholders), 1)
        placeholders = ph.get_section_placeholders(placeholder2.id)
        self.assertEquals(len(placeholders), 1)

    def test_parse_placeholder_text(self):
        # simple example
        soup = BeautifulSoup('<span>[[FOO||BAR]]</span>')
        placeholder = soup.find('span')
        var_type, var_name = ph.parse_placeholder_text(placeholder.text)
        self.assertEquals(var_type, 'foo')
        self.assertEquals(var_name, '[[BAR]]')

        # complex example should still work
        soup = BeautifulSoup('<span>[[FOO||This is a LONG StrINg with Weird Characterz]]</span>')
        placeholder = soup.find('span')
        var_type, var_name = ph.parse_placeholder_text(placeholder.text)
        self.assertEquals(var_type, 'foo')
        self.assertEquals(var_name, '[[This is a LONG StrINg with Weird Characterz]]')

class DocumentTest(BaseTestCase):
    def setUp(self):
        super(DocumentTest, self).setUp()
        self.template = util.insert_new_template()
        util.insert_new_placeholder(template_id=self.template.id)
        util.insert_new_section()
        self.document = util.insert_new_document(self.template.id)

    def test_get_documents(self):
        documents = dm.get_all_documents()
        self.assertEquals(len(documents), 1)
        util.insert_new_document(self.template.id, name='second test doc')
        documents = dm.get_all_documents()
        self.assertEquals(len(documents), 2)

        document = dm.get_single_document(2)
        self.assertEquals(document.template_id, self.template.id)

    def test_get_documents_from_single_parent(self):
        template_two = util.insert_new_template(title='test two')
        util.insert_new_document(template_two.id)
        util.insert_new_document(template_two.id)

        documents = dm.get_documents_and_parent_templates()
        test_results = defaultdict(int)
        for document in documents:
            test_results[document.title] += 1

        self.assertEquals(test_results['test'], 1)
        self.assertEquals(test_results['test two'], 2)
        self.assertEquals(len(test_results.keys()), 2)
        self.assertEquals(sum(test_results.values()), 3)

        document = dm.get_single_document_and_parent_template(self.document.id)
        self.assertEquals(document[2], 'test')

    def test_create_document(self):
        new_doc_id = dm.create_new_document(self.template.id, {'name': 'foobar'})
        placeholders = dm.get_document_placeholders(new_doc_id)
        self.assertEquals(len(placeholders), 1)

    def test_delete_document(self):
        new_doc_id = dm.create_new_document(self.template.id, {'name': 'foobar'})
        documents = dm.get_all_documents()
        self.assertEquals(len(documents), 2)
        dm.delete_document(self.document)
        documents = dm.get_all_documents()
        self.assertEquals(len(documents), 1)
        self.assertEquals(documents[0].id, new_doc_id)
