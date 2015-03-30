import datetime
from template_maker.database import db
from template_maker.builder.models import (
    TemplateBase, TemplateSection, TextSection, TemplatePlaceholders
)
from template_maker.users.models import User

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

def create_a_placeholder(section_id=1):
    return TemplatePlaceholders(template_id=1, section_id=section_id)

def insert_new_placeholder(section_id=None):
    if len(TemplateSection.query.all()) == 0 or section_id is None:
        section = insert_new_section('foo', 'bar')
        section_id = section.id
    placeholder = create_a_placeholder(section_id)
    db.session.add(placeholder)
    db.session.commit()
    return placeholder

def create_a_user(is_admin, email='foo@foo.com'):
    return User(email=email, first_name='foo', last_name='foo', is_admin=is_admin)

def insert_a_user(is_admin=False, email='foo@foo.com'):
    user = create_a_user(is_admin, email)
    db.session.add(user)
    db.session.commit()
    return user.id
