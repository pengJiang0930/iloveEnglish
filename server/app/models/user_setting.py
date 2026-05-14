from sqlalchemy import String, Integer, SmallInteger, Time, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin


class UserSetting(Base, TimestampMixin):
    __tablename__ = "user_setting"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), unique=True)
    daily_reminder: Mapped[int] = mapped_column(SmallInteger, default=1)
    reminder_time: Mapped[str] = mapped_column(String(10), default="20:00")
    pronunciation: Mapped[str] = mapped_column(String(10), default="us")
    theme: Mapped[str] = mapped_column(String(20), default="light")
    font_size: Mapped[str] = mapped_column(String(10), default="medium")

    user: Mapped["User"] = relationship(back_populates="setting")
