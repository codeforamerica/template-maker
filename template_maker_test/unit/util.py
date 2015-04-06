import datetime
from template_maker.database import db
from template_maker.builder.models import (
    TemplateBase, TemplateSection, TextSection, TemplatePlaceholders
)
from template_maker.generator.models import DocumentBase, DocumentPlaceholder
from template_maker.users.models import User
from template_maker.data.documents import set_document_placeholders, get_document_placeholders

def create_a_template(title='test'):
    now = datetime.datetime.utcnow()
    return TemplateBase(created_at=now, updated_at=now, title=title, description='test')

def insert_new_template(title='test', published=False):
    template = create_a_template(title)
    template.published = published
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

def insert_placeholder_type():
    db.session.execute('''INSERT INTO placeholder_types VALUES (1, 'unicode')''')

def create_a_placeholder(section_id=1, template_id=1, full_name='[[BAR||BAZ]]', display_name='[[BAZ]]'):
    placeholder = TemplatePlaceholders(template_id=template_id, section_id=section_id)
    placeholder.full_name=full_name
    placeholder.display_name=display_name
    return placeholder

def insert_new_placeholder(section_id=None, template_id=1, full_name='[[BAR||BAZ]]', display_name='[[BAZ]]'):
    if len(TemplateSection.query.all()) == 0 or section_id is None:
        section = insert_new_section('foo', 'bar')
        section_id = section.id
    placeholder = create_a_placeholder(section_id, full_name=full_name, display_name=display_name)
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

def insert_new_document(template_id, name='test document'):
    now = datetime.datetime.utcnow()
    document = DocumentBase(
        created_at=now,
        updated_at=now,
        name=name,
        template_id=template_id
    )
    db.session.add(document)
    db.session.commit()
    return document

def create_document_with_placeholders():
    insert_placeholder_type()
    template = insert_new_template()
    placeholder = insert_new_placeholder()
    placeholder.type = 1
    template.section_order = [placeholder.section_id]
    document = insert_new_document(template.id)
    set_document_placeholders(template.id, document)
    return document
