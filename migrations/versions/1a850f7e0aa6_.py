"""empty message

Revision ID: 1a850f7e0aa6
Revises: 22e9ba47d864
Create Date: 2015-04-03 16:33:39.130824

"""

# revision identifiers, used by Alembic.
revision = '1a850f7e0aa6'
down_revision = '22e9ba47d864'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('document_base',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('template_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['template_id'], ['template_base.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('document_base')
    ### end Alembic commands ###
