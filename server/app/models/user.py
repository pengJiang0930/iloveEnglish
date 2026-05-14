from sqlalchemy import String, Integer, SmallInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.models.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uid: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(20), index=True)
    password_hash: Mapped[str] = mapped_column(String(128))
    nickname: Mapped[str] = mapped_column(String(50), default="")
    avatar: Mapped[str | None] = mapped_column(String(255))
    level: Mapped[int] = mapped_column(SmallInteger, default=1)
    daily_goal: Mapped[int] = mapped_column(Integer, default=20)
    vip_level: Mapped[int] = mapped_column(SmallInteger, default=0)
    vip_expire_at: Mapped[datetime | None] = mapped_column(DateTime)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime)

    setting: Mapped["UserSetting"] = relationship(back_populates="user", uselist=False)
