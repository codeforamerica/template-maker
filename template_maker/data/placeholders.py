from template_maker.database import db
from template_maker.builder.models import TemplatePlaceholders
from bs4 import BeautifulSoup

VARIABLE_TYPE_MAPS = {
    'text': 1, 'date': 2,'number': 3, 'float': 4
}

def get_all_placeholders(html):
    '''
    Uses BeautifulSoup to parse through an HTML block and
    return all .fr-placeholder span tags
    '''
    soup = BeautifulSoup(html)
    return soup.find_all('span', {'class': 'js-fr-placeholder'})

def get_template_placeholders(template_id):
    '''
    Gets the placeholders associated with each template

    Returns a list of placeholders associated with the template
    along with the sections that they are tied to
    '''
    return TemplatePlaceholders.query.filter(
        TemplatePlaceholders.template_id==template_id
    ).order_by(TemplatePlaceholders.id).all()

def get_section_placeholders(section_id):
    '''
    Gets the placeholders associated with each section

    Returns a list of TemplatePlaceholders associated
    with the input section_id
    '''
    return TemplatePlaceholders.query.filter(
        TemplatePlaceholders.section_id==section_id
    ).order_by(TemplatePlaceholders.id).all()

def parse_placeholder_text(placeholder):
    '''
    Takes a placeholder of the form [[TYPE:NAME]] and
    returns the type and the name
    '''
    no_tags = placeholder.lstrip('[[').rstrip(']]')
    var_type = no_tags.split('||')[0].lower()
    var_name = '[[' + no_tags.split('||')[1] + ']]'
    return var_type, var_name

def dedupe_placeholders(input_placeholders):
    return list(set([i.text for i in input_placeholders]))

def update_placeholders(input_placeholders, current_placeholders, template_id, section_id):

    current_placeholder_full_names = set([i.full_name for i in current_placeholders])
    new_placeholders = list(set(input_placeholders).difference(current_placeholder_full_names))
    to_delete_placeholders = list(set(current_placeholder_full_names).difference(input_placeholders))

    if len(to_delete_placeholders) > 0:
        delete_placeholders(to_delete_placeholders, template_id, section_id)

    if len(new_placeholders) > 0:
        create_placeholders(new_placeholders, template_id, section_id)

    return True

def delete_placeholders(to_delete_placeholders, template_id, section_id):
    TemplatePlaceholders.query.filter(
        TemplatePlaceholders.full_name.in_(to_delete_placeholders),
        TemplatePlaceholders.template_id==template_id,
        TemplatePlaceholders.section_id==section_id
    ).delete(synchronize_session=False)
    return True

def create_placeholders(new_placeholders, template_id, section_id):
    for placeholder in new_placeholders:
        _placeholder = TemplatePlaceholders()
        var_type, var_name = parse_placeholder_text(placeholder)
        _placeholder.full_name = placeholder
        _placeholder.display_name = var_name
        _placeholder.template_id = template_id
        _placeholder.section_id = section_id
        _placeholder.type = VARIABLE_TYPE_MAPS[var_type]
        db.session.add(_placeholder)
    db.session.commit()
