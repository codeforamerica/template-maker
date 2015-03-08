from template_maker.database import db
from template_maker.builder.models import (
    TemplateBase, TemplateSection, TextSection,
    FixedTextSection, TemplateVariables
)

VARIABLE_TYPE_MAPS = {
    'unicode': 1, 'date': 2,'int': 3, 'float': 4
}

SECTION_TYPE_MAPS = {
    'text': TextSection, 'fixed_text': FixedTextSection,
}

def create_new_section(section, template_id):
    '''
    Creates a new section based on the section_type sent by the request
    '''
    new_section = SECTION_TYPE_MAPS.get(section.get('type'))(
        section.get('title'),
        section.get('description'),
        template_id
    )
    db.session.add(new_section)
    db.session.commit()
    return new_section.id


def update_section(section, template_id, form_input):
    '''
    Updates TemplateSection and TemplateVariables models associated with
    a particular template_id
    '''
    if section.section_type in ['text', 'fixed_text']:
        # TODO: Sanitize HTML input
        section.text = form_input.get('widget')
        db.session.commit()
    return section.id

def set_variable_types(sections, template_id):
    '''
    If our forms are all valid set the template types and then
    finally trigger the publication event
    '''
    template_sections = TemplateSection.query.\
        filter(TemplateSection.template_id==template_id).\
        order_by(TemplateSection.id).all()

    for idx, section in enumerate(sections):
        template_section = template_sections[idx]

        template_variables = TemplateVariables.query.\
            filter(TemplateVariables.template_section_id==template_section.id).\
            order_by(TemplateVariables.id).all()

        for var_idx, template_variable in enumerate(section):
            variable = template_variables[var_idx]
            variable.type = TYPE_MAPS[template_variable.get('type')]
            db.session.commit()


def get_template_sections(template_id):
    '''
    Gets the text of the sections for the template

    Returns a list of sections with their text,
    in the proper order that they should be
    arranged on the page
    }
    '''
    if TemplateBase.query.get(template_id):
        template = db.session.execute(
            '''
            SELECT
                a.id as template_id, b.id as template_section_id, b.title,
                b.section_type, b.position
            FROM template_base a
            INNER JOIN template_section b
            on a.id = b.template_id
            WHERE a.id = :template_id
            ORDER BY b.position ASC
            ''',
            { 'template_id': template_id }
        ).fetchall()

        output = []

        for section in template:
            output.append({
                'id': section[1],
                'title': section[2],
                'type': section[3],
            })

        return output
    else:
        return None
