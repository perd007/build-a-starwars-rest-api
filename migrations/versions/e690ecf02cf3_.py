"""empty message

Revision ID: e690ecf02cf3
Revises: d98cb82c87dc
Create Date: 2023-08-28 21:25:02.343528

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e690ecf02cf3'
down_revision = 'd98cb82c87dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorities', schema=None) as batch_op:
        batch_op.drop_constraint('favorities_people_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('favorities_planet_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('favorities_user_id_fkey', type_='foreignkey')
        batch_op.drop_column('planet_id')
        batch_op.drop_column('people_id')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.drop_constraint('people_planet_id_fkey', type_='foreignkey')
        batch_op.drop_column('planet_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.add_column(sa.Column('planet_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('people_planet_id_fkey', 'planet', ['planet_id'], ['id'])

    with op.batch_alter_table('favorities', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('people_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('planet_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('favorities_user_id_fkey', 'user', ['user_id'], ['id'])
        batch_op.create_foreign_key('favorities_planet_id_fkey', 'planet', ['planet_id'], ['id'])
        batch_op.create_foreign_key('favorities_people_id_fkey', 'people', ['people_id'], ['id'])

    # ### end Alembic commands ###
