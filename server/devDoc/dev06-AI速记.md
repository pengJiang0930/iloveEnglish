# Dev06 - AI速记

## 目标

实现AI速记功能，为单词生成记忆技巧，支持用户反馈。

## 数据库表

### word_memory_tip - AI速记内容表

```sql
CREATE TABLE `word_memory_tip` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `word_id` bigint NOT NULL COMMENT '单词ID',
  `tip_type` varchar(20) NOT NULL COMMENT '记忆方法类型',
  `content` text NOT NULL COMMENT '速记内容',
  `like_count` int NOT NULL DEFAULT 0 COMMENT '点赞数',
  `is_official` tinyint NOT NULL DEFAULT 0 COMMENT '是否官方推荐',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_word_id` (`word_id`),
  KEY `idx_tip_type` (`tip_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI速记内容表';
```

### 速记类型说明

| 值 | 说明 | 示例 |
|----|------|------|
| phonetic | 谐音法 | abandon → "一个笨蛋"被抛弃 |
| split | 拆词法 | abandon → a + band + on |
| association | 联想法 | abandon → 想象一个被遗弃的场景 |
| story | 故事法 | abandon → 编一个小故事 |
| root | 词根词缀法 | abandon → ab(离开) + band(捆绑) + on |

## 任务清单

### 6.1 创建数据模型

- [ ] `app/models/word_memory_tip.py` - AI速记 ORM 模型
- [ ] 更新 `app/models/__init__.py` - 导出新模型

### 6.2 创建 Pydantic Schema

- [ ] `app/schemas/word_memory_tip.py` - 请求/响应模型
  - `MemoryTipResponse` - 速记内容响应
  - `GenerateMemoryTipRequest` - 生成速记请求
  - `LikeMemoryTipRequest` - 点赞请求

### 6.3 创建 AI 服务

- [ ] `app/services/ai_service.py` - AI 服务
  - `generate_memory_tip()` - 生成速记内容
  - 设计 Prompt 模板
  - 调用大模型 API
  - 解析返回结果

### 6.4 创建服务层

- [ ] `app/services/memory_tip_service.py` - 速记业务逻辑
  - `get_memory_tips()` - 获取单词的速记内容
  - `generate_memory_tip()` - 生成新的速记内容
  - `like_memory_tip()` - 点赞速记
  - `get_popular_tips()` - 获取热门速记

### 6.5 创建 API 路由

- [ ] `app/api/memory_tip.py`
  - `GET /api/memory-tips/word/{word_id}` - 获取单词速记
  - `POST /api/memory-tips/generate` - 生成速记
  - `POST /api/memory-tips/{id}/like` - 点赞速记
  - `GET /api/memory-tips/popular` - 获取热门速记

## API 接口定义

### 获取单词速记

```
GET /api/memory-tips/word/{word_id}
Authorization: Bearer <token>
```

**成功响应**（200）：
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

### 生成速记

```
POST /api/memory-tips/generate
Authorization: Bearer <token>
```

**请求体**：
```json
{
  "word_id": 1,
  "tip_type": "split"
}
```

**成功响应**（200）：
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

### 点赞速记

```
POST /api/memory-tips/{id}/like
Authorization: Bearer <token>
```

**成功响应**（200）：
```json
{
  "code": 0,
  "message": "点赞成功"
}
```

### 获取热门速记

```
GET /api/memory-tips/popular?limit=10
Authorization: Bearer <token>
```

**查询参数**：
- `limit` (可选): 数量限制，默认 10

**成功响应**（200）：
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

## AI Prompt 设计

### 谐音法 Prompt

```
请为英语单词 "{word}" 设计一个谐音记忆法。
要求：
1. 找到与单词发音相似的中文谐音
2. 谐音要能帮助记忆单词的意思
3. 内容简洁有趣，容易记忆
4. 返回格式：只返回谐音内容，不要其他解释
```

### 拆词法 Prompt

```
请为英语单词 "{word}" 设计一个拆词记忆法。
要求：
1. 将单词拆分成有意义的部分
2. 解释每个部分的含义
3. 将各部分串联起来帮助记忆单词意思
4. 返回格式：只返回拆词内容，不要其他解释
```

### 联想法 Prompt

```
请为英语单词 "{word}" 设计一个联想记忆法。
要求：
1. 基于单词的意思创造一个生动的画面或场景
2. 画面要与单词意思相关
3. 画面要容易想象和记忆
4. 返回格式：只返回联想内容，不要其他解释
```

### 故事法 Prompt

```
请为英语单词 "{word}" 设计一个故事记忆法。
要求：
1. 编一个简短的小故事
2. 故事要包含单词的意思
3. 故事要有趣、容易记忆
4. 返回格式：只返回故事内容，不要其他解释
```

### 词根词缀法 Prompt

```
请为英语单词 "{word}" 设计一个词根词缀记忆法。
要求：
1. 分析单词的词根和词缀
2. 解释词根和词缀的含义
3. 说明如何组合起来表示单词的意思
4. 返回格式：只返回词根词缀分析，不要其他解释
```

## 验证标准

- [ ] 获取单词速记接口正常返回
- [ ] 生成速记功能正常（需配置 AI API）
- [ ] 点赞功能正常
- [ ] 点赞数正确更新
- [ ] 热门速记查询正常
- [ ] 速记内容按点赞数排序
- [ ] 官方推荐速记优先展示
