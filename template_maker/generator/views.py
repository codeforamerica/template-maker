import re
import string

from flask import (
    Blueprint, request, render_template,
    redirect, url_for, abort, flash
)
from flask.ext.wtf import Form
from wtforms import TextField, IntegerField, FloatField, validators

from template_maker.generator.forms import DatePickerField, DocumentBaseForm
from template_maker.data import (
    templates as tp, sections as sc,
    documents as dm
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
    templates = tp.get_published_templates()
    return render_template('generator/list.html', templates=templates)

@blueprint.route('/edit')
def in_progress_documents():
    '''
    Returns a list of all currently created documents.
    '''
    documents = dm.get_documents_and_parent_templates()
    return render_template('generator/in-progress-list.html', documents=documents)

@blueprint.route('/edit/<int:document_id>', methods=['GET', 'POST'])
def edit_in_progress_document(document_id):
    '''
    Allows updating and deleting of individual documents.
    '''
    document_base = dm.get_single_document(document_id)
    if request.args.get('method') == 'DELETE':
        if dm.delete_document(document_base):
            return redirect(url_for('generator.in_progress_documents'))
        return abort(403)

@blueprint.route('/new/from-template-<int:template_id>', methods=['GET', 'POST'])
def new_document(template_id):
    '''
    View handling the creation of new documents from templates

    GET - Returns the new document form
    POST - Creates a new document from a template
    '''
    template = tp.get_single_template(template_id)
    form = DocumentBaseForm()
    if form.validate_on_submit():
        document_base_id = dm.create_new_document(template_id, request.form)
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

def create_rivets_bindings(placeholder, section_text):
    '''
    Converts a placeholder into a <span> that rivets can grab onto
    '''
    repl_text = '<input id="{placeholder_display_name}" placeholder="{placeholder_name}"'.format(
        placeholder_name=strip_tags(placeholder.display_name),
        placeholder_display_name=placeholder.display_name
    ) + \
    ' name="{placeholder_name}"'.format(placeholder_name=placeholder.display_name) + \
    ' class="' + generate_class(placeholder) + '" rv-value="template.placeholder_{idcombo}"'.format(
        idcombo='_'.join(strip_tags(placeholder.display_name).split())
    ) + \
    'value="{placeholder_value}">'.format(placeholder_value=placeholder.value)
    new_text = re.sub(re.escape(placeholder.full_name), repl_text, section_text)
    return new_text

@blueprint.route('/<int:document_id>/edit', methods=['GET', 'POST'])
@blueprint.route('/<int:document_id>/edit/<int:section_id>', methods=['GET', 'POST'])
def edit_document_sections(document_id, section_id=None):
    '''
    View to handle building a new RFP document

    GET - Returns a new document generator based on the template
    POST - TODO
    '''
    document_base = dm.get_single_document(document_id)
    template_base = tp.get_single_template(document_base.template_id)

    if template_base is None or document_base is None:
        return render_template('404.html')

    if section_id is None:
        return redirect(url_for(
            'generator.edit_document_sections', document_id=document_id,
            section_id=template_base.section_order[0]
        ))

    sections = sc.get_template_sections(template_base)
    current_section = sc.get_single_section(section_id, template_base.id)
    placeholders = dm.get_document_placeholders(current_section.id)

    class F(Form):
        pass

    if current_section.section_type == 'text':
        # if we have a text section, we need to prep the page for the rivets
        # two-way data binding
        current_section_text = current_section.text
        for placeholder in placeholders:
            # add a data_input value onto the placeholder
            placeholder.rv_data_input = 'placeholder_' + '_'.join(strip_tags(placeholder.display_name).split())
            # format the section text
            current_section_text = create_rivets_bindings(placeholder, current_section_text)
            # set up the form
            setattr(
                F, placeholder.display_name,
                TYPE_VARIABLES_MAP[placeholder.type](placeholder.display_name, validators=[validators.Optional()])
            )

    form = F()

    if form.validate_on_submit():
        dm.save_document_section(placeholders, request.form)
        flash('Changes successfully saved!', 'alert-success')
        return redirect(url_for(
            'generator.edit_document_sections', document_id=document_base.id, section_id=current_section.id)
        )
    for field in form.__iter__():
        # set the rv_data_input value on the form field as well as on the placeholder
        setattr(field, 'rv_data_input', 'template.placeholder_' + '_'.join(strip_tags(field.name).split()))
        setattr(field, 'label', strip_tags(field.name))

    return render_template('generator/build-document.html',
        document=document_base, template=template_base,
        sections=sections, placeholders=placeholders,
        current_section=current_section,
        current_section_text=current_section_text or None,
        form=form
    )
