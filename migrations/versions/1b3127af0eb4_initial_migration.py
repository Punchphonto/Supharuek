"""Initial migration.

Revision ID: 1b3127af0eb4
Revises: 
Create Date: 2022-01-11 15:47:06.090974

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b3127af0eb4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('woringlist', sa.Column('workplace', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('woringlist', 'workplace')
    # ### end Alembic commands ###
