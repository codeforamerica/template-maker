import datetime
from template_maker.database import (
    Column,
    Model,
    db,
    ReferenceCol,
)
from template_maker.user.models import User

class TemplateBase(Model):
    '''
    Basic metadata about a template

    Fields:
    - created_at: when the template was created
    - updated_at: when the template metadata was last updated
    - title: the displayed title or name of the template
    - description: a freetext description of the template
    '''

    __tablename__ = 'template_base'
    id = Column(db.Integer, primary_key=True)
    created_at = Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(db.DateTime, default=datetime.datetime.utcnow)
    title = Column(db.String(255))
    description = Column(db.Text)
    template_text = db.relationship('TemplateText', cascade='all,delete', lazy='dynamic')
    template_variables = db.relationship('TemplateVariables', cascade='all,delete', lazy='dynamic')
    published = Column(db.Boolean, default=False)
    # created_by = ReferenceCol('users')

    def __init__(self, created_at, updated_at, title, description):
        self.created_at = created_at
        self.updated_at = updated_at
        self.title = title
        self.description = description

class TemplateText(Model):
    '''
    The sections and text associated with each template

    Fields:
    - text: The actual text of each section
    - text_position: The position of the section in this particular template
    - text_type: What type of text the section is (title, for example)
    - template_id: Foreign Key back to the TemplateBase model
    '''

    __tablename__ = 'template_text'
    id = Column(db.Integer, primary_key=True)
    text = Column(db.Text)
    text_position = Column(db.Integer)
    text_type = Column(db.String(255))
    template_id = ReferenceCol('template_base')
    template_variables = db.relationship('TemplateVariables', cascade='all,delete', lazy='dynamic')

    def __init__(self, text=None, text_position=None, text_type=None, template_id=None):
        self.text = text
        self.text_position = text_position
        self.text_type = text_type
        self.template_id = template_id

class VariableType(Model):
    '''
    The types associated with different variables. We use a FK
    constraint to make sure it's one of the approved tyes

    Fields:
    - types: The name of the type in question
    '''
    __tablename__ = 'variable_types'
    id = Column(db.Integer, primary_key=True)
    types = Column(db.Text)

class TemplateVariables(Model):
    '''
    The variables associated with each section

    Fields:
    - name: The actual name of the variable
    - template_id: Foreign Key back to the TemplateBase model
    - template_text_id: Foreign Key back to the TemplateText model
    '''

    __tablename__ = 'template_variables'
    id = Column(db.Integer, primary_key=True)
    name = Column(db.Text)
    type = Column(db.Integer, db.ForeignKey('variable_types.id'))
    template_id = ReferenceCol('template_base')
    template_text_id = ReferenceCol('template_text')

    def __init__(self, name=None, template_id=None, template_text_id=None):
        self.name = name
        self.template_id = template_id
        self.template_text_id = template_text_id
