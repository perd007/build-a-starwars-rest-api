"""empty message

Revision ID: 7fa2b37454d9
Revises: 704d1d4d6abc
Create Date: 2023-08-28 22:10:52.013854

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fa2b37454d9'
down_revision = '704d1d4d6abc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.Column('people_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['people_id'], ['people.id'], ),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('favorities')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorities',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('people_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('planet_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['people_id'], ['people.id'], name='favorities_people_id_fkey'),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], name='favorities_planet_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='favorities_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='favorities_pkey')
    )
    op.drop_table('favorites')
    # ### end Alembic commands ###
