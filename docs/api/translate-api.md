# 翻译 API （规划中）

> **状态**：后端接口尚未实现，以下为规划中的 API 设计。

---

## 接口概览

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| POST | `/api/translate` | 是 | 翻译中文到英文 |
| GET | `/api/translate/history` | 是 | 获取翻译历史 |
| DELETE | `/api/translate/history/{id}` | 是 | 删除翻译历史 |
| POST | `/api/translate/history/{id}/favorite` | 是 | 收藏/取消收藏 |

---

## 1. 翻译中文到英文

```
POST /api/translate
```

**请求体**：

```json
{
  "chinese_text": "我昨天睡得可早了，今天早早就醒过来了，真舒服",
  "input_type": "text"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| chinese_text | string | 是 | 中文句子 |
| input_type | string | 否 | 输入类型：text / voice，默认 text |

**成功响应**：

```json
{
  "code": 0,
  "data": {
    "id": 1,
    "chinese_text": "我昨天睡得可早了，今天早早就醒过来了，真舒服",
    "english_text": "I went to bed really early yesterday and woke up early today. It feels so good!",
    "words": [
      { "word": "I", "meaning": "我", "is_phrase": false, "position": 0 },
      { "word": "went to bed", "meaning": "上床睡觉", "is_phrase": true, "position": 1 },
      { "word": "really", "meaning": "真的、非常", "is_phrase": false, "position": 2 },
      { "word": "early", "meaning": "早", "is_phrase": false, "position": 3 },
      { "word": "yesterday", "meaning": "昨天", "is_phrase": false, "position": 4 },
      { "word": "woke up", "meaning": "醒来", "is_phrase": true, "position": 5 },
      { "word": "feels", "meaning": "感觉", "is_phrase": false, "position": 6 },
      { "word": "so good", "meaning": "很舒服", "is_phrase": true, "position": 7 }
    ],
    "grammar": {
      "tense": "一般过去时",
      "structure": "主语 + 谓语 + 状语",
      "points": [
        { "point": "went to bed", "explanation": "go to bed 的过去式，表示上床睡觉" },
        { "point": "woke up", "explanation": "wake up 的过去式，表示醒来" }
      ]
    },
    "is_favorite": false,
    "created_at": "2026-05-14T15:30:00"
  }
}
```

---

## 2. 获取翻译历史

```
GET /api/translate/history?is_favorite=0&page=1&page_size=20
```

**查询参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| is_favorite | int | 筛选：0=全部, 1=仅收藏 |
| page | int | 页码，默认1 |
| page_size | int | 每页数量，默认20 |

**成功响应**：

```json
{
  "code": 0,
  "data": {
    "total": 50,
    "page": 1,
    "page_size": 20,
    "list": [
      {
        "id": 1,
        "chinese_text": "我昨天睡得可早了，今天早早就醒过来了",
        "english_text": "I went to bed really early yesterday...",
        "is_favorite": true,
        "created_at": "2026-05-14T15:30:00"
      }
    ]
  }
}
```

---

## 3. 删除翻译历史

```
DELETE /api/translate/history/{id}
```

**成功响应**：

```json
{
  "code": 0,
  "message": "删除成功"
}
```

---

## 4. 收藏/取消收藏

```
POST /api/translate/history/{id}/favorite
```

**成功响应**：

```json
{
  "code": 0,
  "message": "已收藏"
}
```

---

## DTO 定义（规划）

### TranslateRequest

```python
class TranslateRequest(BaseModel):
    chinese_text: str
    input_type: str = "text"  # "text" | "voice"
```

### TranslateResponse

```python
class TranslateResponse(BaseModel):
    id: int
    chinese_text: str
    english_text: str
    words: list[WordItem]
    grammar: GrammarAnalysis | None
    is_favorite: bool
    created_at: datetime

class WordItem(BaseModel):
    word: str
    meaning: str
    is_phrase: bool
    position: int
    word_id: int | None = None

class GrammarAnalysis(BaseModel):
    tense: str
    structure: str
    points: list[GrammarPoint]

class GrammarPoint(BaseModel):
    point: str
    explanation: str
```
