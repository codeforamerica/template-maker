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
                'variables': [],
                'type': 'title',
                'template_id': 1
            },
            {
                'content': '''The quick brown {{ animal }} and gray {{ animal }} jump over the lazy {{ animal2 }} on {{ date }}.

                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque accumsan eros nibh, vitae vulputate sem vehicula eu. Etiam eleifend sagittis tempus. Praesent vel mi orci. Vestibulum gravida fringilla sem, vel rutrum neque porttitor a. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum eu arcu congue libero blandit consequat vitae id nibh. Ut faucibus hendrerit risus, quis mattis neque ultricies at. Sed euismod urna vitae odio vulputate, a fermentum ex posuere.

                Aliquam ultrices tincidunt lobortis. Suspendisse potenti. Nullam faucibus, libero quis sodales auctor, orci lectus fringilla purus, et maximus nunc justo in diam. Phasellus luctus nisl id volutpat mattis. Nullam dolor mi, malesuada semper tortor at, cursus molestie lacus. Mauris eleifend quis urna at eleifend. Aenean ultricies sapien et rhoncus egestas. Etiam tempus lectus vel purus sagittis, sit amet iaculis purus consectetur. Donec euismod et massa ut dapibus. Maecenas porttitor suscipit erat. Quisque in dapibus ante, nec tristique metus. Sed ut felis lorem. In hac habitasse platea dictumst.''',
                'variables': ['animal', 'animal2', 'date'],
                'type': 'section',
                'template_id': 1
            },
            {
                'content': 'Mommy made me munch my {{ candy }}. It was {{ taste }} and had lots of {{ ingrediant }}.',
                'variables': ['candy', 'taste', 'ingrediant'],
                'type': 'section',
                'template_id': 1
            },
            {
                'content': '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque accumsan eros nibh, vitae vulputate sem vehicula eu. Etiam eleifend sagittis tempus. Praesent vel mi orci. Vestibulum gravida fringilla sem, vel rutrum neque porttitor a. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum eu arcu congue libero blandit consequat vitae id nibh. Ut faucibus hendrerit risus, quis mattis neque ultricies at. Sed euismod urna vitae odio vulputate, a fermentum ex posuere.

                Aliquam ultrices tincidunt lobortis. Suspendisse potenti. Nullam faucibus, libero quis sodales auctor, orci lectus fringilla purus, et maximus nunc justo in diam. Phasellus luctus nisl id volutpat mattis. Nullam dolor mi, malesuada semper tortor at, cursus molestie lacus. Mauris eleifend quis urna at eleifend. Aenean ultricies sapien et rhoncus egestas. Etiam tempus lectus vel purus sagittis, sit amet iaculis purus consectetur. Donec euismod et massa ut dapibus. Maecenas porttitor suscipit erat. Quisque in dapibus ante, nec tristique metus. Sed ut felis lorem. In hac habitasse platea dictumst.''',
                'variables': [],
                'type': 'section',
                'template_id': 1            
            }
        ]})

    # if not, render the template
    return render_template('builder/process.html')

@blueprint.route('/new/save', methods=['POST'])
def save_new_template():
    return jsonify({'template_id': 1})
