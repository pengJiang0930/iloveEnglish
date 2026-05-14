from sqlalchemy import Integer, SmallInteger, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.models.base import Base, TimestampMixin


class UserWordBook(Base, TimestampMixin):
    __tablename__ = "user_word_book"
    __table_args__ = (
        UniqueConstraint("user_id", "book_id", name="uk_user_book"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), index=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("word_book.id"), index=True)
    current_index: Mapped[int] = mapped_column(Integer, default=0)
    learned_count: Mapped[int] = mapped_column(Integer, default=0)
    mastered_count: Mapped[int] = mapped_column(Integer, default=0)
    is_current: Mapped[int] = mapped_column(SmallInteger, default=0)
    status: Mapped[int] = mapped_column(SmallInteger, default=0)
    started_at: Mapped[datetime | None] = mapped_column(DateTime)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime)
