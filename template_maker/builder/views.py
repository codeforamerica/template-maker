import json
import datetime
from flask import (
    Blueprint, request, make_response, jsonify,
    render_template, redirect, abort, url_for,
    flash
)
from sqlalchemy.dialects.postgresql import array

from template_maker.database import db
from template_maker.builder.models import TemplateBase, TemplateSection, TemplateVariables, VariableTypes
from template_maker.builder.forms import (
    TemplateBaseForm, TemplateSectionForm, TemplateSectionTextForm,
    VariableForm, SelectField, StringField, Form
)
from template_maker.builder.util import (
    create_new_section, update_section,
    get_template_sections, get_template_variables, reorder_sections
)
from template_maker.builder.boilerplate import boilerplate as html_boilerplate


blueprint = Blueprint(
    'builder', __name__, url_prefix='/build',
    template_folder='../templates',
)

SECTION_FORM_MAP = {
    'text': TemplateSectionTextForm,
    'fixed_text': TemplateSectionTextForm
}

# GET-only "data" routes for client-side interactions

@blueprint.route('/')
def list_templates():
    '''
    Returns a list of all the templates.

    Because there is no interacton on this page, it uses
    Flask entirely
    '''
    templates = TemplateBase.query.all()
    output = []
    for template in templates:
        output.append({
            'id': template.id,
            'title': template.title,
            'description': template.description,
            'num_vars': template.template_variables.count()
        })

    return render_template('builder/list.html', templates=output)

@blueprint.route('/new', methods=['GET', 'POST'])
def new_template():
    '''
    Returns the page for building a new template.
    '''
    form = TemplateBaseForm()
    if form.validate_on_submit():
        now = datetime.datetime.utcnow()
        template_base = TemplateBase(
            created_at = now,
            updated_at = now,
            title = request.form.get('title'),
            description = request.form.get('description')
        )
        db.session.add(template_base)
        db.session.commit()
        template_base_id = template_base.id
        return redirect(
            url_for('builder.edit_template', template_id=template_base_id)
        )
    return render_template('builder/new.html', form=form)

@blueprint.route('/<int:template_id>/section/new/<section_type>')
def new_section(template_id, section_type=None):
    new_section = { 'type': section_type, 'title': request.args.get('section_title', '') }
    if request.args.get('boilerplate', False):
        new_section['html'] = html_boilerplate.get(request.args.get('boilerplate'), 'Please insert your text here.')
    new_section_id = create_new_section(new_section, template_id)

    if new_section_id:
        return redirect(
            url_for('builder.edit_template', template_id=template_id, section_id=new_section_id)
        )
    return abort(403)

@blueprint.route('/<int:template_id>/edit', methods=['GET', 'PUT', 'DELETE'])
def edit_template_metadata(template_id):
    '''
    Route for managing individual template objects

    methods can be request-level or come from the request args
    GET - TODO
    PUT - TODO
    DELETE - Deletes the template (and cascades to delete
    template text and associated variables) and returns a 204
    or returns a 403
    '''
    template_base = TemplateBase.query.get(template_id)
    if request.args.get('method') == 'DELETE':
        db.session.delete(template_base)
        db.session.commit()
        return redirect(url_for('builder.list_templates'))

@blueprint.route('/<int:template_id>/')
def redirect_to_section(template_id):
    return redirect(url_for('builder.edit_template', template_id=template_id))

@blueprint.route('/<int:template_id>/section/', methods=['GET', 'POST'])
@blueprint.route('/<int:template_id>/section/<int:section_id>', methods=['GET', 'POST'])
def edit_template(template_id, section_id=None, section_type=None):
    '''
    Route for interacting with individual sections

    GET - Gets the template and renders out the editing for that particular section
    POST - Updates a section
    '''
    template_base = TemplateBase.query.get(template_id)
    section = TemplateSection.query.get(section_id) if section_id else None
    if (template_base is None or section is None or section.template_id != template_id) and section_id > 0:
        return render_template('404.html')
    # if we don't have a section, set up a dummy section
    current_section = section if section else { 'id': 0, 'type': 'dummy' }

    # handle re-ordering
    old_order = template_base.section_order
    if request.method == 'POST':
        request_sections = request.form.getlist('id')
        new_order = reorder_sections(template_base, request_sections) if len(request_sections) > 0 else None
    else:
        new_order = None

    # get the sections and initialize the forms
    sections = get_template_sections(template_base)
    form = SECTION_FORM_MAP[section.section_type]() if section else TemplateSectionForm()
    new_section_form = TemplateSectionForm()

    # if the form is valid, go ahead and save everything
    if form.validate_on_submit():
        update_section(section, template_id, request.form)
        flash('Successfully saved!', 'alert-success')
        return redirect(url_for(
            'builder.edit_template', template_id=template_id,
            section_id=section_id
        ))
    elif request.method == 'POST':
        if new_order and new_order != old_order:
            flash('Successfully saved!', 'alert-success')
        if section_id == 0:
            return redirect(url_for('builder.edit_template', template_id=template_id))
        else:
            return redirect(url_for('builder.edit_template', 
                template_id=template_id, section_id=section_id
            ))

    response = make_response(render_template(
        'builder/edit.html', template=template_base,
        sections=sections, form=form,
        new_section_form=new_section_form,
        current_section=current_section
    ))
    return response

@blueprint.route('/<int:template_id>/section/<int:section_id>/delete')
def delete_section(template_id, section_id):
    template = TemplateBase.query.get(template_id)
    if template.section_order:

        if section_id in template.section_order:
            template.section_order.remove(section_id)

        # cast it to a sqlalchemy array type to ensure
        # the commit works properly
        new_order = array(template.section_order)
        template.section_order = new_order
        db.session.commit()

    section = TemplateSection.query.get(section_id)
    db.session.delete(section)
    db.session.commit()
    flash('Section successfully deleted!', 'alert-success')
    return redirect(url_for('builder.edit_template', template_id=template_id))

@blueprint.route('/<int:template_id>/publish', methods=['GET', 'POST'])
def publish_template(template_id):
    '''
    Route for taking documents from the BUILDER and turning them into TEMPLATES via the GENERATOR

    GET - Returns the preview for the template
    POST - Data contains sections and variables. Publish freezes the current
    version of the template into new database tables, allowing the builder documents
    to be edited and create new templates later on.
    '''
    template_base = TemplateBase.query.get(template_id)
    if template_base is None:
        return render_template('404.html')
    if request.method == 'GET':
        sections = get_template_sections(template_base)
        return render_template('builder/preview.html', sections=sections, template=template_base, preview=True)
    elif request.method == 'POST':
        # set the publish flag to be true, set the section order
        template = TemplateBase.query.get(template_id)
        template.published = True
        reorder_sections(template, request.form.getlist('id'))
        return redirect(url_for('generator.build_document', template_id=template.id))
