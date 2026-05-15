# 词书 API

---

## 接口概览

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| GET | `/api/word-books` | 是 | 获取词书列表 |
| GET | `/api/word-books/{book_id}` | 是 | 获取词书详情 |
| POST | `/api/word-books/select` | 是 | 用户选择词书 |
| GET | `/api/word-books/user/current` | 是 | 获取用户当前词书 |
| GET | `/api/word-books/user/list` | 是 | 获取用户的词书列表 |
| PUT | `/api/word-books/user/progress` | 是 | 更新学习进度 |

---

## 1. 获取词书列表

```
GET /api/word-books?category=core
```

**查询参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| category | string | 否 | 分类筛选：core / exam / daily |

**成功响应**：

```json
{
  "code": 0,
  "data": [
    {
      "id": 1,
      "name": "高频核心1000词",
      "description": "最常用的1000个英语单词",
      "category": "core",
      "word_count": 1000,
      "cover_image": null,
      "is_free": 1,
      "status": 1
    }
  ]
}
```

---

## 2. 获取词书详情

```
GET /api/word-books/{book_id}
```

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| book_id | int | 词书ID |

**成功响应**：

```json
{
  "code": 0,
  "data": {
    "id": 1,
    "name": "高频核心1000词",
    "description": "最常用的1000个英语单词",
    "category": "core",
    "word_count": 1000,
    "cover_image": null,
    "is_free": 1,
    "status": 1,
    "user_progress": {
      "current_index": 50,
      "learned_count": 50,
      "mastered_count": 30,
      "status": 1
    }
  }
}
```

**错误码**：

| 状态码 | 说明 |
|--------|------|
| 404 | 词书不存在 |

---

## 3. 用户选择词书

```
POST /api/word-books/select
```

**请求体**：

```json
{
  "book_id": 1
}
```

**成功响应**：

```json
{
  "code": 0,
  "message": "选择成功"
}
```

**业务规则**：同一时间只有一个 `is_current=1` 的词书。

---

## 4. 获取用户当前词书

```
GET /api/word-books/user/current
```

**成功响应**：

```json
{
  "code": 0,
  "data": {
    "book": {
      "id": 1,
      "name": "高频核心1000词",
      "category": "core",
      "word_count": 1000
    },
    "progress": {
      "current_index": 50,
      "learned_count": 50,
      "mastered_count": 30,
      "status": 1
    }
  }
}
```

---

## 5. 获取用户的词书列表

```
GET /api/word-books/user/list
```

**成功响应**：

```json
{
  "code": 0,
  "data": [
    {
      "id": 1,
      "book_id": 1,
      "book_name": "高频核心1000词",
      "current_index": 50,
      "learned_count": 50,
      "mastered_count": 30,
      "is_current": 1,
      "status": 1
    }
  ]
}
```

---

## 6. 更新学习进度

```
PUT /api/word-books/user/progress
```

**请求体**：

```json
{
  "book_id": 1,
  "learned_count": 1,
  "mastered_count": 0
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| book_id | int | 词书ID |
| learned_count | int | 本次学习单词数 |
| mastered_count | int | 本次掌握单词数 |

**成功响应**：

```json
{
  "code": 0,
  "message": "更新成功"
}
```

---

## DTO 定义

### WordBookResponse

```python
class WordBookResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    category: str
    word_count: int
    cover_image: str | None = None
    is_free: int = 1
    status: int = 1
```

### SelectWordBookRequest

```python
class SelectWordBookRequest(BaseModel):
    book_id: int
```

### UpdateProgressRequest

```python
class UpdateProgressRequest(BaseModel):
    book_id: int
    learned_count: int = 1
    mastered_count: int = 0
```
