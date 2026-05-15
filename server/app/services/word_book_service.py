from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from app.models.word_book import WordBook
from app.models.user_word_book import UserWordBook


async def get_book_list(
    db: AsyncSession, category: str | None = None, include_inactive: bool = False
) -> list[WordBook]:
    query = select(WordBook)
    if not include_inactive:
        query = query.where(WordBook.status == 1)
    if category:
        query = query.where(WordBook.category == category)
    query = query.order_by(WordBook.sort_order, WordBook.id)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_book_detail(db: AsyncSession, book_id: int, user_id: int | None = None) -> dict | None:
    result = await db.execute(select(WordBook).where(WordBook.id == book_id, WordBook.status == 1))
    book = result.scalar_one_or_none()
    if not book:
        return None

    book_data = {
        "id": book.id,
        "name": book.name,
        "description": book.description,
        "category": book.category,
        "word_count": book.word_count,
        "cover_image": book.cover_image,
        "sort_order": book.sort_order,
        "is_free": book.is_free,
        "status": book.status,
        "user_progress": None,
    }

    if user_id:
        progress_result = await db.execute(
            select(UserWordBook).where(
                UserWordBook.user_id == user_id,
                UserWordBook.book_id == book_id,
            )
        )
        progress = progress_result.scalar_one_or_none()
        if progress:
            book_data["user_progress"] = {
                "current_index": progress.current_index,
                "learned_count": progress.learned_count,
                "mastered_count": progress.mastered_count,
                "status": progress.status,
            }

    return book_data


async def select_book(db: AsyncSession, user_id: int, book_id: int) -> None:
    result = await db.execute(select(WordBook).where(WordBook.id == book_id, WordBook.status == 1))
    if not result.scalar_one_or_none():
        raise ValueError("词书不存在")

    existing_result = await db.execute(
        select(UserWordBook).where(
            UserWordBook.user_id == user_id,
            UserWordBook.book_id == book_id,
        )
    )
    if existing_result.scalar_one_or_none():
        raise ValueError("已选择该词书")

    await db.execute(
        update(UserWordBook)
        .where(UserWordBook.user_id == user_id, UserWordBook.is_current == 1)
        .values(is_current=0)
    )

    user_book = UserWordBook(
        user_id=user_id,
        book_id=book_id,
        is_current=1,
        status=1,
        started_at=datetime.now(timezone.utc),
    )
    db.add(user_book)
    await db.commit()


async def get_current_book(db: AsyncSession, user_id: int) -> dict | None:
    result = await db.execute(
        select(UserWordBook).where(UserWordBook.user_id == user_id, UserWordBook.is_current == 1)
    )
    user_book = result.scalar_one_or_none()
    if not user_book:
        return None

    book_result = await db.execute(select(WordBook).where(WordBook.id == user_book.book_id))
    book = book_result.scalar_one_or_none()
    if not book:
        return None

    return {
        "book": {
            "id": book.id,
            "name": book.name,
            "category": book.category,
            "word_count": book.word_count,
        },
        "progress": {
            "current_index": user_book.current_index,
            "learned_count": user_book.learned_count,
            "mastered_count": user_book.mastered_count,
            "status": user_book.status,
        },
    }


async def get_user_books(db: AsyncSession, user_id: int) -> list[dict]:
    result = await db.execute(
        select(UserWordBook)
        .where(UserWordBook.user_id == user_id)
        .order_by(UserWordBook.is_current.desc(), UserWordBook.updated_at.desc())
    )
    user_books = list(result.scalars().all())

    book_ids = [ub.book_id for ub in user_books]
    if not book_ids:
        return []

    books_result = await db.execute(select(WordBook).where(WordBook.id.in_(book_ids)))
    books_map = {b.id: b for b in books_result.scalars().all()}

    return [
        {
            "book": {
                "id": books_map[ub.book_id].id,
                "name": books_map[ub.book_id].name,
                "category": books_map[ub.book_id].category,
                "word_count": books_map[ub.book_id].word_count,
            },
            "progress": {
                "current_index": ub.current_index,
                "learned_count": ub.learned_count,
                "mastered_count": ub.mastered_count,
                "is_current": ub.is_current,
                "status": ub.status,
            },
        }
        for ub in user_books
        if ub.book_id in books_map
    ]


async def update_progress(db: AsyncSession, user_id: int, book_id: int, learned_count: int, mastered_count: int) -> None:
    result = await db.execute(
        select(UserWordBook).where(
            UserWordBook.user_id == user_id,
            UserWordBook.book_id == book_id,
        )
    )
    user_book = result.scalar_one_or_none()
    if not user_book:
        raise ValueError("未选择该词书")

    user_book.learned_count += learned_count
    user_book.mastered_count += mastered_count
    user_book.current_index += learned_count

    book_result = await db.execute(select(WordBook).where(WordBook.id == book_id))
    book = book_result.scalar_one_or_none()
    if book and user_book.current_index >= book.word_count:
        user_book.status = 2
        user_book.finished_at = datetime.now(timezone.utc)

    await db.commit()


async def create_book(db: AsyncSession, **kwargs) -> WordBook:
    book = WordBook(**kwargs)
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book


async def update_book(db: AsyncSession, book_id: int, **kwargs) -> WordBook:
    result = await db.execute(select(WordBook).where(WordBook.id == book_id))
    book = result.scalar_one_or_none()
    if not book:
        raise ValueError("词书不存在")
    for key, value in kwargs.items():
        if value is not None:
            setattr(book, key, value)
    await db.commit()
    await db.refresh(book)
    return book


async def delete_book(db: AsyncSession, book_id: int) -> None:
    result = await db.execute(select(WordBook).where(WordBook.id == book_id))
    book = result.scalar_one_or_none()
    if not book:
        raise ValueError("词书不存在")
    await db.delete(book)
    await db.commit()
