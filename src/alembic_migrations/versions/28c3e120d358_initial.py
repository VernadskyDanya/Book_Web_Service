"""initial

Revision ID: 28c3e120d358
Revises: 
Create Date: 2024-01-27 18:21:19.376032

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '28c3e120d358'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'book',
        sa.Column('book_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=30), nullable=False),
        sa.Column('author', sa.String(length=30), nullable=False),
        sa.Column('published_date', sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint('book_id')
    )
    op.create_table(
        'genre',
        sa.Column('genre_id', sa.Integer(), nullable=False),
        sa.Column('genre_name', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('genre_id')
    )
    op.create_table(
        'book_file',
        sa.Column('file_id', sa.Integer(), nullable=False),
        sa.Column('book_id', sa.Integer(), nullable=True),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('file_format', sa.String(length=20), nullable=True),
        sa.ForeignKeyConstraint(['book_id'], ['book.book_id'], ),
        sa.PrimaryKeyConstraint('file_id')
    )
    op.create_table(
        'book_genre',
        sa.Column('book_id', sa.Integer(), nullable=True),
        sa.Column('genre_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['book_id'], ['book.book_id'], ),
        sa.ForeignKeyConstraint(['genre_id'], ['genre.genre_id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('book_genre')
    op.drop_table('book_file')
    op.drop_table('genre')
    op.drop_table('book')
    # ### end Alembic commands ###
