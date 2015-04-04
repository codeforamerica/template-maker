from bs4 import BeautifulSoup
from template_maker_test.unit.test_base import BaseTestCase
from template_maker.database import db
from template_maker.builder.models import (
    TemplateBase, TemplateSection, TextSection,
    FixedTextSection, TemplatePlaceholders
)

from template_maker.data.templates import (
    get_all_templates, get_single_template, delete_template, create_new_template,
    publish_template as _publish_template
)
from template_maker.data.sections import (
    create_new_section, update_section, get_template_sections, reorder_sections,
    get_single_section, delete_section as _delete_section
)

from template_maker.data.placeholders import (
    get_section_placeholders, get_template_placeholders, parse_placeholder_text
)

from template_maker_test.unit.util import (
    create_a_template, insert_new_template, insert_new_section,
    create_a_placeholder, insert_new_placeholder
)

class BuilderUtilTest(BaseTestCase):
    render_templates = False
    def test_create_new_section(self):
        template = insert_new_template()

        section = {'type': 'text', 'title': 'foobar'}

        new_section_id = create_new_section(section, template.id)
        # assert this is the first new section
        self.assertEquals(new_section_id, 1)
        # assert that the title and type were passed properly
        self.assertEquals(TemplateSection.query.get(new_section_id).__class__.__name__, 'TextSection')
        self.assertEquals(TemplateSection.query.get(new_section_id).title, 'foobar')

    def test_parse_placeholder_text(self):
        # simple example
        soup = BeautifulSoup('<span>[[FOO||BAR]]</span>')
        placeholder = soup.find('span')
        var_type, var_name = parse_placeholder_text(placeholder.text)
        self.assertEquals(var_type, 'foo')
        self.assertEquals(var_name, '[[BAR]]')

        # complex example should still work
        soup = BeautifulSoup('<span>[[FOO||This is a LONG StrINg with Weird Characterz]]</span>')
        placeholder = soup.find('span')
        var_type, var_name = parse_placeholder_text(placeholder.text)
        self.assertEquals(var_type, 'foo')
        self.assertEquals(var_name, '[[This is a LONG StrINg with Weird Characterz]]')

    def test_reorder_sections(self):
        template = insert_new_template()
        self.assertEquals(template.section_order, None)

        # insert some sections
        insert_new_section()
        insert_new_section()
        insert_new_section()

        new_order = [3,1,2]

        reorder_sections(template, new_order)
        self.assertEquals(template.section_order, new_order)

    def test_update_section(self):
        db.session.execute('''INSERT INTO placeholder_types VALUES (1, 'unicode')''')

        template = insert_new_template()
        section = insert_new_section()
        placeholder = insert_new_placeholder(section.id)

        new_content = {
            'widget': 'this is a <span class="js-fr-placeholder">[[Text||foo]]</span>' +
            '<span class="js-fr-placeholder">[[Text||bar]]</span>' +
            '<span class="js-fr-placeholder">[[Text||baz]]</span> update'
        }

        update_section(section, template.id, new_content)
        self.assertEquals(len(TemplatePlaceholders.query.all()), 3)
        self.assertEquals(section.text, new_content.get('widget'))

        new_content2 = {
            'widget': 'this is a section with fewer placeholders <span class="js-fr-placeholder">[[Text||foo]]</span>'
        }

        update_section(section, template.id, new_content2)
        self.assertEquals(len(TemplatePlaceholders.query.all()), 1)
        self.assertEquals(section.text, new_content2.get('widget'))


    def test_get_template_sections(self):
        template = insert_new_template()
        self.assertEquals(template.section_order, None)

        # insert some sections
        insert_new_section()
        insert_new_section()
        insert_new_section()

        # assert that we get the sections
        sections = get_template_sections(template)
        self.assertEquals(len(sections), 3)

        # assert that if we have an order, the sections
        # are returned in that order
        new_order = [3,1,2]
        reorder_sections(template, new_order)
        sections = get_template_sections(template)
        self.assertEquals(len(sections), 3)
        self.assertEquals([i.id for i in sections], new_order)

    def test_get_template_placeholders(self):
        template = insert_new_template()
        self.assertEquals(template.section_order, None)

        # insert some sections and some placeholders
        section1 = insert_new_section()
        section2 = insert_new_section()
        placeholder1 = insert_new_placeholder(section1.id)
        placeholder2 = insert_new_placeholder(section2.id)

        placeholders = get_template_placeholders(template.id)
        self.assertEquals(len(placeholders), 2)

    def test_get_section_placeholders(self):
        template = insert_new_template()
        self.assertEquals(template.section_order, None)

        # insert some sections and some placeholders
        section1 = insert_new_section()
        section2 = insert_new_section()
        placeholder1 = insert_new_placeholder(section1.id)
        placeholder2 = insert_new_placeholder(section2.id)

        placeholders = get_section_placeholders(placeholder1.id)
        self.assertEquals(len(placeholders), 1)
        placeholders = get_section_placeholders(placeholder2.id)
        self.assertEquals(len(placeholders), 1)
