from template_maker_test.unit.test_base import BaseTestCase
from template_maker.builder.models import (
    TemplateBase, TemplateSection, TextSection,
    FixedTextSection, TemplateVariables
)
from template_maker.builder.util import (
    create_new_section, parse_variable_text, reorder_sections
)
from template_maker_test.unit.util import (
    create_a_template, insert_new_template, insert_new_section
)

class BuilderUtilTest(BaseTestCase):
    def test_create_new_section(self):
        template_id = insert_new_template()

        section = {'type': 'text', 'title': 'foobar'}

        new_section_id = create_new_section(section, template_id)
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
        template_id = insert_new_template()
        template = TemplateBase.query.get(template_id)
        self.assertEquals(template.section_order, None)

        # insert some sections
        insert_new_section()
        insert_new_section()
        insert_new_section()

        new_order = [3,1,2]

        reorder_sections(template, new_order)
        self.assertEquals(template.section_order, new_order)

    def test_update_section(self):
        pass

    def test_update_variables(self):
        pass

    def test_get_template_sections(self):
        pass

    def test_get_template_variables(self):
        pass

    def test_get_section_variables(self):
        pass
