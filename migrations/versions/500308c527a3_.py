"""empty message

Revision ID: 500308c527a3
Revises: 7fa2b37454d9
Create Date: 2023-08-29 23:12:34.232118

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '500308c527a3'
down_revision = '7fa2b37454d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.alter_column('planet_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.alter_column('planet_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
