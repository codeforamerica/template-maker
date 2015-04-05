import datetime
from template_maker.database import db
from template_maker.generator.models import DocumentBase, DocumentPlaceholder
from template_maker.builder.models import TemplateBase
from template_maker.data.placeholders import get_template_placeholders, TemplatePlaceholders

def get_all_documents():
    '''
    Returns all documents currently being edited
    '''
    return DocumentBase.query.all()

def get_documents_and_parent_templates():
    return db.session.query(
        DocumentBase.id, DocumentBase.name, TemplateBase.title
    ).filter(DocumentBase.template_id==TemplateBase.id).all()

def get_document_placeholders(document_id):
    '''
    Gets all the placeholders associated with a document
    '''
    return db.session.query(
        DocumentPlaceholder.id, TemplatePlaceholders.full_name, TemplatePlaceholders.type,
        TemplatePlaceholders.display_name, DocumentPlaceholder.value
    ).filter(DocumentPlaceholder.document_id==document_id).filter(
        DocumentPlaceholder.placeholder_id==TemplatePlaceholders.id
    ).all()

def get_single_document(document_id):
    '''
    Returns a single document from a template_id
    '''
    return DocumentBase.query.get(document_id)

def get_single_document_and_parent_template(document_id):
    return db.session.query(
        DocumentBase.id, DocumentBase.name, TemplateBase.title
    ).filter(DocumentBase.template_id==TemplateBase.id).filter(
        DocumentBase.id==document_id
    ).all()

def set_document_placeholders(template_id, document_base):
    # create the placeholders for the document
    placeholders = get_template_placeholders(template_id)
    for placeholder in placeholders:
        _placeholder = DocumentPlaceholder(
            document_id=document_base.id,
            placeholder_id=placeholder.id,
        )
        db.session.add(_placeholder)
    db.session.commit()

def create_new_document(template_id, data):
    now = datetime.datetime.utcnow()

    # create the document
    document_base = DocumentBase(
        created_at=now,
        updated_at=now,
        name=data.get('name'),
        template_id=template_id
    )
    db.session.add(document_base)
    db.session.commit()

    set_document_placeholders(template_id, document_base)

    return document_base.id

def save_document_section(document, section, placeholders, data):
    for placeholder in placeholders:
        _placeholder = DocumentPlaceholder.query.get(placeholder.id)
        _placeholder.value = data.get(placeholder.display_name, '')
        db.session.commit()

    return True

def delete_document(document):
    db.session.delete(document)
    db.session.commit()
    return True
