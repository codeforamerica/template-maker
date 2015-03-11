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
    created_at = Column(db.DateTime)
    updated_at = Column(db.DateTime)
    title = Column(db.String(255))
    description = Column(db.Text)
    template_text = db.relationship('TemplateSection', cascade='all,delete', lazy='dynamic')
    template_variables = db.relationship('TemplateVariables', cascade='all,delete', lazy='dynamic')
    published = Column(db.Boolean, default=False)
    # created_by = ReferenceCol('users')

    def __init__(self, created_at, updated_at, title, description):
        self.created_at = created_at
        self.updated_at = updated_at
        self.title = title
        self.description = description

class TemplateSection(Model):
    '''
    TemplateSection is a superclass of section information and maps to section types

    Fields:
    - title: The name of the section
    - description: The description of the section
    - position: Where in the template the section lies
    - template_id: Foreign Key relationship back to the TemplateBase
    - section_type: The type of section to be used. This uses "joined
    table inheritance": http://docs.sqlalchemy.org/en/rel_0_9/orm/inheritance.html
    '''

    __tablename__ = 'template_section'
    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(255))
    description = Column(db.Text)
    template_id = ReferenceCol('template_base')
    template_variables = db.relationship('TemplateVariables', cascade='all,delete', lazy='dynamic')
    section_type = Column('section_type', db.String(50))
    __mapper_args__ = {'polymorphic_on': section_type}

    def __init__(self, template_id=None, title=None, description=None):
        self.template_id = template_id
        self.title = title
        self.description = description

class TextSection(TemplateSection):
    '''
    TextSection is a class of TemplateSection; it supports large text input with
    variable interpolation

    Fields:
    - id: 1:1 Relationship from TemplateSection
    - text: Text of the section
    '''
    __tablename__ = 'text_section'
    section_id = Column(db.Integer, db.ForeignKey('template_section.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'text',
        'inherit_condition': (section_id == TemplateSection.id)
    }
    text = Column(db.Text)
    choice_type = ('text', 'Text Section')

    def __init__(self, title, description, template_id):
        super(TextSection, self).__init__(template_id=template_id, title=title, description=description)

class FixedTextSection(TemplateSection):
    '''
    FixedTextSection is a class of TemplateSection. It does not allow document generators
    to interpolate variables.

    - id: 1:1 Relationship from TemplateSection
    - text: Text of the section
    '''
    __tablename__ = 'fixed_text_section'
    section_id = Column(db.Integer, db.ForeignKey('template_section.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'fixed_text',
        'inherit_condition': (section_id == TemplateSection.id)
    }
    text = Column(db.Text)
    choice_type = ('fixed_text', 'Fixed Text Section')

    def __init__(self, title, description, template_id):
        super(FixedTextSection, self).__init__(template_id=template_id, title=title, description=description)


# A list of all implemented section types for a new section CHOICES field
IMPLEMENTED_SECTIONS = [cls.choice_type for cls in vars()['TemplateSection'].__subclasses__()]

class VariableTypes(Model):
    '''
    The types associated with different variables. We use a FK
    constraint to make sure it's one of the approved tyes

    Fields:
    - type: The name of the type in question
    '''
    __tablename__ = 'variable_types'
    id = Column(db.Integer, primary_key=True)
    type = Column(db.Text)

class TemplateVariables(Model):
    '''
    The variables associated with each section

    Fields:
    - name: The actual name of the variable
    - template_id: Foreign Key back to the TemplateBase model
    - section_id: Foreign Key back to the TemplateSection model
    '''

    __tablename__ = 'template_variables'
    id = Column(db.Integer, primary_key=True)
    name = Column(db.Text)
    type = Column(db.Integer, db.ForeignKey('variable_types.id'))
    template_id = ReferenceCol('template_base')
    section_id = ReferenceCol('template_section')

    def __init__(self, name=None, template_id=None, section_id=None):
        self.name = name
        self.template_id = template_id
        self.section_id = section_id
