"""Decorate variables

Revision ID: 228017954653
Revises: 5549c709cd56
Create Date: 2015-03-15 19:43:47.544488

"""

# revision identifiers, used by Alembic.
revision = '228017954653'
down_revision = '5549c709cd56'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('template_variables', sa.Column('display_name', sa.Text(), nullable=True))
    op.add_column('template_variables', sa.Column('full_name', sa.Text(), nullable=True))
    op.drop_column('template_variables', 'name')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('template_variables', sa.Column('name', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_column('template_variables', 'full_name')
    op.drop_column('template_variables', 'display_name')
    ### end Alembic commands ###
