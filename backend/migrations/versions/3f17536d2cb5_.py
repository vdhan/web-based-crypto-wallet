"""empty message

Revision ID: 3f17536d2cb5
Revises: 1dea9da9b9cc
Create Date: 2024-12-18 22:50:47.385135

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f17536d2cb5'
down_revision = '1dea9da9b9cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('revoke',
    sa.Column('jti', sa.String(length=26), nullable=False),
    sa.Column('expire', sa.DateTime(), nullable=False),
    sa.Column('id', sa.String(length=26), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('revoke')
    # ### end Alembic commands ###
