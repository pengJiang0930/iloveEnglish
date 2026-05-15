from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db
from app.schemas.user import ApiResponse

router = APIRouter(tags=["系统"])


@router.get("/api/health", response_model=ApiResponse, summary="健康检查")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return ApiResponse(data={"status": "healthy", "database": db_status})
