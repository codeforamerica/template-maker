import datetime
from template_maker.database import db
from template_maker.builder.models import (
    TemplateBase, TemplateSection, TextSection, TemplateVariables
)

def create_a_template():
    now = datetime.datetime.utcnow()
    return TemplateBase(created_at=now, updated_at=now, title='test', description='test')

def insert_new_template():
    template = create_a_template()
    db.session.add(template)
    db.session.commit()
    return template

def create_a_text_section(title, text):
    section = TextSection(template_id=1, title=title, description=None)
    section.text = text
    return section

def insert_new_section(title='foo', text='bar'):
    section = create_a_text_section(title, text)
    db.session.add(section)
    db.session.commit()
    return section

def create_a_variable(section_id=1):
    return TemplateVariables(template_id=1, section_id=section_id)

def insert_new_variable(section_id=None):
    if len(TemplateSection.query.all()) == 0 or section_id is None:
        section = insert_new_section('foo', 'bar')
        section_id = section.id
    variable = create_a_variable(section_id)
    db.session.add(variable)
    db.session.commit()
    return variable
