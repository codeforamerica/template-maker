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
    placeholder_text = placeholder.text
    no_tags = placeholder_text.lstrip('[[').rstrip(']]')
    var_type = no_tags.split('||')[0].lower()
    var_name = '[[' + no_tags.split('||')[1] + ']]'
    return var_type, var_name

def delete_excess_placeholders(current_placeholders, input_placeholders):
    if len(current_placeholders) > len(input_placeholders):
        TemplatePlaceholders.query.filter(
            TemplatePlaceholders.id.in_(
                [i.id for i in current_placeholders[len(input_placeholders):]]
            )
        ).delete(synchronize_session=False)
    return True

def create_or_update_placeholder(var_idx, placeholder, input_placeholders, current_placeholders, template_id, section_id):
    _placeholder = current_placeholders[var_idx] if len(current_placeholders) > 0 and var_idx < len(current_placeholders) else TemplatePlaceholders()
    var_type, var_name = parse_placeholder_text(placeholder)
    _placeholder.full_name = placeholder.text
    _placeholder.display_name = var_name
    _placeholder.template_id = template_id
    _placeholder.section_id = section_id
    _placeholder.type = VARIABLE_TYPE_MAPS[var_type]
    if not _placeholder.id:
        db.session.add(_placeholder)
    db.session.commit()
