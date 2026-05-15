from sqlalchemy import String, Integer, SmallInteger, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.models.base import Base, TimestampMixin


class UserWordList(Base, TimestampMixin):
    __tablename__ = "user_word_list"
    __table_args__ = (
        UniqueConstraint("user_id", "word_id", name="uk_user_word"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), index=True)
    word_id: Mapped[int] = mapped_column(Integer, ForeignKey("word.id"), index=True)
    source: Mapped[str] = mapped_column(String(20), default="book")
    status: Mapped[int] = mapped_column(SmallInteger, default=0)
    review_count: Mapped[int] = mapped_column(Integer, default=0)
    last_review_at: Mapped[datetime | None] = mapped_column(DateTime)
    next_review_at: Mapped[datetime | None] = mapped_column(DateTime, index=True)
