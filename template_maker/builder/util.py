import re
from template_maker.database import db
from template_maker.builder.models import (
    TemplateBase, TemplateSection, TextSection,
    FixedTextSection, TemplateVariables
)

VARIABLE_TYPE_MAPS = {
    'text': 1, 'date': 2,'int': 3, 'float': 4
}

SECTION_TYPE_MAPS = {
    'text': TextSection, 'fixed_text': FixedTextSection,
}

VARIABLE_RE = re.compile('(\[\[ |\[\[).*?\|\|.*?(\]\]| \]\])')

def create_new_section(section, template_id):
    '''
    Creates a new section based on the section_type sent by the request
    '''
    new_section = SECTION_TYPE_MAPS.get(section.get('type'))(
        section.get('title', ''),
        '',
        template_id
    )
    db.session.add(new_section)
    db.session.commit()
    return new_section.id

def parse_variable_text(variable):
    '''
    Takes a variable of the form [[TYPE:NAME]] and
    returns the type and the name
    '''
    no_tags = variable.lstrip('[[').rstrip(']]')
    var_type = no_tags.split('||')[0].lower()
    var_name = '[[' + no_tags.split('||')[1] + ']]'
    return var_type, var_name

def update_section(section, template_id, form_input):
    '''
    Updates TemplateSection and TemplateVariables models associated with
    a particular template_id
    '''
    section.title = form_input.get('title')
    if section.section_type == 'fixed_text':
        # TODO: Sanitize HTML input
        section.text = form_input.get('widget')
        db.session.commit()
    elif section.section_type == 'text':
        html = form_input.get('widget')
        section.text = html
        # save the text
        db.session.commit()
        # find all variables, using the regex set above
        input_variables = [i.group() for i in re.finditer(VARIABLE_RE, html)]
        # get any existing variables
        current_variables = get_section_variables(section.id)

        # if there are more old variables than new ones, delete the excess
        if len(current_variables) > len(input_variables):
            TemplateVariables.query.filter(
                TemplateVariables.id.in_(
                    [i.id for i in current_variables[len(input_variables):]]
                )
            ).delete(synchronize_session=False)

        # overwrite the old variables with the new ones
        for var_idx, variable in enumerate(input_variables):
            _variable = current_variables[var_idx] if len(current_variables) > 0 and var_idx < len(current_variables) else TemplateVariables()
            var_type, var_name = parse_variable_text(variable)
            _variable.full_name = variable
            _variable.display_name = var_name
            _variable.template_id = template_id
            _variable.section_id = section.id
            _variable.type = VARIABLE_TYPE_MAPS[var_type]
            if not _variable.id:
                db.session.add(_variable)
            db.session.commit()

    return section.id

def update_variables(template_variables, variables, template_id):
    variables_dict = variables.to_dict()
    for variable in template_variables:
        variable.type = VARIABLE_TYPE_MAPS[variables_dict[variable.name]]
        db.session.commit()
    return

def get_template_sections(template_id):
    '''
    Gets the text of the sections for the template

    Returns a list of sections with their metadata,
    in the proper order that they should be
    arranged on the page
    '''
    if TemplateBase.query.get(template_id):
        return TemplateSection.query.filter(TemplateSection.template_id==template_id).all()
    else:
        return None

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
