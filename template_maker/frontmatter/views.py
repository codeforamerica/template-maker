from flask import (
    Blueprint,
    render_template,
)

blueprint = Blueprint(
    'frontmatter', __name__,
    template_folder='../templates'
)

@blueprint.route('/')
def index():
    return render_template('frontmatter/index.html')
