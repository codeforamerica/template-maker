from template_maker_test.unit.test_base import BaseTestCase
from template_maker.database import db
from template_maker.builder.models import (
    TemplateBase, TemplateSection, TextSection,
    FixedTextSection, TemplateVariables
)
from template_maker.builder.util import (
    create_new_section, parse_variable_text, reorder_sections,
    get_template_sections, get_template_variables, get_section_variables,
    update_section
)
from template_maker_test.unit.util import (
    create_a_template, insert_new_template, insert_new_section,
    create_a_variable, insert_new_variable
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

    def test_parse_variable_text(self):
        # simple example
        variable = '[[FOO||BAR]]'
        var_type, var_name = parse_variable_text(variable)
        self.assertEquals(var_type, 'foo')
        self.assertEquals(var_name, '[[BAR]]')

        # complex example should still work
        variable = '[[FOO||This is a LONG StrINg with Weird Characterz]]'
        var_type, var_name = parse_variable_text(variable)
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
        db.session.execute('''INSERT INTO variable_types VALUES (1, 'unicode')''')

        template = insert_new_template()
        section = insert_new_section()
        variable = insert_new_variable(section.id)

        new_content = {
            'widget': 'this is a [[Text||foo]] [[Text||bar]] [[Text||baz]] update'
        }

        update_section(section, template.id, new_content)
        self.assertEquals(len(TemplateVariables.query.all()), 3)
        self.assertEquals(section.text, new_content.get('widget'))

        new_content2 = {
            'widget': 'this is a section with fewer variables [[Text||foo]]'
        }

        update_section(section, template.id, new_content2)
        self.assertEquals(len(TemplateVariables.query.all()), 1)
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

    def test_get_template_variables(self):
        template = insert_new_template()
        self.assertEquals(template.section_order, None)

        # insert some sections and some variables
        section1 = insert_new_section()
        section2 = insert_new_section()
        variable1 = insert_new_variable(section1.id)
        variable2 = insert_new_variable(section2.id)

        variables = get_template_variables(template.id)
        self.assertEquals(len(variables), 2)

    def test_get_section_variables(self):
        template = insert_new_template()
        self.assertEquals(template.section_order, None)

        # insert some sections and some variables
        section1 = insert_new_section()
        section2 = insert_new_section()
        variable1 = insert_new_variable(section1.id)
        variable2 = insert_new_variable(section2.id)

        variables = get_section_variables(variable1.id)
        self.assertEquals(len(variables), 1)
        variables = get_section_variables(variable2.id)
        self.assertEquals(len(variables), 1)
