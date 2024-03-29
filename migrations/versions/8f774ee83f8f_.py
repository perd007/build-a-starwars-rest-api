"""empty message

Revision ID: 8f774ee83f8f
Revises: 98181bd1dd86
Create Date: 2023-08-28 22:06:22.543664

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f774ee83f8f'
down_revision = '98181bd1dd86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorities', schema=None) as batch_op:
        batch_op.add_column(sa.Column('people_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'people', ['people_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorities', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('people_id')

    # ### end Alembic commands ###
