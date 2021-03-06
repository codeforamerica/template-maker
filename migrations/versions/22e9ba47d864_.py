"""Mass rename variables to placeholders

Revision ID: 22e9ba47d864
Revises: 3fe7a442d4f1
Create Date: 2015-03-27 17:55:33.315929

"""

# revision identifiers, used by Alembic.
revision = '22e9ba47d864'
down_revision = '3fe7a442d4f1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    placeholder_types = op.create_table('placeholder_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.bulk_insert(placeholder_types, [
        { 'id': 1, 'type': 'unicode' },
        { 'id': 2, 'type': 'date' },
        { 'id': 3, 'type': 'int' },
        { 'id': 4, 'type': 'float' }
    ])
    op.create_table('template_placeholders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.Text(), nullable=True),
    sa.Column('display_name', sa.Text(), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('template_id', sa.Integer(), nullable=False),
    sa.Column('section_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['section_id'], ['template_section.id'], ),
    sa.ForeignKeyConstraint(['template_id'], ['template_base.id'], ),
    sa.ForeignKeyConstraint(['type'], ['placeholder_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('template_variables')
    op.drop_table('variable_types')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('template_variables',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('type', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('template_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('section_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('display_name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('full_name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['section_id'], [u'template_section.id'], name=u'template_variables_section_id_fkey'),
    sa.ForeignKeyConstraint(['template_id'], [u'template_base.id'], name=u'template_variables_template_id_fkey'),
    sa.ForeignKeyConstraint(['type'], [u'variable_types.id'], name=u'template_variables_type_fkey'),
    sa.PrimaryKeyConstraint('id', name=u'template_variables_pkey')
    )
    op.create_table('variable_types',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('type', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'variable_types_pkey')
    )
    op.drop_table('template_placeholders')
    op.drop_table('placeholder_types')
    ### end Alembic commands ###
