from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.word_book import (
    WordBookResponse,
    WordBookDetailResponse,
    SelectWordBookRequest,
    UpdateProgressRequest,
)
from app.schemas.user import ApiResponse
from app.services import word_book_service
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/word-books", tags=["词书"])


@router.get("", response_model=ApiResponse, summary="获取词书列表")
async def get_book_list(
    category: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    books = await word_book_service.get_book_list(db, category)
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
