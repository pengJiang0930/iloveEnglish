from pydantic import BaseModel, Field
from datetime import datetime


class WordBookResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    category: str
    word_count: int
    cover_image: str | None = None
    is_free: int = 1
    status: int = 1

    model_config = {"from_attributes": True}


class WordBookDetailResponse(WordBookResponse):
    sort_order: int = 0
    user_progress: dict | None = None


class UserWordBookResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    current_index: int = 0
    learned_count: int = 0
    mastered_count: int = 0
    is_current: int = 0
    status: int = 0
    started_at: datetime | None = None
    finished_at: datetime | None = None

    model_config = {"from_attributes": True}


class SelectWordBookRequest(BaseModel):
    book_id: int = Field(..., description="词书ID")


class UpdateProgressRequest(BaseModel):
    book_id: int = Field(..., description="词书ID")
    learned_count: int = Field(default=1, description="学习单词数")
    mastered_count: int = Field(default=0, description="掌握单词数")


class WordBookCreateRequest(BaseModel):
    name: str = Field(..., max_length=100, description="词书名称")
    description: str | None = Field(None, max_length=500, description="描述")
    category: str = Field(..., description="分类: core / exam / daily")
    word_count: int = Field(default=0, description="单词总数")
    cover_image: str | None = Field(None, max_length=255, description="封面图片URL")
    sort_order: int = Field(default=0, description="排序")
    is_free: int = Field(default=1, description="是否免费")
    status: int = Field(default=1, description="状态 0=下架 1=上架")


class WordBookUpdateRequest(BaseModel):
    name: str | None = Field(None, max_length=100, description="词书名称")
    description: str | None = Field(None, max_length=500, description="描述")
    category: str | None = Field(None, description="分类")
    word_count: int | None = Field(None, description="单词总数")
    cover_image: str | None = Field(None, max_length=255, description="封面图片URL")
    sort_order: int | None = Field(None, description="排序")
    is_free: int | None = Field(None, description="是否免费")
    status: int | None = Field(None, description="状态")
