import re
import string
from flask import (
    Blueprint, request, render_template,
    redirect, url_for, abort
)

from wtforms import TextField, IntegerField, FloatField
from template_maker.builder.forms import PlaceholderForm
from template_maker.generator.forms import DatePickerField, DocumentBaseForm
from template_maker.data.templates import get_single_template, get_published_templates
from template_maker.data.sections import get_template_sections
from template_maker.data.placeholders import get_section_placeholders
from template_maker.data.documents import (
    create_new_document, get_single_document,
    get_documents_and_parent_templates, delete_document
)

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
    templates = get_published_templates()
    return render_template('generator/list.html', templates=templates)

@blueprint.route('/edit')
def in_progress_documents():
    '''
    Returns a list of all currently created documents.
    '''
    documents = get_documents_and_parent_templates()
    return render_template('generator/in-progress-list.html', documents=documents)

@blueprint.route('/edit/<int:document_id>', methods=['GET', 'POST'])
def edit_in_progress_document(document_id):
    '''
    Allows updating and deleting of individual documents.
    '''
    document_base = get_single_document(document_id)
    if request.args.get('method') == 'DELETE':
        if delete_document(document_base):
            return redirect(url_for('generator.in_progress_documents'))
        return abort(403)

@blueprint.route('/new/from-template-<int:template_id>', methods=['GET', 'POST'])
def new_document(template_id):
    '''
    View handling the creation of new documents from templates

    GET - Returns the new document form
    POST - Creates a new document from a template
    '''
    template = get_single_template(template_id)
    form = DocumentBaseForm()
    if form.validate_on_submit():
        document_base_id = create_new_document(template_id, request.form)
        return redirect(
            url_for('generator.edit_document_sections', document_id=document_base_id)
        )

    return render_template('generator/new.html', form=form, template=template)

def strip_tags(name):
    '''
    Takes a placeholder name and strips out the tags
    '''
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    name = re.sub(regex, "", name)
    return name

def generate_class(placeholder):
    _class = 'template-placeholder'
    if placeholder.type == 2:
        _class += ' datepicker'
    return _class

def create_rivets_bindings(placeholder, section):
    '''
    Converts a placeholder into a <span> that rivets can grab onto
    '''
    repl_text = '<input id="{placeholder_name}-value" placeholder="{placeholder_name}"'.format(
        placeholder_name=strip_tags(placeholder.display_name)
    ) + \
    'class="' + generate_class(placeholder) + '" rv-value="template.placeholder_{idcombo}" >'.format(
        idcombo=strip_tags(placeholder.display_name)
    )
    return re.sub(re.escape(placeholder.full_name), repl_text, section.text)

@blueprint.route('/<int:document_id>/edit')
@blueprint.route('/<int:document_id>/edit/<int:section_id>')
def edit_document_sections(document_id, section_id=None):
    '''
    View to handle building a new RFP document

    GET - Returns a new document generator based on the template
    POST - TODO
    '''
    document_base = get_single_document(document_id)
    template_base = get_single_template(document_base.template_id)
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
                setattr(
                    F,
                    placeholder.display_name,
                    TYPE_VARIABLES_MAP[placeholder.type](placeholder.display_name)
                )

    form = F()
    for field in form.__iter__():
        # set the rv_data_input value on the form field as well as on the placeholder
        setattr(field, 'rv_data_input', 'template.placeholder_' + strip_tags(field.name))
        setattr(field, 'label', strip_tags(field.name))

    return render_template('generator/build-document.html', document=document_base,
        template=template_base, sections=sections, placeholders=placeholders, form=form)
