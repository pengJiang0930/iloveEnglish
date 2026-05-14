"""seed word_book data

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-05-14 22:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### 插入预置词书数据 ###
    word_book_table = sa.table('word_book',
        sa.column('name', sa.String),
        sa.column('description', sa.String),
        sa.column('category', sa.String),
        sa.column('word_count', sa.Integer),
        sa.column('sort_order', sa.Integer),
        sa.column('is_free', sa.SmallInteger),
        sa.column('status', sa.SmallInteger),
    )

    op.bulk_insert(word_book_table, [
        {
            'name': '高频核心1000词',
            'description': '最常用的1000个英语单词',
            'category': 'core',
            'word_count': 1000,
            'sort_order': 1,
            'is_free': 1,
            'status': 1,
        },
        {
            'name': '高频核心2000词',
            'description': '最常用的2000个英语单词',
            'category': 'core',
            'word_count': 2000,
            'sort_order': 2,
            'is_free': 1,
            'status': 1,
        },
        {
            'name': '高频核心3000词',
            'description': '最常用的3000个英语单词',
            'category': 'core',
            'word_count': 3000,
            'sort_order': 3,
            'is_free': 1,
            'status': 1,
        },
        {
            'name': '四级核心词汇',
            'description': '大学英语四级高频词汇',
            'category': 'exam',
            'word_count': 2000,
            'sort_order': 4,
            'is_free': 1,
            'status': 1,
        },
        {
            'name': '六级核心词汇',
            'description': '大学英语六级高频词汇',
            'category': 'exam',
            'word_count': 2500,
            'sort_order': 5,
            'is_free': 1,
            'status': 1,
        },
        {
            'name': '考研核心词汇',
            'description': '考研英语高频词汇',
            'category': 'exam',
            'word_count': 3000,
            'sort_order': 6,
            'is_free': 1,
            'status': 1,
        },
        {
            'name': '雅思核心词汇',
            'description': '雅思考试高频词汇',
            'category': 'exam',
            'word_count': 3500,
            'sort_order': 7,
            'is_free': 0,
            'status': 1,
        },
        {
            'name': '托福核心词汇',
            'description': '托福考试高频词汇',
            'category': 'exam',
            'word_count': 4000,
            'sort_order': 8,
            'is_free': 0,
            'status': 1,
        },
        {
            'name': '日常口语高频词',
            'description': '日常对话中最常用的单词',
            'category': 'daily',
            'word_count': 500,
            'sort_order': 9,
            'is_free': 1,
            'status': 1,
        },
        {
            'name': '生活场景词汇',
            'description': '购物、餐饮、交通等场景词汇',
            'category': 'daily',
            'word_count': 800,
            'sort_order': 10,
            'is_free': 1,
            'status': 1,
        },
    ])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### 删除预置词书数据 ###
    op.execute("DELETE FROM word_book WHERE category IN ('core', 'exam', 'daily')")
    # ### end Alembic commands ###
