import datetime
from template_maker.database import db
from template_maker.builder.models import TemplateBase

def get_all_templates():
    '''
    Returns all templates
    '''
    return TemplateBase.query.all()

def get_published_templates():
    '''
    Returns published templates
    '''
    return TemplateBase.query.filter(TemplateBase.published==True).all()

def get_single_template(template_id):
    '''
    Returns a single template from a template_id
    '''
    return TemplateBase.query.get(template_id)

def create_new_template(data):
    '''
    Creates a new template from a dictionary or request.form
    object
    '''
    now = datetime.datetime.utcnow()
    template_base = TemplateBase(
        created_at = now,
        updated_at = now,
        title = data.get('title'),
        description = data.get('description')
    )
    db.session.add(template_base)
    db.session.commit()

    return template_base.id

def delete_template(template):
    '''
    Deletes the passed Template object
    '''
    db.session.delete(template)
    db.session.commit()
    return True

def publish_template(template_id):
    template = get_single_template(template_id)
    template.published = True
    return template
