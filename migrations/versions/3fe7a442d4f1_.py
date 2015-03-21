"""empty message

Revision ID: 3fe7a442d4f1
Revises: 44b77ae3ee69
Create Date: 2015-03-21 17:51:53.883838

"""

# revision identifiers, used by Alembic.
revision = '3fe7a442d4f1'
down_revision = '44b77ae3ee69'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'users_username_key', 'users', type_='unique')
    op.drop_column('users', 'username')
    op.drop_column('users', 'password')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('username', sa.VARCHAR(length=80), autoincrement=False, nullable=False))
    op.create_unique_constraint(u'users_username_key', 'users', ['username'])
    ### end Alembic commands ###
