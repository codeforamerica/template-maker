import re
from sqlalchemy.dialects.postgresql import array

from template_maker.database import db
from template_maker.builder.models import TemplateSection, TextSection, FixedTextSection
from template_maker.data.placeholders import (
    delete_excess_placeholders, create_or_update_placeholder, get_section_placeholders,
    get_all_placeholders
)

SECTION_TYPE_MAPS = {
    'text': TextSection, 'fixed_text': FixedTextSection,
}

def get_template_sections(template):
    '''
    Gets the text of the sections for the template

    Returns a list of sections with their metadata,
    in the proper order that they should be
    arranged on the page
    '''
    sections = TemplateSection.query.filter(TemplateSection.template_id==template.id).all()
    if template.section_order and len(template.section_order) == len(sections):
        order = []
        try:
            for ix, i in enumerate(template.section_order):
                order.append([section.id for section in sections].index(i))
            sections = [ sections[i] for i in order ]
        except ValueError:
            pass
    return sections

def get_single_section(section_id, template_id):
    if section_id:
        return TemplateSection.query.get(section_id)
    else:
        dummy_section = TemplateSection(template_id=template_id)
        dummy_section.section_type = 'dummy'
        dummy_section.id = 0
        return dummy_section

def create_new_section(section, template_id):
    '''
    Creates a new section based on the section_type sent by the request
    '''
    new_section = SECTION_TYPE_MAPS.get(section.get('type'))(
        section.get('title', ''),
        '',
        template_id
    ) if section.get('type') in SECTION_TYPE_MAPS.keys() else None
    if new_section:
        if section.get('type') in ('text', 'fixed_text'):
            new_section.text = section.get('html', '')
        db.session.add(new_section)
        db.session.commit()
        return new_section.id
    return False

def reorder_sections(template, section_order, to_delete=None):
    '''
    Takes a template, a list of ids, and sets the order
    on the template base model
    '''
    if to_delete:
        if to_delete in template.section_order:
            template.section_order.remove(to_delete)

            # cast it to a sqlalchemy array type to ensure
            # the commit works properly
            new_order = array(template.section_order)
            template.section_order = new_order if len(new_order) > 0 else None
            db.session.commit()
            
    else:
        template.section_order = [int(i) for i in section_order]
        db.session.commit()

    return template.section_order

def update_section(section, template_id, form_input):
    '''
    Updates TemplateSection and TemplatePlaceholders models associated with
    a particular template_id
    '''
    section.title = form_input.get('title')

    if section.section_type == 'text':
        html = form_input.get('widget')
        section.text = html
        # save the text
        db.session.commit()
        # find all placeholders, using beautiful soup
        input_placeholders = get_all_placeholders(html)
        # get any existing placeholders
        current_placeholders = get_section_placeholders(section.id)

        # if there are more old placeholders than new ones, delete the excess
        delete_excess_placeholders(current_placeholders, input_placeholders)

        # overwrite the old placeholders with the new ones
        for var_idx, placeholder in enumerate(input_placeholders):
            create_or_update_placeholder(var_idx, placeholder, input_placeholders, current_placeholders, template_id, section.id)

    return section.id

def delete_section(section_id, template_id):
    section = get_single_section(section_id, template_id)
    db.session.delete(section)
    db.session.commit()
    return True
