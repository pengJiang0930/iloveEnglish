# 单词 API

---

## 接口概览

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| GET | `/api/words/book/{book_id}` | 是 | 获取词书单词列表（分页） |
| GET | `/api/words/next` | 是 | 获取下一个待学习单词 |
| GET | `/api/words/{id}` | 是 | 获取单词详情 |
| POST | `/api/words/word-list` | 是 | 添加到单词本 |
| DELETE | `/api/words/word-list/{word_id}` | 是 | 从单词本移除 |
| PUT | `/api/words/word-list/{word_id}/status` | 是 | 更新单词掌握状态 |
| GET | `/api/words/word-list` | 是 | 获取用户单词本（分页+筛选） |
| GET | `/api/words/review` | 是 | 获取待复习单词 |

---

## 1. 获取词书单词列表

```
GET /api/words/book/{book_id}?page=1&page_size=20
```

**查询参数**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| page | int | 1 | 页码 |
| page_size | int | 20 | 每页数量 |

**成功响应**：

```json
{
  "code": 0,
  "data": {
    "total": 1000,
    "page": 1,
    "page_size": 20,
    "list": [
      {
        "id": 1,
        "word": "abandon",
        "phonetic": "/əˈbændən/",
        "meaning_cn": "v. 放弃；抛弃",
        "part_of_speech": "v.",
        "level": 2,
        "in_word_list": false
      }
    ]
  }
}
```

---

## 2. 获取下一个待学习单词

```
GET /api/words/next
```

**成功响应**：

```json
{
  "code": 0,
  "data": {
    "id": 51,
    "word": "ability",
    "phonetic": "/əˈbɪləti/",
    "meaning_cn": "n. 能力；才能",
    "part_of_speech": "n.",
    "level": 1,
    "book_info": {
      "book_id": 1,
      "book_name": "高频核心1000词",
      "current_index": 50,
      "total_count": 1000
    }
  }
}
```

**逻辑**：根据 `user_word_book.is_current` 和 `current_index`，跳过已加入单词本的单词，返回下一个。

---

## 3. 获取单词详情

```
GET /api/words/{id}
```

**成功响应**：

```json
{
  "code": 0,
  "data": {
    "id": 1,
    "word": "abandon",
    "phonetic": "/əˈbændən/",
    "meaning_cn": "v. 放弃；抛弃",
    "meaning_en": "to leave someone or something permanently",
    "part_of_speech": "v.",
    "frequency": 5000,
    "level": 2,
    "example_sentence": "He abandoned his wife and children.",
    "example_translation": "他抛弃了妻子和孩子。",
    "audio_url": null,
    "in_word_list": false,
    "memory_tips": [
      {
        "id": 1,
        "tip_type": "split",
        "content": "a + band + on：一个乐队在上面演奏，被放弃了",
        "like_count": 10,
        "is_official": 1
      }
    ]
  }
}
```

---

## 4. 添加到单词本

```
POST /api/words/word-list
```

**请求体**：

```json
{
  "word_id": 1,
  "source": "book"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| word_id | int | 单词ID |
| source | string | 来源：book / translate |

**成功响应**：

```json
{
  "code": 0,
  "message": "添加成功"
}
```

**业务规则**：同一用户对同一单词只能添加一次。

---

## 5. 从单词本移除

```
DELETE /api/words/word-list/{word_id}
```

**成功响应**：

```json
{
  "code": 0,
  "message": "移除成功"
}
```

---

## 6. 更新单词掌握状态

```
PUT /api/words/word-list/{word_id}/status
```

**请求体**：

```json
{
  "status": 1
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| status | int | 0=未掌握, 1=已掌握 |

**成功响应**：

```json
{
  "code": 0,
  "message": "更新成功"
}
```

---

## 7. 获取用户单词本

```
GET /api/words/word-list?status=0&source=book&page=1&page_size=20
```

**查询参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| status | int | 掌握状态筛选：0=未掌握, 1=已掌握 |
| source | string | 来源筛选：book / translate |
| page | int | 页码，默认1 |
| page_size | int | 每页数量，默认20 |

**成功响应**：

```json
{
  "code": 0,
  "data": {
    "total": 100,
    "page": 1,
    "page_size": 20,
    "list": [
      {
        "id": 1,
        "word_id": 1,
        "word": "abandon",
        "phonetic": "/əˈbændən/",
        "meaning_cn": "v. 放弃；抛弃",
        "source": "book",
        "status": 0,
        "review_count": 0,
        "next_review_at": "2026-05-15T10:00:00"
      }
    ]
  }
}
```

---

## 8. 获取待复习单词

```
GET /api/words/review?limit=20
```

**查询参数**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| limit | int | 20 | 返回数量 |

**成功响应**：

```json
{
  "code": 0,
  "data": [
    {
      "id": 1,
      "word_id": 1,
      "word": "abandon",
      "phonetic": "/əˈbændən/",
      "meaning_cn": "v. 放弃；抛弃",
      "review_count": 1,
      "last_review_at": "2026-05-14T10:00:00",
      "memory_tip": "a + band + on：一个乐队在上面演奏，被放弃了"
    }
  ]
}
```

**逻辑**：返回 `next_review_at <= NOW()` 且 `status=0` 的单词，按 `next_review_at` 排序。

---

## DTO 定义

### AddToWordListRequest

```python
class AddToWordListRequest(BaseModel):
    word_id: int
    source: str  # "book" | "translate"
```

### UpdateWordStatusRequest

```python
class UpdateWordStatusRequest(BaseModel):
    status: int  # 0=未掌握, 1=已掌握
```
