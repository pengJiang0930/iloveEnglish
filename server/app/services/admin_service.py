from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.user import User
from app.models.word_book import WordBook
from app.models.word import Word


async def get_dashboard_stats(db: AsyncSession) -> dict:
    book_count = (await db.execute(select(func.count()).select_from(WordBook))).scalar()
    word_count = (await db.execute(select(func.count()).select_from(Word))).scalar()
    user_count = (await db.execute(
        select(func.count()).select_from(User).where(User.deleted_at.is_(None))
    )).scalar()
    return {"book_count": book_count, "word_count": word_count, "user_count": user_count}


async def get_user_list(
    db: AsyncSession,
    phone: str | None = None,
    nickname: str | None = None,
    status: int | None = None,
    page: int = 1,
    page_size: int = 20,
) -> dict:
    # Admin sees all users, including disabled (deleted_at is not null)
    base = select(User)
    count_base = select(func.count()).select_from(User)

    if status is not None:
        if status == 1:
            base = base.where(User.deleted_at.is_(None))
            count_base = count_base.where(User.deleted_at.is_(None))
        else:
            base = base.where(User.deleted_at.isnot(None))
            count_base = count_base.where(User.deleted_at.isnot(None))

    if phone:
        base = base.where(User.phone.like(f"%{phone}%"))
        count_base = count_base.where(User.phone.like(f"%{phone}%"))
    if nickname:
        base = base.where(User.nickname.like(f"%{nickname}%"))
        count_base = count_base.where(User.nickname.like(f"%{nickname}%"))

    total = (await db.execute(count_base)).scalar()

    offset = (page - 1) * page_size
    query = base.order_by(User.created_at.desc()).offset(offset).limit(page_size)
    result = await db.execute(query)
    users = result.scalars().all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "list": [
            {
                "id": u.id,
                "uid": u.uid,
                "phone": u.phone,
                "nickname": u.nickname,
                "avatar": u.avatar,
                "level": u.level,
                "vip_level": u.vip_level,
                "daily_goal": u.daily_goal,
                "status": 1 if u.deleted_at is None else 0,
                "last_login_at": u.last_login_at.isoformat() if u.last_login_at else None,
                "created_at": u.created_at.isoformat() if u.created_at else None,
            }
            for u in users
        ],
    }


async def toggle_user_status(db: AsyncSession, user_id: int, action: str) -> None:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise ValueError("用户不存在")

    if action == "disable":
        user.deleted_at = datetime.now(timezone.utc)
    elif action == "enable":
        user.deleted_at = None
    else:
        raise ValueError("无效操作，只支持 enable / disable")
    await db.commit()
