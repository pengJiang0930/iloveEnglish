from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class WordBookItem(Base):
    __tablename__ = "word_book_item"
    __table_args__ = (
        UniqueConstraint("book_id", "word_id", name="uk_book_word"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("word_book.id"), index=True)
    word_id: Mapped[int] = mapped_column(Integer, ForeignKey("word.id"), index=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
