from template_maker.database import db
from template_maker.builder.models import TemplateBase, TemplateText, TemplateVariables

def set_template_content(sections, template_id):
    '''
    Updates TemplateText and TemplateVariables models associated with
    a particular template_id
    '''
    # first, get all sections associated with the template
    template_sections = TemplateText.query.\
        filter(TemplateText.template_id==template_id).\
        order_by(TemplateText.id).all()

    # if we have more old sections than new sections, delete the excess
    # old sections
    if len(template_sections) > len(sections):
        TemplateText.query.filter(
            TemplateText.id.in_(
                [i.id for i in template_sections[len(sections):]]
            )
        ).delete(synchronize_session=False)
        db.session.commit()

    for idx, section in enumerate(sections):
        # get the template's text section
        template_section = template_sections[idx] \
            if len(template_sections) > 0 and idx < len(template_sections) \
            else TemplateText()

        # update the section's text fields
        template_section.text = section.get('content', '')
        template_section.text_position = idx
        template_section.text_type = section.get('type')
        template_section.template_id = template_id
        # if it is a new section add it, otherwise update it
        if template_section.id is None:
            db.session.add(template_section)
        db.session.commit()
        
        template_text_id = template_section.id

        # repeat the same process for variables
        template_variables = TemplateVariables.query.\
            filter(TemplateVariables.template_text_id==template_text_id).\
            order_by(TemplateVariables.id).all()

        if len(template_variables) > len(section.get('variables', [])):
            TemplateVariables.query.filter(
                TemplateVariables.id.in_(
                    [i.id for i in template_variables[len(section.get('variables')):]]
                )
            ).delete(synchronize_session=False)
            db.session.commit()

        for var_idx, template_variable in enumerate(section.get('variables', [])):
            variable = template_variables[var_idx] if len(template_variables) > 0 and var_idx < len(template_variables) else TemplateVariables()
            variable.name = template_variable
            variable.template_id = template_id,
            variable.template_text_id = template_text_id
            if variable.id is None:
                db.session.add(variable)
            db.session.commit()
