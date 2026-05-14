from sqlalchemy import String, Integer, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin


class WordBook(Base, TimestampMixin):
    __tablename__ = "word_book"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(500))
    category: Mapped[str] = mapped_column(String(50), index=True)
    word_count: Mapped[int] = mapped_column(Integer, default=0)
    cover_image: Mapped[str | None] = mapped_column(String(255))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_free: Mapped[int] = mapped_column(SmallInteger, default=1)
    status: Mapped[int] = mapped_column(SmallInteger, default=1, index=True)
