"""empty message

Revision ID: 925947b72b6e
Revises: 
Create Date: 2021-01-23 14:18:08.934071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '925947b72b6e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('movies', 'imdb_rating',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('movies', 'title',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('movies', 'title',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('movies', 'imdb_rating',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
