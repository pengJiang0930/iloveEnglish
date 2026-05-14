# Dev04 - 词书管理

## 目标

实现词书相关接口，包括词书列表、词书详情、用户词书进度管理。

## 数据库表

### word_book - 词书表

```sql
CREATE TABLE `word_book` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '词书名称',
  `description` varchar(500) DEFAULT NULL COMMENT '词书描述',
  `category` varchar(50) NOT NULL COMMENT '分类(core/exam/daily)',
  `word_count` int NOT NULL DEFAULT 0 COMMENT '单词总数',
  `cover_image` varchar(255) DEFAULT NULL COMMENT '封面图片',
  `sort_order` int NOT NULL DEFAULT 0 COMMENT '排序',
  `is_free` tinyint NOT NULL DEFAULT 1 COMMENT '是否免费(0=付费,1=免费)',
  `status` tinyint NOT NULL DEFAULT 1 COMMENT '状态(0=下架,1=上架)',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_category` (`category`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='词书表';
```

### user_word_book - 用户词书进度表

```sql
CREATE TABLE `user_word_book` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `book_id` bigint NOT NULL COMMENT '词书ID',
  `current_index` int NOT NULL DEFAULT 0 COMMENT '当前学习到第几个单词',
  `learned_count` int NOT NULL DEFAULT 0 COMMENT '已学单词数',
  `mastered_count` int NOT NULL DEFAULT 0 COMMENT '已掌握单词数',
  `is_current` tinyint NOT NULL DEFAULT 0 COMMENT '是否为当前学习的词书',
  `status` tinyint NOT NULL DEFAULT 1 COMMENT '状态(0=未开始,1=学习中,2=已完成)',
  `started_at` datetime DEFAULT NULL COMMENT '开始学习时间',
  `finished_at` datetime DEFAULT NULL COMMENT '完成学习时间',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_book` (`user_id`, `book_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_book_id` (`book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户词书进度表';
```

## 任务清单

### 4.1 创建数据模型

- [ ] `app/models/word_book.py` - 词书 ORM 模型
- [ ] `app/models/user_word_book.py` - 用户词书进度 ORM 模型
- [ ] 更新 `app/models/__init__.py` - 导出新模型

### 4.2 创建 Pydantic Schema

- [ ] `app/schemas/word_book.py` - 请求/响应模型
  - `WordBookResponse` - 词书信息响应
  - `WordBookListResponse` - 词书列表响应
  - `UserWordBookResponse` - 用户词书进度响应
  - `SelectWordBookRequest` - 选择词书请求

### 4.3 创建服务层

- [ ] `app/services/word_book_service.py` - 词书业务逻辑
  - `get_book_list()` - 获取词书列表（按分类筛选）
  - `get_book_detail()` - 获取词书详情
  - `select_book()` - 用户选择词书
  - `get_user_books()` - 获取用户的词书列表
  - `get_current_book()` - 获取用户当前词书
  - `update_progress()` - 更新学习进度

### 4.4 创建 API 路由

- [ ] `app/api/word_book.py`
  - `GET /api/word-books` - 获取词书列表
  - `GET /api/word-books/{id}` - 获取词书详情
  - `POST /api/word-books/select` - 用户选择词书
  - `GET /api/word-books/user/current` - 获取用户当前词书
  - `GET /api/word-books/user/list` - 获取用户的词书列表
  - `PUT /api/word-books/user/progress` - 更新学习进度

## API 接口定义

### 获取词书列表

```
GET /api/word-books?category=core
Authorization: Bearer <token>
```

**查询参数**：
- `category` (可选): 分类筛选 (core/exam/daily)

**成功响应**（200）：
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

### 获取词书详情

```
GET /api/word-books/{id}
Authorization: Bearer <token>
```

**成功响应**（200）：
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

### 用户选择词书

```
POST /api/word-books/select
Authorization: Bearer <token>
```

**请求体**：
```json
{
  "book_id": 1
}
```

**成功响应**（200）：
```json
{
  "code": 0,
  "message": "选择成功"
}
```

### 获取用户当前词书

```
GET /api/word-books/user/current
Authorization: Bearer <token>
```

**成功响应**（200）：
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

### 更新学习进度

```
PUT /api/word-books/user/progress
Authorization: Bearer <token>
```

**请求体**：
```json
{
  "book_id": 1,
  "learned_count": 1,
  "mastered_count": 0
}
```

**成功响应**（200）：
```json
{
  "code": 0,
  "message": "更新成功"
}
```

## 验证标准

- [ ] 词书列表接口正常返回
- [ ] 分类筛选功能正常
- [ ] 词书详情接口正常返回
- [ ] 用户选择词书功能正常
- [ ] 用户当前词书查询正常
- [ ] 学习进度更新功能正常
- [ ] 重复选择词书返回提示
