from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.user import ApiResponse
from app.schemas.admin import ToggleUserStatusRequest
from app.services import admin_service
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/admin", tags=["管理端"])


@router.get("/dashboard", response_model=ApiResponse, summary="仪表盘统计数据")
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await admin_service.get_dashboard_stats(db)
    return ApiResponse(data=result)


@router.get("/users", response_model=ApiResponse, summary="用户列表")
async def get_user_list(
    phone: str | None = Query(None),
    nickname: str | None = Query(None),
    status: int | None = Query(None, description="1=正常, 0=禁用"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await admin_service.get_user_list(db, phone, nickname, status, page, page_size)
    return ApiResponse(data=result)


@router.put("/users/{user_id}/status", response_model=ApiResponse, summary="启用/禁用用户")
async def toggle_user_status(
    user_id: int,
    body: ToggleUserStatusRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        await admin_service.toggle_user_status(db, user_id, body.action)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ApiResponse(message="操作成功")
