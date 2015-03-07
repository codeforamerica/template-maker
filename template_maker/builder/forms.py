from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired

from template_maker.builder.models import IMPLEMENTED_SECTIONS

class TemplateBaseForm(Form):
    '''
    Simple form for creating a new template
    '''
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])

class TemplateSectionForm(Form):
    '''
    Simple form for creating adding a new template section
    '''
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    type = SelectField('Type', choices=IMPLEMENTED_SECTIONS, validators=[DataRequired()])
