# Dev05 - 单词管理

## 目标

实现单词相关接口，包括单词列表、单词详情、用户单词本管理。

## 数据库表

### word - 单词表

```sql
CREATE TABLE `word` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `word` varchar(100) NOT NULL COMMENT '英文单词',
  `phonetic` varchar(100) DEFAULT NULL COMMENT '音标',
  `meaning_cn` varchar(500) NOT NULL COMMENT '中文释义',
  `meaning_en` varchar(500) DEFAULT NULL COMMENT '英文释义',
  `part_of_speech` varchar(50) DEFAULT NULL COMMENT '词性(n./v./adj./adv.等)',
  `frequency` int NOT NULL DEFAULT 0 COMMENT '词频(越高越常用)',
  `level` tinyint NOT NULL DEFAULT 1 COMMENT '难度等级(1-5)',
  `example_sentence` text DEFAULT NULL COMMENT '例句',
  `example_translation` varchar(500) DEFAULT NULL COMMENT '例句翻译',
  `audio_url` varchar(255) DEFAULT NULL COMMENT '发音音频URL',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_word` (`word`),
  KEY `idx_frequency` (`frequency`),
  KEY `idx_level` (`level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='单词表';
```

### word_book_item - 词书-单词关联表

```sql
CREATE TABLE `word_book_item` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `book_id` bigint NOT NULL COMMENT '词书ID',
  `word_id` bigint NOT NULL COMMENT '单词ID',
  `sort_order` int NOT NULL DEFAULT 0 COMMENT '在词书中的排序',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_book_word` (`book_id`, `word_id`),
  KEY `idx_book_id` (`book_id`),
  KEY `idx_word_id` (`word_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='词书-单词关联表';
```

### user_word_list - 用户单词本表

```sql
CREATE TABLE `user_word_list` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `word_id` bigint NOT NULL COMMENT '单词ID',
  `source` varchar(20) NOT NULL COMMENT '来源(book=词书,translate=口语翻译)',
  `status` tinyint NOT NULL DEFAULT 0 COMMENT '掌握状态(0=未掌握,1=已掌握)',
  `review_count` int NOT NULL DEFAULT 0 COMMENT '复习次数',
  `last_review_at` datetime DEFAULT NULL COMMENT '最后复习时间',
  `next_review_at` datetime DEFAULT NULL COMMENT '下次复习时间(艾宾浩斯)',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_word` (`user_id`, `word_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_word_id` (`word_id`),
  KEY `idx_next_review` (`user_id`, `next_review_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户单词本表';
```

## 任务清单

### 5.1 创建数据模型

- [ ] `app/models/word.py` - 单词 ORM 模型
- [ ] `app/models/word_book_item.py` - 词书-单词关联 ORM 模型
- [ ] `app/models/user_word_list.py` - 用户单词本 ORM 模型
- [ ] 更新 `app/models/__init__.py` - 导出新模型

### 5.2 创建 Pydantic Schema

- [ ] `app/schemas/word.py` - 请求/响应模型
  - `WordResponse` - 单词信息响应
  - `WordDetailResponse` - 单词详情响应（含AI速记）
  - `WordListResponse` - 单词列表响应（分页）
  - `UserWordListResponse` - 用户单词本响应
  - `AddToWordListRequest` - 添加到单词本请求
  - `UpdateWordStatusRequest` - 更新单词状态请求

### 5.3 创建服务层

- [ ] `app/services/word_service.py` - 单词业务逻辑
  - `get_words_by_book()` - 获取词书中的单词列表
  - `get_word_detail()` - 获取单词详情
  - `get_next_word()` - 获取下一个待学习单词
  - `add_to_word_list()` - 添加到单词本
  - `remove_from_word_list()` - 从单词本移除
  - `update_word_status()` - 更新单词掌握状态
  - `get_user_word_list()` - 获取用户单词本
  - `get_review_words()` - 获取待复习单词

### 5.4 创建 API 路由

- [ ] `app/api/word.py`
  - `GET /api/words/book/{book_id}` - 获取词书单词列表
  - `GET /api/words/{id}` - 获取单词详情
  - `GET /api/words/next` - 获取下一个待学习单词
  - `POST /api/words/word-list` - 添加到单词本
  - `DELETE /api/words/word-list/{word_id}` - 从单词本移除
  - `PUT /api/words/word-list/{word_id}/status` - 更新单词状态
  - `GET /api/words/word-list` - 获取用户单词本
  - `GET /api/words/review` - 获取待复习单词

## API 接口定义

### 获取词书单词列表

```
GET /api/words/book/{book_id}?page=1&page_size=20
Authorization: Bearer <token>
```

**查询参数**：
- `page` (可选): 页码，默认 1
- `page_size` (可选): 每页数量，默认 20

**成功响应**（200）：
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

### 获取单词详情

```
GET /api/words/{id}
Authorization: Bearer <token>
```

**成功响应**（200）：
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
    "audio_url": "https://...",
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

### 获取下一个待学习单词

```
GET /api/words/next
Authorization: Bearer <token>
```

**成功响应**（200）：
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

### 添加到单词本

```
POST /api/words/word-list
Authorization: Bearer <token>
```

**请求体**：
```json
{
  "word_id": 1,
  "source": "book"
}
```

**成功响应**（200）：
```json
{
  "code": 0,
  "message": "添加成功"
}
```

### 从单词本移除

```
DELETE /api/words/word-list/{word_id}
Authorization: Bearer <token>
```

**成功响应**（200）：
```json
{
  "code": 0,
  "message": "移除成功"
}
```

### 更新单词状态

```
PUT /api/words/word-list/{word_id}/status
Authorization: Bearer <token>
```

**请求体**：
```json
{
  "status": 1
}
```

**成功响应**（200）：
```json
{
  "code": 0,
  "message": "更新成功"
}
```

### 获取用户单词本

```
GET /api/words/word-list?status=0&source=book&page=1&page_size=20
Authorization: Bearer <token>
```

**查询参数**：
- `status` (可选): 掌握状态筛选 (0=未掌握, 1=已掌握)
- `source` (可选): 来源筛选 (book=词书, translate=口语翻译)
- `page` (可选): 页码，默认 1
- `page_size` (可选): 每页数量，默认 20

**成功响应**（200）：
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

### 获取待复习单词

```
GET /api/words/review?limit=20
Authorization: Bearer <token>
```

**查询参数**：
- `limit` (可选): 数量限制，默认 20

**成功响应**（200）：
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

## 验证标准

- [ ] 词书单词列表接口正常返回
- [ ] 分页功能正常
- [ ] 单词详情接口正常返回
- [ ] 获取下一个待学习单词功能正常
- [ ] 添加到单词本功能正常
- [ ] 重复添加返回提示
- [ ] 从单词本移除功能正常
- [ ] 更新单词状态功能正常
- [ ] 用户单词本查询正常
- [ ] 待复习单词查询正常
