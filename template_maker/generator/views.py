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
from template_maker.builder.forms import VariableForm
from template_maker.generator.forms import DatePickerField
from template_maker.builder.util import get_template_sections, get_section_variables

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
    Takes a variable name and strips out the tags
    '''
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    name = re.sub(regex, "", name)
    return "_".join(name.split())

def create_rivets_bindings(variable, section):
    '''
    Converts a variable into a <span> that rivets can grab onto
    '''
    repl_text = '<input id="{variable_name}-value" placeholder="{variable_name}"'.format(variable_name=strip_tags(variable.display_name)) + \
    'class="template-variable" rv-value="template.variable_{idcombo}" disabled>'.format(idcombo=strip_tags(variable.display_name))
    return re.sub(re.escape(variable.full_name), repl_text, section.text)

@blueprint.route('/<int:template_id>/generate')
def build_document(template_id):
    '''
    View to handle building a new RFP document

    GET - Returns a new document generator based on the template
    POST - TODO
    '''
    template_base = TemplateBase.query.get(template_id)
    sections = get_template_sections(template_base)
    class F(VariableForm):
        pass

    for section in sections:
        if section.section_type == 'text':
            # if we have a text section, we need to prep the page for the rivets
            # two-way data binding
            variables = get_section_variables(section.id)
            for variable in variables:
                # add a data_input value onto the variable
                variable.rv_data_input = 'variable_' + strip_tags(variable.display_name)
                # format the section text
                section.text = create_rivets_bindings(variable, section)
                # set up the form
                setattr(F, variable.display_name, TYPE_VARIABLES_MAP[variable.type](variable.display_name))

    form = F()
    for field in form.__iter__():
        # set the rv_data_input value on the form field as well as on the variable
        setattr(field, 'rv_data_input', 'template.variable_' + strip_tags(field.name))
        setattr(field, 'label', strip_tags(field.name))

    return render_template('generator/build-document.html', sections=sections, variables=variables, form=form)

