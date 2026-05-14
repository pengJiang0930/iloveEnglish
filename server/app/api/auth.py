from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.user import UserRegister, UserLogin, UserResponse, TokenResponse, ApiResponse
from app.services import user_service
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/register", response_model=ApiResponse, summary="注册")
async def register(body: UserRegister, db: AsyncSession = Depends(get_db)):
    print(f"[REGISTER] phone={body.phone}, password={body.password}, nickname={body.nickname}")
    print(f"[REGISTER] password len={len(body.password)}, bytes={len(body.password.encode('utf-8'))}")
    try:
        result = await user_service.register(db, body.phone, body.password, body.nickname)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"[REGISTER ERROR] {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return ApiResponse(
        message="注册成功",
        data={
            "token": result["token"],
            "user": UserResponse.model_validate(result["user"]).model_dump(),
        },
    )


@router.post("/login", response_model=ApiResponse, summary="登录")
async def login(body: UserLogin, db: AsyncSession = Depends(get_db)):
    try:
        result = await user_service.login(db, body.phone, body.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return ApiResponse(
        message="登录成功",
        data={
            "token": result["token"],
            "user": UserResponse.model_validate(result["user"]).model_dump(),
        },
    )


@router.get("/me", response_model=ApiResponse, summary="获取当前用户信息")
async def get_me(current_user: User = Depends(get_current_user)):
    return ApiResponse(
        data=UserResponse.model_validate(current_user).model_dump(),
    )
