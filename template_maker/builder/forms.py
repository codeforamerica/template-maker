from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class TemplateBaseForm(Form):
    '''
    Simple form for creating a new template
    '''
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])