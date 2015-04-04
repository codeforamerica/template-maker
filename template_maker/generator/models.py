from template_maker.database import (
    Column,
    Model,
    db,
    ReferenceCol
)

class DocumentBase(Model):
    '''
    Metadata about a new document, relates back to
    a template
    '''

    __tablename__ = 'document_base'
    id = Column(db.Integer, primary_key=True)
    created_at = Column(db.DateTime)
    updated_at = Column(db.DateTime)
    name = Column(db.String(255))
    template_id = ReferenceCol('template_base')

    def __init__(self, created_at, updated_at, name, template_id):
        self.created_at = created_at
        self.updated_at = updated_at
        self.name = name
        self.template_id = template_id

class DocumentPlaceholder(Model):
    '''
    A document's placeholder's value. Relates to the
    document and the placeholder
    '''

    __tablename__ = 'document_placeholder'
    id = Column(db.Integer, primary_key=True)
    document_id = ReferenceCol('document_base')
    placeholder_id = ReferenceCol('template_placeholders')
    value = Column(db.Text)

    def __init__(self, document_id, placeholder_id):
        self.document_id = document_id
        self.placeholder_id = placeholder_id
