import re
import string
from flask import (
    Blueprint,
    request,
    Response,
    jsonify,
    render_template,
    redirect,
    abort
)

from template_maker.database import db
from template_maker.builder.models import TemplateBase
from wtforms import TextField, IntegerField, FloatField
from template_maker.builder.forms import PlaceholderForm
from template_maker.generator.forms import DatePickerField
from template_maker.data.sections import get_template_sections
from template_maker.data.placeholders import get_section_placeholders

TYPE_VARIABLES_MAP = {
    1: TextField, 2: DatePickerField, 3: IntegerField, 4: FloatField
}

blueprint = Blueprint(
    'generator', __name__, url_prefix='/generate',
    template_folder='../templates'
)

@blueprint.route('/')
def list_templates():
    '''
    Returns a list of all the templates.

    Because there is no interacton on this page, it uses
    Flask entirely
    '''
    templates = TemplateBase.query.filter(TemplateBase.published==True).all()
    return render_template('generator/list.html', templates=templates)

def strip_tags(name):
    '''
    Takes a placeholder name and strips out the tags
    '''
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    name = re.sub(regex, "", name)
    return "_".join(name.split())

def create_rivets_bindings(placeholder, section):
    '''
    Converts a placeholder into a <span> that rivets can grab onto
    '''
    repl_text = '<input id="{placeholder_name}-value" placeholder="{placeholder_name}"'.format(placeholder_name=strip_tags(placeholder.display_name)) + \
    'class="template-placeholder" rv-value="template.placeholder_{idcombo}" disabled>'.format(idcombo=strip_tags(placeholder.display_name))
    return re.sub(re.escape(placeholder.full_name), repl_text, section.text)

@blueprint.route('/<int:template_id>/generate')
def build_document(template_id):
    '''
    View to handle building a new RFP document

    GET - Returns a new document generator based on the template
    POST - TODO
    '''
    template_base = TemplateBase.query.get(template_id)
    sections = get_template_sections(template_base)
    class F(PlaceholderForm):
        pass

    for section in sections:
        if section.section_type == 'text':
            # if we have a text section, we need to prep the page for the rivets
            # two-way data binding
            placeholders = get_section_placeholders(section.id)
            for placeholder in placeholders:
                # add a data_input value onto the placeholder
                placeholder.rv_data_input = 'placeholder_' + strip_tags(placeholder.display_name)
                # format the section text
                section.text = create_rivets_bindings(placeholder, section)
                # set up the form
                setattr(F, placeholder.display_name, TYPE_VARIABLES_MAP[placeholder.type](placeholder.display_name))

    form = F()
    for field in form.__iter__():
        # set the rv_data_input value on the form field as well as on the placeholder
        setattr(field, 'rv_data_input', 'template.placeholder_' + strip_tags(field.name))
        setattr(field, 'label', strip_tags(field.name))

    return render_template('generator/build-document.html', 
        template=template_base, sections=sections, placeholders=placeholders, form=form)
