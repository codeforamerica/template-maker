from flask import Blueprint, render_template, request, jsonify

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
        return jsonify({'template': [
            {
                'content': 'Test Sentence',
                'type': 'title',
                'template_id': 1
            },
            {
                'content': 'The quick brown {{ animal }} and gray {{ animal }} jump over the lazy {{ animal2 }} on {{ date }}.',
                'variables': ['animal', 'animal2', 'date'],
                'type': 'section',
                'template_id': 1
            }
        ]})

    # if not, render the template
    return render_template('builder/process.html')

@blueprint.route('/new/save', methods=['POST'])
def save_new_template():
    return jsonify({'template_id': 1})
