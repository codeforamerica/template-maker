"""empty message

Revision ID: 4aa97067cd17
Revises: 4d97a5fdba44
Create Date: 2015-03-05 15:25:11.092726

"""

# revision identifiers, used by Alembic.
revision = '4aa97067cd17'
down_revision = '4d97a5fdba44'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    variable_types_table = op.create_table('variable_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('types', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.bulk_insert(variable_types_table, [
        { 'id': 1, 'type': 'unicode' },
        { 'id': 2, 'type': 'date' },
        { 'id': 3, 'type': 'int' },
        { 'id': 4, 'type': 'float' }
    ])
    op.add_column(u'template_base', sa.Column('published', sa.Boolean(), nullable=True))
    op.add_column(u'template_variables', sa.Column('type', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'template_variables', 'variable_types', ['type'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'template_variables', type_='foreignkey')
    op.drop_column(u'template_variables', 'type')
    op.drop_column(u'template_base', 'published')
    op.drop_table('variable_types')
    ### end Alembic commands ###
