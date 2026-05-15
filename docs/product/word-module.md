# 单词与词书模块

---

## 一、功能概述

核心学习模块，包含词书浏览、单词学习、AI速记、用户单词本管理、复习等功能。

---

## 二、词书管理

### 2.1 预置词书分类

| 分类 | 词书名称 | 单词数 |
|------|---------|--------|
| 核心 (core) | 高频核心1000词 | 1000 |
| 核心 (core) | 高频核心2000词 | 2000 |
| 核心 (core) | 高频核心3000词 | 3000 |
| 考试 (exam) | 四级核心词汇 | ~2000 |
| 考试 (exam) | 六级核心词汇 | ~2000 |
| 考试 (exam) | 考研核心词汇 | ~3000 |
| 考试 (exam) | 雅思核心词汇 | ~3000 |
| 考试 (exam) | 托福核心词汇 | ~3000 |
| 日常 (daily) | 日常口语高频词 | ~1000 |
| 日常 (daily) | 生活场景词汇 | ~1000 |

### 2.2 词书字段

| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 词书名称 |
| description | string | 词书描述 |
| category | string | 分类：core / exam / daily |
| word_count | int | 单词总数 |
| cover_image | string | 封面图片URL |
| sort_order | int | 排序序号 |
| is_free | int | 是否免费（0=付费, 1=免费） |
| status | int | 状态（0=下架, 1=上架） |

---

## 三、单词学习

### 3.1 单词字段

| 字段 | 类型 | 说明 |
|------|------|------|
| word | string | 英文单词 |
| phonetic | string | 音标 |
| meaning_cn | string | 中文释义 |
| meaning_en | string | 英文释义 |
| part_of_speech | string | 词性（n./v./adj./adv.等） |
| frequency | int | 词频（越高越常用） |
| level | tinyint | 难度等级（1-5） |
| example_sentence | text | 例句 |
| example_translation | string | 例句翻译 |
| audio_url | string | 发音音频URL |

### 3.2 学习流程

1. 用户选择词书，系统记录为"当前词书"
2. 系统通过 `current_index` 定位下一个待学习单词
3. 用户查看单词卡片（默认隐藏释义）
4. 用户点击显示释义，可选择"认识"/"不认识"
5. 不认识：查看详情和AI速记，可选择加入单词本
6. 每学完一个单词，更新 `user_word_book` 进度

### 3.3 用户词书进度

| 字段 | 说明 |
|------|------|
| current_index | 当前学到第几个单词（sort_order） |
| learned_count | 已学单词数 |
| mastered_count | 已掌握单词数 |
| is_current | 是否为当前学习的词书（同一时间只有一个） |
| status | 0=未开始, 1=学习中, 2=已完成 |

---

## 四、AI速记

### 4.1 速记类型

| 类型 | 说明 | 示例 |
|------|------|------|
| phonetic | 谐音法 | abandon → "一个笨蛋"被抛弃 |
| split | 拆词法 | abandon → a + band + on |
| association | 联想法 | abandon → 想象一个被遗弃的场景 |
| story | 故事法 | abandon → 编一个小故事 |
| root | 词根词缀法 | abandon → ab(离开) + band(捆绑) + on |

### 4.2 展示规则
- 每个单词可以有多条速记内容
- 按点赞数排序，`is_official=1` 的优先展示
- 用户可点击"换个记忆方式"获取其他类型的速记
- 用户可点赞反馈

### 4.3 word_memory_tip 表

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='AI速记内容表';
```

---

## 五、用户单词本

### 5.1 功能说明
- 用户可将单词加入"我的单词本"（来源：词书学习 / 口语翻译）
- 支持按状态筛选（全部/未掌握/已掌握）
- 支持按来源筛选（词书/口语翻译）
- 基于艾宾浩斯遗忘曲线安排复习

### 5.2 字段说明

| 字段 | 说明 |
|------|------|
| word_id | 单词ID |
| source | 来源（book=词书, translate=口语翻译） |
| status | 掌握状态（0=未掌握, 1=已掌握） |
| review_count | 复习次数 |
| last_review_at | 最后复习时间 |
| next_review_at | 下次复习时间（基于艾宾浩斯曲线） |

### 5.3 艾宾浩斯复习间隔

| 复习次数 | 间隔天数 |
|----------|----------|
| 第1次 | 1天 |
| 第2次 | 2天 |
| 第3次 | 4天 |
| 第4次 | 7天 |
| 第5次 | 15天 |
| 第6次 | 30天 |

---

## 六、数据表结构

### word

```sql
CREATE TABLE `word` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `word` varchar(100) NOT NULL COMMENT '英文单词',
  `phonetic` varchar(100) DEFAULT NULL COMMENT '音标',
  `meaning_cn` varchar(500) NOT NULL COMMENT '中文释义',
  `meaning_en` varchar(500) DEFAULT NULL COMMENT '英文释义',
  `part_of_speech` varchar(50) DEFAULT NULL COMMENT '词性',
  `frequency` int NOT NULL DEFAULT 0 COMMENT '词频',
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='单词表';
```

### word_book

```sql
CREATE TABLE `word_book` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '词书名称',
  `description` varchar(500) DEFAULT NULL COMMENT '词书描述',
  `category` varchar(50) NOT NULL COMMENT '分类(core/exam/daily)',
  `word_count` int NOT NULL DEFAULT 0 COMMENT '单词总数',
  `cover_image` varchar(255) DEFAULT NULL COMMENT '封面图片',
  `sort_order` int NOT NULL DEFAULT 0 COMMENT '排序',
  `is_free` tinyint NOT NULL DEFAULT 1 COMMENT '是否免费',
  `status` tinyint NOT NULL DEFAULT 1 COMMENT '状态(0=下架,1=上架)',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_category` (`category`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='词书表';
```

### word_book_item

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='词书-单词关联表';
```

### user_word_book

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户词书进度表';
```

### user_word_list

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户单词本表';
```

---

## 七、关键业务SQL

### 获取用户当前词书的下一个待学习单词

```sql
SELECT w.*
FROM word w
JOIN word_book_item wbi ON w.id = wbi.word_id
JOIN user_word_book uwb ON wbi.book_id = uwb.book_id
WHERE uwb.user_id = ?
  AND uwb.is_current = 1
  AND wbi.sort_order >= uwb.current_index
  AND w.id NOT IN (
    SELECT word_id FROM user_word_list WHERE user_id = ?
  )
ORDER BY wbi.sort_order
LIMIT 1;
```

### 获取用户今日待复习的单词

```sql
SELECT uwl.*, w.word, w.phonetic, w.meaning_cn, wmt.content as memory_tip
FROM user_word_list uwl
JOIN word w ON uwl.word_id = w.id
LEFT JOIN word_memory_tip wmt ON w.id = wmt.word_id AND wmt.is_official = 1
WHERE uwl.user_id = ?
  AND uwl.status = 0
  AND uwl.next_review_at <= NOW()
ORDER BY uwl.next_review_at
LIMIT 20;
```
