"""create word, word_book_item, user_word_list tables

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-05-15 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c3d4e5f6a7b8'
down_revision: Union[str, None] = 'b2c3d4e5f6a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('word',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('word', sa.String(length=100), nullable=False),
    sa.Column('phonetic', sa.String(length=100), nullable=True),
    sa.Column('meaning_cn', sa.String(length=500), nullable=False),
    sa.Column('meaning_en', sa.String(length=500), nullable=True),
    sa.Column('part_of_speech', sa.String(length=50), nullable=True),
    sa.Column('frequency', sa.Integer(), nullable=False),
    sa.Column('level', sa.SmallInteger(), nullable=False),
    sa.Column('example_sentence', sa.Text(), nullable=True),
    sa.Column('example_translation', sa.String(length=500), nullable=True),
    sa.Column('audio_url', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('word', name='idx_word')
    )
    with op.batch_alter_table('word', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_word_word'), ['word'], unique=True)
        batch_op.create_index(batch_op.f('ix_word_frequency'), ['frequency'], unique=False)
        batch_op.create_index(batch_op.f('ix_word_level'), ['level'], unique=False)

    op.create_table('word_book_item',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('word_id', sa.Integer(), nullable=False),
    sa.Column('sort_order', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['word_book.id'], ),
    sa.ForeignKeyConstraint(['word_id'], ['word.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('book_id', 'word_id', name='uk_book_word')
    )
    with op.batch_alter_table('word_book_item', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_word_book_item_book_id'), ['book_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_word_book_item_word_id'), ['word_id'], unique=False)

    op.create_table('user_word_list',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('word_id', sa.Integer(), nullable=False),
    sa.Column('source', sa.String(length=20), nullable=False),
    sa.Column('status', sa.SmallInteger(), nullable=False),
    sa.Column('review_count', sa.Integer(), nullable=False),
    sa.Column('last_review_at', sa.DateTime(), nullable=True),
    sa.Column('next_review_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['word_id'], ['word.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'word_id', name='uk_user_word')
    )
    with op.batch_alter_table('user_word_list', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_word_list_user_id'), ['user_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_word_list_word_id'), ['word_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_word_list_next_review_at'), ['next_review_at'], unique=False)


def downgrade() -> None:
    with op.batch_alter_table('user_word_list', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_word_list_next_review_at'))
        batch_op.drop_index(batch_op.f('ix_user_word_list_word_id'))
        batch_op.drop_index(batch_op.f('ix_user_word_list_user_id'))

    op.drop_table('user_word_list')

    with op.batch_alter_table('word_book_item', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_word_book_item_word_id'))
        batch_op.drop_index(batch_op.f('ix_word_book_item_book_id'))

    op.drop_table('word_book_item')

    with op.batch_alter_table('word', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_word_level'))
        batch_op.drop_index(batch_op.f('ix_word_frequency'))
        batch_op.drop_index(batch_op.f('ix_word_word'))

    op.drop_table('word')
