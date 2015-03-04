"""empty message

Revision ID: 4d97a5fdba44
Revises: 4d8d36f3d608
Create Date: 2015-03-03 23:47:57.315967

"""

# revision identifiers, used by Alembic.
revision = '4d97a5fdba44'
down_revision = '4d8d36f3d608'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('template_base', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('template_base', sa.Column('title', sa.String(length=255), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('template_base', 'title')
    op.drop_column('template_base', 'description')
    ### end Alembic commands ###
