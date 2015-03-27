from template_maker.database import db
from template_maker.builder.models import TemplateVariables

VARIABLE_TYPE_MAPS = {
    'text': 1, 'date': 2,'number': 3, 'float': 4
}

def get_template_variables(template_id):
    '''
    Gets the variables associated with each template

    Returns a list of variables associated with the template
    along with the sections that they are tied to
    '''
    return TemplateVariables.query.filter(
        TemplateVariables.template_id==template_id
    ).order_by(TemplateVariables.id).all()

def get_section_variables(section_id):
    '''
    Gets the variables associated with each section

    Returns a list of TemplateVariables associated
    with the input section_id
    '''
    return TemplateVariables.query.filter(
        TemplateVariables.section_id==section_id
    ).order_by(TemplateVariables.id).all()

def parse_variable_text(variable):
    '''
    Takes a variable of the form [[TYPE:NAME]] and
    returns the type and the name
    '''
    no_tags = variable.lstrip('[[').rstrip(']]')
    var_type = no_tags.split('||')[0].lower()
    var_name = '[[' + no_tags.split('||')[1] + ']]'
    return var_type, var_name

def delete_excess_variables(current_variables, input_variables):
    if len(current_variables) > len(input_variables):
        TemplateVariables.query.filter(
            TemplateVariables.id.in_(
                [i.id for i in current_variables[len(input_variables):]]
            )
        ).delete(synchronize_session=False)
    return True

def create_or_update_variable(var_idx, variable, input_variables, current_variables, template_id, section_id):
    _variable = current_variables[var_idx] if len(current_variables) > 0 and var_idx < len(current_variables) else TemplateVariables()
    var_type, var_name = parse_variable_text(variable)
    _variable.full_name = variable
    _variable.display_name = var_name
    _variable.template_id = template_id
    _variable.section_id = section_id
    _variable.type = VARIABLE_TYPE_MAPS[var_type]
    if not _variable.id:
        db.session.add(_variable)
    db.session.commit()
