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
    title = StringField('Title')
    type = SelectField('Type', choices=IMPLEMENTED_SECTIONS)

class FroalaWidget(widgets.TextArea):
    '''
    Custom CKEditor Text Area Widget
    '''
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'froala')
        kwargs.setdefault('style', 'display:none;')
        return super(FroalaWidget, self).__call__(field, **kwargs)

class FroalaField(TextAreaField):
    widget = FroalaWidget()

class TemplateSectionTextForm(Form):
    '''
    WYSIWYG Editor for the TextSection and FixedTextSection Models
    '''
    title = StringField('Title')
    widget = FroalaField()

class VariableForm(Form):
    '''
    Since the number of variable differ from template to template, we
    just pass a blank form to get CSRF protection. In the view, we
    use dynamic form generation as laid out here:
    https://groups.google.com/forum/#!topic/wtforms/cJl3aqzZieA
    '''
    pass
