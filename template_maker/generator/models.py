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
