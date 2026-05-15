from pydantic import BaseModel, Field
from datetime import datetime


class DashboardStats(BaseModel):
    book_count: int = 0
    word_count: int = 0
    user_count: int = 0


class AdminUserItem(BaseModel):
    id: int
    uid: str
    phone: str | None = None
    nickname: str
    avatar: str | None = None
    level: int
    vip_level: int
    daily_goal: int
    status: int = 1
    last_login_at: str | None = None
    created_at: str | None = None


class AdminUserListData(BaseModel):
    total: int
    page: int
    page_size: int
    list: list[AdminUserItem]


class ToggleUserStatusRequest(BaseModel):
    action: str = Field(..., description="enable / disable")
