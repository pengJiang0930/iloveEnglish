# 口语翻译模块

---

## 一、功能概述

用户输入中文日常用语，AI 翻译成英文，并提供句子拆解（单词/短语释义）、语法讲解（大白话），支持单词添加到单词本。

---

## 二、核心流程

```
输入中文 → AI翻译成英文 → 句子拆解 → 语法讲解 → 点击生词加入单词本
```

---

## 三、翻译结果结构

### 3.1 翻译结果页包含
1. **英文翻译** — 自然、地道的英文表达
2. **发音播放** — 点击朗读英文翻译
3. **句子拆解** — 每个单词/短语的中文释义，可点击添加到单词本
4. **语法讲解** — 用大白话解释时态、句型结构等
5. **收藏/分享** — 收藏经典句子

### 3.2 句子拆解数据结构

```json
{
  "words": [
    {
      "word": "I",
      "meaning": "我",
      "is_phrase": false,
      "position": 0
    },
    {
      "word": "went to bed",
      "meaning": "上床睡觉",
      "is_phrase": true,
      "position": 1
    },
    {
      "word": "early",
      "meaning": "早地",
      "is_phrase": false,
      "position": 2
    }
  ]
}
```

### 3.3 语法讲解数据结构

```json
{
  "tense": "一般过去时",
  "structure": "主语 + 谓语 + 状语",
  "points": [
    {
      "point": "went to bed",
      "explanation": "go to bed 的过去式，表示上床睡觉"
    },
    {
      "point": "early",
      "explanation": "副词，修饰动词，表示早地"
    }
  ]
}
```

---

## 四、数据表结构

### translate_history — 翻译历史表

```sql
CREATE TABLE `translate_history` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `chinese_text` text NOT NULL COMMENT '中文原文',
  `english_text` text NOT NULL COMMENT '英文翻译',
  `grammar_analysis` text DEFAULT NULL COMMENT '语法分析（JSON）',
  `input_type` varchar(10) NOT NULL DEFAULT 'text' COMMENT '输入类型(text=文字,voice=语音)',
  `is_favorite` tinyint NOT NULL DEFAULT 0 COMMENT '是否收藏',
  `word_count` int NOT NULL DEFAULT 0 COMMENT '句子中的单词数',
  `new_word_count` int NOT NULL DEFAULT 0 COMMENT '用户添加到单词本的数量',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_created_at` (`created_at`),
  KEY `idx_is_favorite` (`user_id`, `is_favorite`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='翻译历史表';
```

### translate_word_item — 翻译单词拆解表

```sql
CREATE TABLE `translate_word_item` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `translate_id` bigint NOT NULL COMMENT '翻译记录ID',
  `word_id` bigint DEFAULT NULL COMMENT '单词ID（如果系统词库中有）',
  `word` varchar(100) NOT NULL COMMENT '英文单词/短语',
  `meaning_cn` varchar(500) NOT NULL COMMENT '中文释义',
  `is_phrase` tinyint NOT NULL DEFAULT 0 COMMENT '是否短语(0=单词,1=短语)',
  `sort_order` int NOT NULL DEFAULT 0 COMMENT '在句子中的顺序',
  `added_to_list` tinyint NOT NULL DEFAULT 0 COMMENT '是否已添加到单词本',
  PRIMARY KEY (`id`),
  KEY `idx_translate_id` (`translate_id`),
  KEY `idx_word_id` (`word_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='翻译单词拆解表';
```

---

## 五、交互细节

1. 翻译结果中的**单词/短语可点击**，点击后弹出详情卡片
2. 详情卡片中有 **[+ 加入我的单词本]** 按钮
3. 语法讲解用**大白话**，不使用学术术语
4. 翻译历史可按收藏筛选，支持删除
5. 输入支持文字和语音两种方式（语音为二期功能）

---

## 六、关键业务SQL

### 获取用户的翻译历史（带单词拆解）

```sql
SELECT
  th.*,
  GROUP_CONCAT(
    JSON_OBJECT(
      'word', twi.word,
      'meaning', twi.meaning_cn,
      'is_phrase', twi.is_phrase,
      'added_to_list', twi.added_to_list
    )
  ) as words
FROM translate_history th
LEFT JOIN translate_word_item twi ON th.id = twi.translate_id
WHERE th.user_id = ?
GROUP BY th.id
ORDER BY th.created_at DESC
LIMIT 20;
```
