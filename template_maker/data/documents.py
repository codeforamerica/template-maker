import datetime
from template_maker.database import db
from template_maker.generator.models import DocumentBase
from template_maker.builder.models import TemplateBase

def get_all_documents():
    '''
    Returns all documents currently being edited
    '''
    return DocumentBase.query.all()

def get_documents_and_parent_templates():
    return db.session.query(
        DocumentBase.id, DocumentBase.name, TemplateBase.title
    ).filter(DocumentBase.template_id==TemplateBase.id).all()

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

def create_new_document(template_id, data):
    now = datetime.datetime.utcnow()
    document_base = DocumentBase(
        created_at=now,
        updated_at=now,
        name=data.get('name'),
        template_id=template_id
    )

    db.session.add(document_base)
    db.session.commit()

    return document_base.id

def delete_document(document):
    db.session.delete(document)
    db.session.commit()
    return True
