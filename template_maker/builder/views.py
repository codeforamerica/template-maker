from flask import Blueprint, render_template

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
