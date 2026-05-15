from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.word import (
    AddToWordListRequest,
    UpdateWordStatusRequest,
    WordCreateRequest,
    WordUpdateRequest,
    WordResponse,
)
from app.schemas.user import ApiResponse
from app.services import word_service
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/words", tags=["单词"])


@router.get("/book/{book_id}", response_model=ApiResponse, summary="获取词书单词列表")
async def get_words_by_book(
    book_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await word_service.get_words_by_book(db, book_id, page, page_size, current_user.id)
    if result is None:
        raise HTTPException(status_code=404, detail="词书不存在")
    return ApiResponse(data=result)


@router.get("/next", response_model=ApiResponse, summary="获取下一个待学习单词")
async def get_next_word(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await word_service.get_next_word(db, current_user.id)
    return ApiResponse(data=result)


@router.get("/review", response_model=ApiResponse, summary="获取待复习单词")
async def get_review_words(
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await word_service.get_review_words(db, current_user.id, limit)
    return ApiResponse(data=result)


@router.get("/word-list", response_model=ApiResponse, summary="获取用户单词本")
async def get_word_list(
    status: int | None = Query(None, description="0=未掌握, 1=已掌握"),
    source: str | None = Query(None, description="book / translate"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await word_service.get_word_list(db, current_user.id, status, source, page, page_size)
    return ApiResponse(data=result)


@router.get("/{word_id}", response_model=ApiResponse, summary="获取单词详情")
async def get_word_detail(
    word_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await word_service.get_word_detail(db, word_id, current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="单词不存在")
    return ApiResponse(data=result)


@router.post("/word-list", response_model=ApiResponse, summary="添加到单词本")
async def add_to_word_list(
    body: AddToWordListRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        await word_service.add_to_word_list(db, current_user.id, body.word_id, body.source)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ApiResponse(message="添加成功")


@router.delete("/word-list/{word_id}", response_model=ApiResponse, summary="从单词本移除")
async def remove_from_word_list(
    word_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        await word_service.remove_from_word_list(db, current_user.id, word_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ApiResponse(message="移除成功")


@router.put("/word-list/{word_id}/status", response_model=ApiResponse, summary="更新单词掌握状态")
async def update_word_status(
    word_id: int,
    body: UpdateWordStatusRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        await word_service.update_word_status(db, current_user.id, word_id, body.status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ApiResponse(message="更新成功")


@router.post("/admin", response_model=ApiResponse, summary="新增单词（管理端）")
async def create_word(
    body: WordCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        word = await word_service.create_word(db, **body.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ApiResponse(
        message="创建成功",
        data=WordResponse.model_validate(word).model_dump(),
    )


@router.put("/admin/{word_id}", response_model=ApiResponse, summary="编辑单词（管理端）")
async def update_word(
    word_id: int,
    body: WordUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        word = await word_service.update_word(db, word_id, **body.model_dump(exclude_none=True))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ApiResponse(
        message="更新成功",
        data=WordResponse.model_validate(word).model_dump(),
    )


@router.delete("/admin/{word_id}", response_model=ApiResponse, summary="删除单词（管理端）")
async def delete_word(
    word_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        await word_service.delete_word(db, word_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ApiResponse(message="删除成功")
