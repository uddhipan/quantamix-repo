"""empty message

Revision ID: 422559659aba
Revises: 6a626f9c0277
Create Date: 2018-11-30 16:58:40.201793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '422559659aba'
down_revision = '6a626f9c0277'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('achievements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('medal_count', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_achievements_timestamp'), 'achievements', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_achievements_timestamp'), table_name='achievements')
    op.drop_table('achievements')
    # ### end Alembic commands ###
