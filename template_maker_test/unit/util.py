import datetime
from template_maker.database import db
from template_maker.builder.models import (
    TemplateBase, TextSection
)

def create_a_template():
    now = datetime.datetime.utcnow()
    return TemplateBase(created_at=now, updated_at=now, title='test', description='test')

def insert_new_template():
    template = create_a_template()
    db.session.add(template)
    db.session.commit()
    return template.id

def create_a_text_section(title, text):
    section = TextSection(template_id=1, title=title, description=None)
    section.text = text
    return section

def insert_new_section(title='foo', text='bar'):
    section = create_a_text_section(title, text)
    db.session.add(section)
    db.session.commit()
    return section.id