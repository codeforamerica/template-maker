import datetime
from template_maker.database import (
    Column,
    Model,
    db,
    ReferenceCol
)
from template_maker.user.models import User

class TemplateBase(Model):

    __tablename__ = 'template_base'
    id = Column(db.Integer, primary_key=True)
    created_at = Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(db.DateTime, default=datetime.datetime.utcnow)
    template_text = db.relationship('TemplateText', cascade='all,delete', lazy='dynamic')
    template_variables = db.relationship('TemplateVariables', cascade='all,delete', lazy='dynamic')
    # created_by = ReferenceCol('users')

    def __init__(self, created_at, updated_at):
        self.created_at = created_at
        self.updated_at = updated_at

class TemplateText(Model):

    __tablename__ = 'template_text'
    id = Column(db.Integer, primary_key=True)
    text = Column(db.Text)
    text_position = Column(db.Integer)
    text_type = Column(db.String(255))
    template_id = ReferenceCol('template_base')
    template_variables = db.relationship('TemplateVariables', cascade='all,delete', lazy='dynamic')

    def __init__(self, text, text_position, text_type, template_id):
        self.text = text
        self.text_position = text_position
        self.text_type = text_type
        self.template_id = template_id

class TemplateVariables(Model):

    __tablename__ = 'template_variables'
    id = Column(db.Integer, primary_key=True)
    name = Column(db.Text)
    template_id = ReferenceCol('template_base')
    template_text_id = ReferenceCol('template_text')

    def __init__(self, name, template_id, template_text_id):
        self.name = name
        self.template_id = template_id
        self.template_text_id = template_text_id
