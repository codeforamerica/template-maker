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

blueprint = Blueprint(
    'generator', __name__, url_prefix='/generate',
    template_folder='../templates'
)

@blueprint.route('/')
def list_templates():
    '''
    Returns a list of all the templates.

    Because there is no interacton on this page, it uses
    Flask entirely
    '''
    templates = TemplateBase.query.filter(TemplateBase.published==True).all()
    return render_template('generator/list.html', templates=templates)