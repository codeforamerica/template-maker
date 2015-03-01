import json
import datetime
from flask import Blueprint, render_template, request, jsonify, abort

from template_maker.database import db
from template_maker.builder.models import TemplateBase, TemplateText, TemplateVariables

blueprint = Blueprint(
    'builder', __name__, url_prefix='/build',
    template_folder='../templates'
)

@blueprint.route('/')
def list_templates():
    return render_template('builder/list.html')

@blueprint.route('/new')
def new_template():
    return render_template('builder/new.html')

@blueprint.route('/edit/<int:template_id>/process')
def add_variables_to_template(template_id):
    # check if request is made async by checking if the angular header is present
    if 'XMLHttpRequest' in request.headers.get('X-Requested-With', ''):
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

    # if not, render the template
    return render_template('builder/process.html')

@blueprint.route('/new/save', methods=['POST'])
def save_new_template():

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
