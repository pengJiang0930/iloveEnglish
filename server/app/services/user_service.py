import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.models.user_setting import UserSetting
from app.utils.auth import hash_password, verify_password, create_access_token


async def register(db: AsyncSession, phone: str, password: str, nickname: str) -> dict:
    existing = await db.execute(select(User).where(User.phone == phone, User.deleted_at.is_(None)))
    if existing.scalar_one_or_none():
        raise ValueError("该手机号已注册")

    user = User(
        uid=uuid.uuid4().hex,
        phone=phone,
        password_hash=hash_password(password),
        nickname=nickname or f"用户{phone[-4:]}",
    )
    db.add(user)
    await db.flush()

    setting = UserSetting(user_id=user.id)
    db.add(setting)
    await db.commit()
    await db.refresh(user)

    token = create_access_token(user.uid)
    return {"token": token, "user": user}


async def login(db: AsyncSession, phone: str, password: str) -> dict:
    result = await db.execute(select(User).where(User.phone == phone, User.deleted_at.is_(None)))
    user = result.scalar_one_or_none()
    if not user:
        raise ValueError("用户不存在")

    if not verify_password(password, user.password_hash):
        raise ValueError("密码错误")

    from datetime import datetime, timezone
    user.last_login_at = datetime.now(timezone.utc)
    await db.commit()

    token = create_access_token(user.uid)
    return {"token": token, "user": user}
