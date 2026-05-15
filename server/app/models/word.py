from sqlalchemy import String, Integer, SmallInteger, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin


class Word(Base, TimestampMixin):
    __tablename__ = "word"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    word: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    phonetic: Mapped[str | None] = mapped_column(String(100))
    meaning_cn: Mapped[str] = mapped_column(String(500))
    meaning_en: Mapped[str | None] = mapped_column(String(500))
    part_of_speech: Mapped[str | None] = mapped_column(String(50))
    frequency: Mapped[int] = mapped_column(Integer, default=0, index=True)
    level: Mapped[int] = mapped_column(SmallInteger, default=1, index=True)
    example_sentence: Mapped[str | None] = mapped_column(Text)
    example_translation: Mapped[str | None] = mapped_column(String(500))
    audio_url: Mapped[str | None] = mapped_column(String(255))
