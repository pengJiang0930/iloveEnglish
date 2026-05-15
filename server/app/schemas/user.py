from typing import Any
from pydantic import BaseModel, Field
from datetime import datetime


class UserRegister(BaseModel):
    phone: str = Field(..., min_length=11, max_length=20, description="手机号")
    password: str = Field(..., min_length=6, max_length=50, description="密码")
    nickname: str = Field(default="", max_length=50, description="昵称")


class UserLogin(BaseModel):
    phone: str = Field(..., description="手机号")
    password: str = Field(..., description="密码")


class UserResponse(BaseModel):
    uid: str
    phone: str | None
    nickname: str
    avatar: str | None
    level: int
    daily_goal: int
    vip_level: int
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    token: str
    user: UserResponse


class ApiResponse(BaseModel):
    code: int = 0
    message: str = "success"
    data: Any = None
