from flask import (
    Blueprint, render_template, redirect, url_for
)

blueprint = Blueprint(
    'frontmatter', __name__,
    template_folder='../templates'
)

@blueprint.route('/')
def index():
    # return render_template('frontmatter/index.html')
    return redirect(url_for('builder.list_templates'))
