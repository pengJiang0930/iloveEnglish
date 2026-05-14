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
