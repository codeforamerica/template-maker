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
    created_at = Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = ReferenceCol('users')

class TemplateText(Model):

    __tablename__ = 'template_text'
    text = Column(db.Text)
    text_position = Column(db.Integer)
    text_type = Column(db.String(255))
    template_id = ReferenceCol('template_base')

class TemplateVariables(Model):

    __tablename__ = 'template_variables'
    name = Column(db.Text)
    template_id = ReferenceCol('template_base')
