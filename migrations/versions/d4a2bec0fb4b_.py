"""empty message

Revision ID: d4a2bec0fb4b
Revises: 5901d21b9291
Create Date: 2018-11-30 16:33:26.270556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4a2bec0fb4b'
down_revision = '5901d21b9291'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('intrest')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('intrest',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('intrest_names', sa.TEXT(), nullable=True),
    sa.Column('intrest_type', sa.TEXT(), nullable=True),
    sa.Column('intrest_name', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
