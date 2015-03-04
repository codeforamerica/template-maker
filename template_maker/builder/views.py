import json
import datetime
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
from template_maker.builder.models import TemplateBase, TemplateText, TemplateVariables
from template_maker.builder.forms import TemplateBaseForm
from template_maker.builder.util import set_template_content

blueprint = Blueprint(
    'builder', __name__, url_prefix='/build',
    template_folder='../templates'
)

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
        return redirect('build/edit/{template_id}'.format(template_id=template_base_id))
    return render_template('builder/new.html', form=form)

@blueprint.route('/edit/<int:template_id>', methods=['GET', 'PUT', 'DELETE'])
def edit_template(template_id):
    '''
    Route for interacting with base templates

    GET - Gets the template and returns a 200 or returns a 404
    PUT - Updates the template and returns a 204 or returns a 403
    DELETE - Deletes the template (and cascades to delete
    template text and associated variables) and returns a 204
    or returns a 403
    '''
    template_base = TemplateBase.query.get(template_id)
    if request.method == 'GET':
        if template_base:
            return render_template('builder/edit.html')
        else:
            render_template('404.html')
    elif request.method == 'PUT':
        sections = json.loads(request.data)
        set_template_content(sections, template_id)
        return jsonify({'template_id': template_id}), 200
    elif request.method == 'DELETE':
        try:
            db.session.delete(template_base)
            db.session.commit()
            return Response(status=204)
        except:
            abort(403)

@blueprint.route('/edit/<int:template_id>/process')
def configure_variables(template_id):
    if TemplateBase.query.get(template_id):
        return render_template('builder/process.html')
    else:
        return render_template('404.html')

@blueprint.route('/data/templates/<int:template_id>')
def get_template_sections(template_id):
    if TemplateBase.query.get(template_id):
        template = db.session.execute(
            '''
            SELECT
                a.id as template_id, b.id as template_text_id, b.text,
                b.text_position, b.text_type
            FROM template_base a
            INNER JOIN template_text b
            on a.id = b.template_id
            WHERE a.id = :template_id
            ORDER BY b.text_position, b.id ASC
            ''',
            { 'template_id': template_id }
        ).fetchall()

        output = []

        for section in template:
            output.append({
                'type': section[4],
                'content': section[2]
            })

        return jsonify({'sections': output})
    else:
        return jsonify({
            'template': 'ERROR: Template Not Found'
        }), 404

@blueprint.route('/data/templates/<int:template_id>/process')
def get_template_sections_and_variables(template_id):
    # check if request is made async by checking if the angular header is present
    if TemplateBase.query.get(template_id):
        template = db.session.execute(
            '''
            SELECT
                a.id as template_id, b.id as template_text_id, b.text,
                b.text_position, b.text_type, ARRAY_AGG(c.name)
            FROM template_base a
            INNER JOIN template_text b
            ON a.id = b.template_id
            LEFT JOIN template_variables c
            ON a.id = c.template_id and b.id = c.template_text_id
            WHERE a.id = :template_id
            GROUP BY a.id, b.id, b.text, b.text_position, b.text_type
            ORDER BY b.text_position, b.id ASC
            ''',
            { 'template_id': template_id }
        ).fetchall()

        output = []

        for result in template:
            variables = [] if result[5] == [None] else result[5]
            output.append({
                'content': result[2],
                'variables': variables,
                'type': result[4]
            })

        return jsonify({
            'template': output
        })
    else:
        return jsonify({
            'template': 'ERROR: Template Not Found'
        }), 404

@blueprint.route('/tmp', methods=['POST'])
def update_template_text():
    try:
        # create our new TemplateBase object
        now = datetime.datetime.utcnow()
        sections = json.loads(request.data)
        template_base = TemplateBase(
            created_at = now,
            updated_at = now
            )
        db.session.add(template_base)
        db.session.commit()
        template_base_id = template_base.id

        for idx, section in enumerate(sections):
            template_section = TemplateText(
                text = section.get('content'),
                text_position = idx,
                text_type = section.get('type'),
                template_id = template_base_id
            )
            db.session.add(template_section)
            db.session.commit()
            template_text_id = template_section.id

            for variable in section.get('variables', []):
                template_variables = TemplateVariables(
                    name = variable,
                    template_id = template_base_id,
                    template_text_id = template_text_id
                )
                db.session.add(template_variables)
                db.session.commit()

        return jsonify({'template_id': template_base_id}), 201
    except:
        abort(403)
