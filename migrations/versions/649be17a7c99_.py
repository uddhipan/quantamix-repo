"""empty message

Revision ID: 649be17a7c99
Revises: 1099768dff5f
Create Date: 2018-11-30 16:46:04.821548

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '649be17a7c99'
down_revision = '1099768dff5f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('intrest',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('intrest_type', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('intrest')
    # ### end Alembic commands ###
