# AI速记 API

---

## 接口概览

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| GET | `/api/memory-tips/word/{word_id}` | 是 | 获取单词的速记列表 |
| POST | `/api/memory-tips/generate` | 是 | 生成新的速记内容 |
| POST | `/api/memory-tips/{id}/like` | 是 | 点赞速记 |
| GET | `/api/memory-tips/popular` | 是 | 获取热门速记 |

---

## 1. 获取单词速记

```
GET /api/memory-tips/word/{word_id}
```

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| word_id | int | 单词ID |

**成功响应**：

```json
{
  "code": 0,
  "data": [
    {
      "id": 1,
      "word_id": 1,
      "tip_type": "split",
      "content": "a + band + on：一个乐队在上面演奏，被放弃了",
      "like_count": 10,
      "is_official": 1,
      "created_at": "2026-05-14T10:00:00"
    },
    {
      "id": 2,
      "word_id": 1,
      "tip_type": "phonetic",
      "content": "谐音：一个笨蛋，被抛弃了",
      "like_count": 5,
      "is_official": 0,
      "created_at": "2026-05-14T11:00:00"
    }
  ]
}
```

**排序规则**：`is_official=1` 优先，其次按 `like_count` 降序。

---

## 2. 生成速记

```
POST /api/memory-tips/generate
```

**请求体**：

```json
{
  "word_id": 1,
  "tip_type": "split"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| word_id | int | 单词ID |
| tip_type | string | 速记类型（可选） |

**tip_type 枚举**：

| 值 | 说明 |
|----|------|
| phonetic | 谐音法 |
| split | 拆词法 |
| association | 联想法 |
| story | 故事法 |
| root | 词根词缀法 |

**成功响应**：

```json
{
  "code": 0,
  "data": {
    "id": 3,
    "word_id": 1,
    "tip_type": "split",
    "content": "a + band + on：想象一个乐队站在舞台上表演",
    "like_count": 0,
    "is_official": 0,
    "created_at": "2026-05-14T12:00:00"
  }
}
```

---

## 3. 点赞速记

```
POST /api/memory-tips/{id}/like
```

**成功响应**：

```json
{
  "code": 0,
  "message": "点赞成功"
}
```

---

## 4. 获取热门速记

```
GET /api/memory-tips/popular?limit=10
```

**查询参数**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| limit | int | 10 | 返回数量 |

**成功响应**：

```json
{
  "code": 0,
  "data": [
    {
      "id": 1,
      "word_id": 1,
      "word": "abandon",
      "tip_type": "split",
      "content": "a + band + on：一个乐队在上面演奏，被放弃了",
      "like_count": 10,
      "is_official": 1
    }
  ]
}
```

---

## DTO 定义

### GenerateMemoryTipRequest

```python
class GenerateMemoryTipRequest(BaseModel):
    word_id: int
    tip_type: str | None = None
```

### MemoryTipResponse

```python
class MemoryTipResponse(BaseModel):
    id: int
    word_id: int
    tip_type: str
    content: str
    like_count: int
    is_official: int
    created_at: datetime
```
