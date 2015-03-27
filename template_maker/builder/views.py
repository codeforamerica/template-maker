from flask import (
    Blueprint, request, make_response,
    render_template, redirect, abort, url_for,
    flash, current_app
)

from flask.ext.login import current_user
from template_maker.extensions import login_manager
from template_maker.users.models import User

from template_maker.builder.forms import (
    TemplateBaseForm, TemplateSectionForm, TemplateSectionTextForm,
    PlaceholderForm, SelectField, StringField, Form
)

from template_maker.data.templates import (
    get_all_templates, get_single_template, delete_template, create_new_template, 
    publish_template as _publish_template
)
from template_maker.data.sections import (
    create_new_section, update_section, get_template_sections, reorder_sections,
    get_single_section, delete_section as _delete_section
)

from template_maker.data.placeholders import get_template_placeholders
from template_maker.builder.boilerplate import boilerplate as html_boilerplate

blueprint = Blueprint(
    'builder', __name__, url_prefix='/build',
    template_folder='../templates',
)

@login_manager.user_loader
def load_user(userid):
    return User.get_by_id(int(userid))

# restrict blueprint to only authenticated users
@blueprint.before_request
def restrict_access():
    if current_app.config.get('ENV') != 'test':
        if not current_user.is_authenticated() or current_user.is_anonymous():
            return redirect(url_for('users.login'))

SECTION_FORM_MAP = {
    'text': TemplateSectionTextForm,
    'fixed_text': TemplateSectionTextForm,
    'dummy': TemplateSectionForm
}

@blueprint.route('/')
def list_templates():
    '''
    Returns a list of all the templates.

    Because there is no interacton on this page, it uses
    Flask entirely
    '''
    templates = get_all_templates()
    output = []
    for template in templates:
        output.append({
            'id': template.id,
            'title': template.title,
            'description': template.description,
        })

    return render_template('builder/list.html', templates=output)

@blueprint.route('/new', methods=['GET', 'POST'])
def new_template():
    '''
    Returns the page for building a new template.
    '''
    form = TemplateBaseForm()
    if form.validate_on_submit():

        template_base_id = create_new_template(request.form)
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
    template text and associated placeholders) and returns a 204
    or returns a 403
    '''
    template_base = get_single_template(template_id)
    if request.args.get('method') == 'DELETE':
        if delete_template(template_base):
            return redirect(url_for('builder.list_templates'))
        return abort(403)

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
    template_base = get_single_template(template_id)
    current_section = get_single_section(section_id, template_id)
    if template_base is None or (current_section and current_section.template_id != template_id):
        return render_template('404.html')

    # handle re-ordering
    old_order = template_base.section_order
    if request.method == 'POST':
        request_sections = request.form.getlist('id')
        new_order = reorder_sections(template_base, request_sections) if len(request_sections) > 0 else None
    else:
        new_order = None

    # get the sections and initialize the forms
    sections = get_template_sections(template_base)
    form = SECTION_FORM_MAP[current_section.section_type]()
    new_section_form = TemplateSectionForm()

    # if the form is valid, go ahead and save everything
    if form.validate_on_submit():
        update_section(current_section, template_id, request.form)
        flash('Successfully saved!', 'alert-success')
        return redirect(url_for(
            'builder.edit_template', template_id=template_id
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
    template = get_single_template(template_id)
    if template.section_order and len(template.section_order) > 0:
        reorder_sections(template, template.section_order, to_delete=section_id)

    _delete_section(section_id, template_id)

    flash('Section successfully deleted!', 'alert-success')
    return redirect(url_for('builder.edit_template', template_id=template_id))

@blueprint.route('/<int:template_id>/publish', methods=['GET', 'POST'])
def publish_template(template_id):
    '''
    Route for taking documents from the BUILDER and turning them into TEMPLATES via the GENERATOR

    GET - Returns the preview for the template
    POST - Data contains sections and placeholders. Publish freezes the current
    version of the template into new database tables, allowing the builder documents
    to be edited and create new templates later on.
    '''
    template_base = get_single_template(template_id)
    if template_base is None:
        return render_template('404.html')
    if request.method == 'GET':
        sections = get_template_sections(template_base)
        return render_template('builder/preview.html', sections=sections, template=template_base, preview=True)
    elif request.method == 'POST':
        # set the publish flag to be true, set the section order
        template = _publish_template(template_id)
        reorder_sections(template, request.form.getlist('id'))
        return redirect(url_for('builder.list_templates'))
