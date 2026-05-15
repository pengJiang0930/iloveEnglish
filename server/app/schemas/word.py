from pydantic import BaseModel, Field
from datetime import datetime


class WordResponse(BaseModel):
    id: int
    word: str
    phonetic: str | None = None
    meaning_cn: str
    part_of_speech: str | None = None
    level: int = 1

    model_config = {"from_attributes": True}


class WordBookListItem(WordResponse):
    in_word_list: bool = False


class WordListData(BaseModel):
    total: int
    page: int
    page_size: int
    list: list[WordBookListItem]


class MemoryTipItem(BaseModel):
    id: int
    tip_type: str
    content: str
    like_count: int = 0
    is_official: int = 0


class WordDetailResponse(WordResponse):
    meaning_en: str | None = None
    frequency: int = 0
    example_sentence: str | None = None
    example_translation: str | None = None
    audio_url: str | None = None
    in_word_list: bool = False
    memory_tips: list[MemoryTipItem] = []


class NextWordBookInfo(BaseModel):
    book_id: int
    book_name: str
    current_index: int
    total_count: int


class NextWordResponse(BaseModel):
    id: int
    word: str
    phonetic: str | None = None
    meaning_cn: str
    part_of_speech: str | None = None
    level: int = 1
    book_info: NextWordBookInfo | None = None


class AddToWordListRequest(BaseModel):
    word_id: int = Field(..., description="单词ID")
    source: str = Field(default="book", description="来源：book / translate")


class UpdateWordStatusRequest(BaseModel):
    status: int = Field(..., description="0=未掌握, 1=已掌握")


class WordCreateRequest(BaseModel):
    word: str = Field(..., max_length=100, description="英文单词")
    phonetic: str | None = Field(None, max_length=100, description="音标")
    meaning_cn: str = Field(..., max_length=500, description="中文释义")
    meaning_en: str | None = Field(None, max_length=500, description="英文释义")
    part_of_speech: str | None = Field(None, max_length=50, description="词性")
    frequency: int = Field(default=0, description="词频")
    level: int = Field(default=1, description="难度等级 1-5")
    example_sentence: str | None = Field(None, description="例句")
    example_translation: str | None = Field(None, max_length=500, description="例句翻译")
    audio_url: str | None = Field(None, max_length=255, description="发音音频URL")
    book_id: int | None = Field(None, description="所属词书ID（可选）")


class WordUpdateRequest(BaseModel):
    word: str | None = Field(None, max_length=100, description="英文单词")
    phonetic: str | None = Field(None, max_length=100, description="音标")
    meaning_cn: str | None = Field(None, max_length=500, description="中文释义")
    meaning_en: str | None = Field(None, max_length=500, description="英文释义")
    part_of_speech: str | None = Field(None, max_length=50, description="词性")
    frequency: int | None = Field(None, description="词频")
    level: int | None = Field(None, description="难度等级")
    example_sentence: str | None = Field(None, description="例句")
    example_translation: str | None = Field(None, max_length=500, description="例句翻译")
    audio_url: str | None = Field(None, max_length=255, description="发音音频URL")


class UserWordListItem(BaseModel):
    id: int
    word_id: int
    word: str
    phonetic: str | None = None
    meaning_cn: str
    source: str
    status: int
    review_count: int = 0
    next_review_at: datetime | None = None


class UserWordListData(BaseModel):
    total: int
    page: int
    page_size: int
    list: list[UserWordListItem]


class ReviewWordItem(BaseModel):
    id: int
    word_id: int
    word: str
    phonetic: str | None = None
    meaning_cn: str
    review_count: int = 0
    last_review_at: datetime | None = None
    memory_tip: str | None = None
