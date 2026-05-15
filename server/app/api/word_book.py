from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.word_book import (
    WordBookResponse,
    WordBookDetailResponse,
    SelectWordBookRequest,
    UpdateProgressRequest,
    WordBookCreateRequest,
    WordBookUpdateRequest,
)
from app.schemas.user import ApiResponse
from app.services import word_book_service
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/word-books", tags=["词书"])


@router.get("", response_model=ApiResponse, summary="获取词书列表")
async def get_book_list(
    category: str | None = None,
    include_inactive: bool = False,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    books = await word_book_service.get_book_list(db, category, include_inactive)
    return ApiResponse(
        data=[WordBookResponse.model_validate(b).model_dump() for b in books]
    )


@router.get("/user/current", response_model=ApiResponse, summary="获取用户当前词书")
async def get_current_book(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await word_book_service.get_current_book(db, current_user.id)
    if not result:
        return ApiResponse(data=None)
    return ApiResponse(data=result)


@router.get("/user/list", response_model=ApiResponse, summary="获取用户的词书列表")
async def get_user_books(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await word_book_service.get_user_books(db, current_user.id)
    return ApiResponse(data=result)


@router.post("/select", response_model=ApiResponse, summary="用户选择词书")
async def select_book(
    body: SelectWordBookRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        await word_book_service.select_book(db, current_user.id, body.book_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ApiResponse(message="选择成功")


@router.put("/user/progress", response_model=ApiResponse, summary="更新学习进度")
async def update_progress(
    body: UpdateProgressRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        await word_book_service.update_progress(
            db, current_user.id, body.book_id, body.learned_count, body.mastered_count
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ApiResponse(message="更新成功")


@router.get("/{book_id}", response_model=ApiResponse, summary="获取词书详情")
async def get_book_detail(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await word_book_service.get_book_detail(db, book_id, current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="词书不存在")
    return ApiResponse(data=result)


@router.post("", response_model=ApiResponse, summary="新增词书（管理端）")
async def create_book(
    body: WordBookCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    book = await word_book_service.create_book(db, **body.model_dump())
    return ApiResponse(
        message="创建成功",
        data=WordBookResponse.model_validate(book).model_dump(),
    )


@router.put("/{book_id}", response_model=ApiResponse, summary="编辑词书（管理端）")
async def update_book(
    book_id: int,
    body: WordBookUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        book = await word_book_service.update_book(db, book_id, **body.model_dump(exclude_none=True))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ApiResponse(
        message="更新成功",
        data=WordBookResponse.model_validate(book).model_dump(),
    )


@router.delete("/{book_id}", response_model=ApiResponse, summary="删除词书（管理端）")
async def delete_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        await word_book_service.delete_book(db, book_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ApiResponse(message="删除成功")


@router.put("/{book_id}/status", response_model=ApiResponse, summary="切换词书上架/下架（管理端）")
async def toggle_book_status(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from sqlalchemy import select
    from app.models.word_book import WordBook
    result = await db.execute(select(WordBook).where(WordBook.id == book_id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="词书不存在")
    new_status = 0 if book.status == 1 else 1
    await word_book_service.update_book(db, book_id, status=new_status)
    return ApiResponse(message="操作成功")
