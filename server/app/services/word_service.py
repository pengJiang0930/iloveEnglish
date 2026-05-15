from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.word import Word
from app.models.word_book import WordBook
from app.models.word_book_item import WordBookItem
from app.models.user_word_book import UserWordBook
from app.models.user_word_list import UserWordList

EBBINGHAUS_INTERVALS = [1, 2, 4, 7, 15, 30]


def _calc_next_review(review_count: int) -> datetime:
    days = EBBINGHAUS_INTERVALS[min(review_count, len(EBBINGHAUS_INTERVALS) - 1)]
    return datetime.now(timezone.utc) + timedelta(days=days)


async def get_words_by_book(
    db: AsyncSession, book_id: int, page: int = 1, page_size: int = 20, user_id: int | None = None
) -> dict:
    book_result = await db.execute(select(WordBook).where(WordBook.id == book_id, WordBook.status == 1))
    book = book_result.scalar_one_or_none()
    if not book:
        return None

    count_query = select(func.count()).select_from(WordBookItem).where(WordBookItem.book_id == book_id)
    total = (await db.execute(count_query)).scalar()

    offset = (page - 1) * page_size
    query = (
        select(Word, WordBookItem.sort_order)
        .join(WordBookItem, Word.id == WordBookItem.word_id)
        .where(WordBookItem.book_id == book_id)
        .order_by(WordBookItem.sort_order)
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(query)
    rows = result.all()

    in_word_list_ids = set()
    if user_id and rows:
        word_ids = [row[0].id for row in rows]
        wl_result = await db.execute(
            select(UserWordList.word_id).where(
                UserWordList.user_id == user_id,
                UserWordList.word_id.in_(word_ids),
            )
        )
        in_word_list_ids = {row[0] for row in wl_result.all()}

    word_list = []
    for word, sort_order in rows:
        word_list.append({
            "id": word.id,
            "word": word.word,
            "phonetic": word.phonetic,
            "meaning_cn": word.meaning_cn,
            "part_of_speech": word.part_of_speech,
            "level": word.level,
            "in_word_list": word.id in in_word_list_ids,
        })

    return {"total": total, "page": page, "page_size": page_size, "list": word_list}


async def get_next_word(db: AsyncSession, user_id: int) -> dict | None:
    uwb_result = await db.execute(
        select(UserWordBook).where(UserWordBook.user_id == user_id, UserWordBook.is_current == 1)
    )
    user_book = uwb_result.scalar_one_or_none()
    if not user_book:
        return None

    book_result = await db.execute(select(WordBook).where(WordBook.id == user_book.book_id))
    book = book_result.scalar_one_or_none()
    if not book:
        return None

    word_list_ids_query = select(UserWordList.word_id).where(UserWordList.user_id == user_id)
    word_list_result = await db.execute(word_list_ids_query)
    skip_ids = {row[0] for row in word_list_result.all()}

    query = (
        select(Word, WordBookItem.sort_order)
        .join(WordBookItem, Word.id == WordBookItem.word_id)
        .where(
            WordBookItem.book_id == user_book.book_id,
            WordBookItem.sort_order >= user_book.current_index,
        )
        .order_by(WordBookItem.sort_order)
    )
    result = await db.execute(query)
    rows = result.all()

    for word, sort_order in rows:
        if word.id not in skip_ids:
            return {
                "id": word.id,
                "word": word.word,
                "phonetic": word.phonetic,
                "meaning_cn": word.meaning_cn,
                "part_of_speech": word.part_of_speech,
                "level": word.level,
                "book_info": {
                    "book_id": book.id,
                    "book_name": book.name,
                    "current_index": sort_order,
                    "total_count": book.word_count,
                },
            }

    return None


async def get_word_detail(db: AsyncSession, word_id: int, user_id: int | None = None) -> dict | None:
    result = await db.execute(select(Word).where(Word.id == word_id))
    word = result.scalar_one_or_none()
    if not word:
        return None

    in_word_list = False
    if user_id:
        wl_result = await db.execute(
            select(UserWordList).where(
                UserWordList.user_id == user_id,
                UserWordList.word_id == word_id,
            )
        )
        in_word_list = wl_result.scalar_one_or_none() is not None

    return {
        "id": word.id,
        "word": word.word,
        "phonetic": word.phonetic,
        "meaning_cn": word.meaning_cn,
        "meaning_en": word.meaning_en,
        "part_of_speech": word.part_of_speech,
        "frequency": word.frequency,
        "level": word.level,
        "example_sentence": word.example_sentence,
        "example_translation": word.example_translation,
        "audio_url": word.audio_url,
        "in_word_list": in_word_list,
        "memory_tips": [],
    }


async def add_to_word_list(db: AsyncSession, user_id: int, word_id: int, source: str) -> None:
    word_result = await db.execute(select(Word).where(Word.id == word_id))
    if not word_result.scalar_one_or_none():
        raise ValueError("单词不存在")

    existing = await db.execute(
        select(UserWordList).where(
            UserWordList.user_id == user_id,
            UserWordList.word_id == word_id,
        )
    )
    if existing.scalar_one_or_none():
        raise ValueError("该单词已在单词本中")

    entry = UserWordList(
        user_id=user_id,
        word_id=word_id,
        source=source,
        status=0,
        review_count=0,
        next_review_at=datetime.now(timezone.utc) + timedelta(days=1),
    )
    db.add(entry)
    await db.commit()


async def remove_from_word_list(db: AsyncSession, user_id: int, word_id: int) -> None:
    result = await db.execute(
        select(UserWordList).where(
            UserWordList.user_id == user_id,
            UserWordList.word_id == word_id,
        )
    )
    entry = result.scalar_one_or_none()
    if not entry:
        raise ValueError("该单词不在单词本中")

    await db.delete(entry)
    await db.commit()


async def update_word_status(db: AsyncSession, user_id: int, word_id: int, status: int) -> None:
    result = await db.execute(
        select(UserWordList).where(
            UserWordList.user_id == user_id,
            UserWordList.word_id == word_id,
        )
    )
    entry = result.scalar_one_or_none()
    if not entry:
        raise ValueError("该单词不在单词本中")

    entry.status = status
    if status == 0:
        entry.review_count += 1
        entry.last_review_at = datetime.now(timezone.utc)
        entry.next_review_at = _calc_next_review(entry.review_count)
    await db.commit()


async def get_word_list(
    db: AsyncSession,
    user_id: int,
    status: int | None = None,
    source: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> dict:
    query = select(UserWordList).where(UserWordList.user_id == user_id)
    if status is not None:
        query = query.where(UserWordList.status == status)
    if source is not None:
        query = query.where(UserWordList.source == source)

    count_query = select(func.count()).select_from(UserWordList).where(UserWordList.user_id == user_id)
    if status is not None:
        count_query = count_query.where(UserWordList.status == status)
    if source is not None:
        count_query = count_query.where(UserWordList.source == source)
    total = (await db.execute(count_query)).scalar()

    offset = (page - 1) * page_size
    query = query.order_by(UserWordList.created_at.desc()).offset(offset).limit(page_size)
    result = await db.execute(query)
    entries = result.scalars().all()

    word_ids = [e.word_id for e in entries]
    word_list = []
    if word_ids:
        words_result = await db.execute(select(Word).where(Word.id.in_(word_ids)))
        words_map = {w.id: w for w in words_result.scalars().all()}

        for entry in entries:
            w = words_map.get(entry.word_id)
            word_list.append({
                "id": entry.id,
                "word_id": entry.word_id,
                "word": w.word if w else "",
                "phonetic": w.phonetic if w else None,
                "meaning_cn": w.meaning_cn if w else "",
                "source": entry.source,
                "status": entry.status,
                "review_count": entry.review_count,
                "next_review_at": entry.next_review_at,
            })

    return {"total": total, "page": page, "page_size": page_size, "list": word_list}


async def get_review_words(db: AsyncSession, user_id: int, limit: int = 20) -> list[dict]:
    result = await db.execute(
        select(UserWordList)
        .where(
            UserWordList.user_id == user_id,
            UserWordList.status == 0,
            UserWordList.next_review_at <= datetime.now(timezone.utc),
        )
        .order_by(UserWordList.next_review_at)
        .limit(limit)
    )
    entries = result.scalars().all()

    if not entries:
        return []

    word_ids = [e.word_id for e in entries]
    words_result = await db.execute(select(Word).where(Word.id.in_(word_ids)))
    words_map = {w.id: w for w in words_result.scalars().all()}

    return [
        {
            "id": entry.id,
            "word_id": entry.word_id,
            "word": words_map[entry.word_id].word if entry.word_id in words_map else "",
            "phonetic": words_map[entry.word_id].phonetic if entry.word_id in words_map else None,
            "meaning_cn": words_map[entry.word_id].meaning_cn if entry.word_id in words_map else "",
            "review_count": entry.review_count,
            "last_review_at": entry.last_review_at,
            "memory_tip": None,
        }
        for entry in entries
    ]


async def create_word(db: AsyncSession, book_id: int | None = None, **kwargs) -> Word:
    existing = await db.execute(select(Word).where(Word.word == kwargs.get("word")))
    if existing.scalar_one_or_none():
        raise ValueError("该单词已存在")

    word = Word(**{k: v for k, v in kwargs.items() if k != "book_id"})
    db.add(word)
    await db.flush()

    if book_id:
        book_result = await db.execute(select(WordBook).where(WordBook.id == book_id))
        if book_result.scalar_one_or_none():
            max_order = await db.execute(
                select(func.max(WordBookItem.sort_order)).where(WordBookItem.book_id == book_id)
            )
            next_order = (max_order.scalar() or 0) + 1
            item = WordBookItem(book_id=book_id, word_id=word.id, sort_order=next_order)
            db.add(item)

    await db.commit()
    await db.refresh(word)
    return word


async def update_word(db: AsyncSession, word_id: int, **kwargs) -> Word:
    result = await db.execute(select(Word).where(Word.id == word_id))
    word = result.scalar_one_or_none()
    if not word:
        raise ValueError("单词不存在")

    if "word" in kwargs and kwargs["word"] and kwargs["word"] != word.word:
        dup = await db.execute(select(Word).where(Word.word == kwargs["word"]))
        if dup.scalar_one_or_none():
            raise ValueError("该单词已存在")

    for key, value in kwargs.items():
        if value is not None:
            setattr(word, key, value)
    await db.commit()
    await db.refresh(word)
    return word


async def delete_word(db: AsyncSession, word_id: int) -> None:
    result = await db.execute(select(Word).where(Word.id == word_id))
    word = result.scalar_one_or_none()
    if not word:
        raise ValueError("单词不存在")

    await db.execute(
        select(WordBookItem).where(WordBookItem.word_id == word_id)
    )
    items_result = await db.execute(
        select(WordBookItem).where(WordBookItem.word_id == word_id)
    )
    for item in items_result.scalars().all():
        await db.delete(item)

    await db.delete(word)
    await db.commit()
