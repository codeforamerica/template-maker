import json
import datetime
from flask import (
    Blueprint, request, Response, jsonify,
    render_template, redirect, abort, url_for
)

from template_maker.database import db
from template_maker.builder.models import TemplateBase, TemplateSection, TemplateVariables, VariableTypes
from template_maker.builder.forms import (
    TemplateBaseForm, TemplateSectionForm, TemplateSectionTextForm,
    VariableForm, SelectField, StringField
) 
from template_maker.builder.util import (
    create_new_section, update_section, update_variables,
    get_template_sections, get_template_variables
)

blueprint = Blueprint(
    'builder', __name__, url_prefix='/build',
    template_folder='../templates'
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

@blueprint.route('/<int:template_id>/edit', methods=['GET', 'PUT', 'DELETE'])
def delete_template():
    '''
    Route for managing individual template objects

    GET - TODO
    PUT - TODO
    DELETE - Deletes the template (and cascades to delete
    template text and associated variables) and returns a 204
    or returns a 403
    '''
    if request.method == 'DELETE':
        try:
            db.session.delete(template_base)
            db.session.commit()
            return Response(status=204)
        except:
            abort(403)

@blueprint.route('/<int:template_id>/section/new', methods=['GET', 'POST'])
def edit_template(template_id):
    '''
    Route for interacting with base templates

    GET - Gets the template and renders out the section editor view with
    a new section form pre-loaded
    POST - Creates a new section
    '''
    template_base = TemplateBase.query.get(template_id)

    if template_base is None:
        return render_template('404.html')

    new_section_form = TemplateSectionForm()

    if new_section_form.validate_on_submit():
        new_section = request.form
        new_section_id = create_new_section(new_section, template_id)
        return redirect(
            url_for('builder.edit_section', template_id=template_id, section_id=new_section_id)
        )
    else:
        sections = get_template_sections(template_id)
        return render_template(
            'builder/edit.html', template=template_base,
            sections=sections, new_section_form=new_section_form,
            edit_section=False
        )

@blueprint.route('/<int:template_id>/section/<int:section_id>', methods=['GET', 'POST', 'DELETE'])
def edit_section(template_id, section_id):
    '''
    Route for interacting with individual sections

    GET - Gets the template and renders out the editing for that particular section
    PUT - Updates the section
    DELETE - Deletes the section
    '''
    template_base = TemplateBase.query.get(template_id)
    section = TemplateSection.query.get(section_id)
    if template_base is None or section is None:
        return render_template('404.html')

    sections = get_template_sections(template_id)
    form = SECTION_FORM_MAP[section.section_type]()

    if form.validate_on_submit():
        update_section(section, template_id, request.form)
        return redirect(url_for(
            'builder.edit_section', template_id=template_id,
            section_id=section_id
        ))
    else:
        return render_template(
            'builder/edit.html', template=template_base,
            sections=sections, section=section,
            form=form
        )

# TODO: is there a way to cache this once per session as opposed
# to getting it from the database all the time?
def get_variable_types():
    return [
        (i.type, i.type) for i in VariableTypes.query.all()
    ]

@blueprint.route('/<int:template_id>/configure', methods=['GET', 'POST'])
def configure_variables(template_id):
    template_base = TemplateBase.query.get(template_id)
    if template_base is None:
        return render_template('404.html')

    class F(VariableForm):
        pass

    variables = get_template_variables(template_id)

    for variable in variables:
        setattr(F, variable.name, SelectField(variable.name, choices=get_variable_types()))

    form = F()
    if form.validate_on_submit():
        update_variables(variables, request.form, template_id)
        return redirect(url_for('builder.publish_template', template_id=template_id))

    sections = get_template_sections(template_id)
    return render_template(
        'builder/configure.html', template=template_base,
        sections=sections, variables=variables, form=form
    )

@blueprint.route('/edit/<int:template_id>/publish', methods=['GET', 'POST'])
def publish_template(template_id):
    '''
    Route for taking documents from the BUILDER and turning them into TEMPLATES via the GENERATOR

    GET - Returns the preview for the template
    POST - Data contains sections and variables. Publish freezes the current
    version of the template into new database tables, allowing the builder documents
    to be edited and create new templates later on.
    '''
    if request.method == 'GET':
        return render_template('builder/preview.html')
    elif request.method == 'POST':
        data = json.loads(request.data)
        # ensure all of the variables have types
        if not all([item.get('type') for sublist in data for item in sublist]):
            abort(403)
        else:
            # set the variable types
            set_variable_types(data, template_id)
            # set the publish flag to be true
            template = TemplateBase.query.get(template_id)
            template.published = True
            db.session.commit()
            return redirect(url_for('generator.list_templates'))
