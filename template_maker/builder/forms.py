from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SelectField, widgets
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

class CKTextAreaWidget(widgets.TextArea):
    '''
    Custom CKEditor Text Area Widget
    '''
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()

class TemplateSectionTextForm(Form):
    '''
    WYSIWYG Editor for the TextSection and FixedTextSection Models
    '''
    widget = CKTextAreaField()