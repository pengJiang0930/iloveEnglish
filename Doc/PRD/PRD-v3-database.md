# PRD v3 - 数据库设计文档

> 基于v2功能（AI速记单词 + 日常口语转英语）设计的数据库结构

---

## 一、数据库概览

### 1.1 表清单

| 序号 | 表名 | 说明 | 所属模块 |
|------|------|------|----------|
| 1 | user | 用户表 | 用户 |
| 2 | user_setting | 用户设置表 | 用户 |
| 3 | word_book | 词书表 | 单词 |
| 4 | word | 单词表 | 单词 |
| 5 | word_book_item | 词书-单词关联表 | 单词 |
| 6 | user_word_book | 用户词书进度表 | 单词 |
| 7 | user_word_list | 用户单词本 | 单词 |
| 8 | word_memory_tip | AI速记内容表 | 单词 |
| 9 | translate_history | 翻译历史表 | 口语 |
| 10 | translate_word_item | 翻译单词拆解表 | 口语 |
| 11 | daily_stat | 每日学习统计表 | 统计 |
| 12 | learning_streak | 连续学习记录表 | 统计 |
| 13 | feedback | 用户反馈表 | 系统 |

### 1.2 ER关系图（简化）

```
┌──────────┐     ┌──────────────┐     ┌──────────┐
│  user    │────<│ user_word_   │>────│word_book │
│          │     │ book         │     │          │
└──────────┘     └──────────────┘     └──────────┘
     │                                      │
     │                                      │
     ▼                                      ▼
┌──────────┐     ┌──────────────┐     ┌──────────┐
│  user_   │     │word_book_    │>────│  word    │
│  word_   │     │item          │     │          │
│  list    │     └──────────────┘     └──────────┘
└──────────┘                                  │
     ▲                                        │
     │                                        ▼
     │           ┌──────────────┐     ┌──────────┐
     └───────────│word_memory_  │>────│          │
                 │tip           │     │          │
                 └──────────────┘     └──────────┘

┌──────────┐     ┌──────────────┐     ┌──────────┐
│  user    │────<│translate_    │────<│translate_│
│          │     │history       │     │word_item │
└──────────┘     └──────────────┘     └──────────┘
```

---

## 二、表结构详细设计

### 2.1 user - 用户表

| 字段名 | 类型 | 长度 | 必填 | 默认值 | 说明 |
|--------|------|------|------|--------|------|
| id | bigint | - | 是 | - | 主键，自增 |
| uid | varchar | 32 | 是 | - | 用户唯一标识（UUID） |
| phone | varchar | 20 | 否 | null | 手机号 |
| nickname | varchar | 50 | 是 | '' | 昵称 |
| avatar | varchar | 255 | 否 | null | 头像URL |
| level | tinyint | - | 是 | 1 | 英语等级（1-5） |
| daily_goal | int | - | 是 | 20 | 每日学习目标（单词数） |
| vip_level | tinyint | - | 是 | 0 | 会员等级（0=免费） |
| vip_expire_at | datetime | - | 否 | null | 会员过期时间 |
| last_login_at | datetime | - | 否 | null | 最后登录时间 |
| created_at | datetime | - | 是 | CURRENT_TIMESTAMP | 创建时间 |
| updated_at | datetime | - | 是 | CURRENT_TIMESTAMP | 更新时间 |
| deleted_at | datetime | - | 否 | null | 软删除时间 |

**索引**：
- `idx_uid` UNIQUE (uid)
- `idx_phone` (phone)
- `idx_created_at` (created_at)

**说明**：
- level: 1=零基础, 2=初级, 3=中级, 4=高级, 5=精通
- vip_level: 0=免费用户, 1=月度会员, 2=年度会员, 3=终身会员

---

### 2.2 user_setting - 用户设置表

| 字段名 | 类型 | 长度 | 必填 | 默认值 | 说明 |
|--------|------|------|------|--------|------|
| id | bigint | - | 是 | - | 主键，自增 |
| user_id | bigint | - | 是 | - | 用户ID |
| daily_reminder | tinyint | - | 是 | 1 | 每日提醒（0=关, 1=开） |
| reminder_time | time | - | 是 | '20:00' | 提醒时间 |
| pronunciation | varchar | 10 | 是 | 'us' | 发音偏好（us=美音, uk=英音） |
| theme | varchar | 20 | 是 | 'light' | 主题（light/dark） |
| font_size | varchar | 10 | 是 | 'medium' | 字体大小 |
| created_at | datetime | - | 是 | CURRENT_TIMESTAMP | 创建时间 |
| updated_at | datetime | - | 是 | CURRENT_TIMESTAMP | 更新时间 |

**索引**：
- `idx_user_id` UNIQUE (user_id)

---

### 2.3 word_book - 词书表

| 字段名 | 类型 | 长度 | 必填 | 默认值 | 说明 |
|--------|------|------|------|--------|------|
| id | bigint | - | 是 | - | 主键，自增 |
| name | varchar | 100 | 是 | - | 词书名称 |
| description | varchar | 500 | 否 | null | 词书描述 |
| category | varchar | 50 | 是 | - | 分类 |
| word_count | int | - | 是 | 0 | 单词总数 |
| cover_image | varchar | 255 | 否 | null | 封面图片 |
| sort_order | int | - | 是 | 0 | 排序 |
| is_free | tinyint | - | 是 | 1 | 是否免费（0=付费, 1=免费） |
| status | tinyint | - | 是 | 1 | 状态（0=下架, 1=上架） |
| created_at | datetime | - | 是 | CURRENT_TIMESTAMP | 创建时间 |
| updated_at | datetime | - | 是 | CURRENT_TIMESTAMP | 更新时间 |

**索引**：
- `idx_category` (category)
- `idx_status` (status)

**预置数据**：
| category | name | description |
|----------|------|-------------|
| core | 高频核心1000词 | 最常用的1000个英语单词 |
| core | 高频核心2000词 | 最常用的2000个英语单词 |
| core | 高频核心3000词 | 最常用的3000个英语单词 |
| exam | 四级核心词汇 | 大学英语四级高频词汇 |
| exam | 六级核心词汇 | 大学英语六级高频词汇 |
| exam | 考研核心词汇 | 考研英语高频词汇 |
| exam | 雅思核心词汇 | 雅思考试高频词汇 |
| exam | 托福核心词汇 | 托福考试高频词汇 |
| daily | 日常口语高频词 | 日常对话中最常用的单词 |
| daily | 生活场景词汇 | 购物、餐饮、交通等场景词汇 |

---

### 2.4 word - 单词表

| 字段名 | 类型 | 长度 | 必填 | 默认值 | 说明 |
|--------|------|------|------|--------|------|
| id | bigint | - | 是 | - | 主键，自增 |
| word | varchar | 100 | 是 | - | 英文单词 |
| phonetic | varchar | 100 | 否 | null | 音标 |
| meaning_cn | varchar | 500 | 是 | - | 中文释义 |
| meaning_en | varchar | 500 | 否 | null | 英文释义 |
| part_of_speech | varchar | 50 | 否 | null | 词性（n./v./adj./adv.等） |
| frequency | int | - | 是 | 0 | 词频（越高越常用） |
| level | tinyint | - | 是 | 1 | 难度等级（1-5） |
| example_sentence | text | - | 否 | null | 例句 |
| example_translation | varchar | 500 | 否 | null | 例句翻译 |
| audio_url | varchar | 255 | 否 | null | 发音音频URL |
| created_at | datetime | - | 是 | CURRENT_TIMESTAMP | 创建时间 |
| updated_at | datetime | - | 是 | CURRENT_TIMESTAMP | 更新时间 |

**索引**：
- `idx_word` UNIQUE (word)
- `idx_frequency` (frequency)
- `idx_level` (level)

**说明**：
- frequency: 词频数据可从语料库获取，值越大表示越常用
- level: 1=入门, 2=初级, 3=中级, 4=高级, 5=专业

---

### 2.5 word_book_item - 词书-单词关联表

| 字段名 | 类型 | 长度 | 必填 | 默认值 | 说明 |
|--------|------|------|------|--------|------|
| id | bigint | - | 是 | - | 主键，自增 |
| book_id | bigint | - | 是 | - | 词书ID |
| word_id | bigint | - | 是 | - | 单词ID |
| sort_order | int | - | 是 | 0 | 在词书中的排序 |

**索引**：
- `idx_book_id` (book_id)
- `idx_word_id` (word_id)
- `uk_book_word` UNIQUE (book_id, word_id)

---

### 2.6 user_word_book - 用户词书进度表

| 字段名 | 类型 | 长度 | 必填 | 默认值 | 说明 |
|--------|------|------|------|--------|------|
| id | bigint | - | 是 | - | 主键，自增 |
| user_id | bigint | - | 是 | - | 用户ID |
| book_id | bigint | - | 是 | - | 词书ID |
| current_index | int | - | 是 | 0 | 当前学习到第几个单词 |
| learned_count | int | - | 是 | 0 | 已学单词数 |
| mastered_count | int | - | 是 | 0 | 已掌握单词数 |
| is_current | tinyint | - | 是 | 0 | 是否为当前学习的词书 |
| status | tinyint | - | 是 | 1 | 状态（0=未开始, 1=学习中, 2=已完成） |
| started_at | datetime | - | 否 | null | 开始学习时间 |
| finished_at | datetime | - | 否 | null | 完成学习时间 |
| created_at | datetime | - | 是 | CURRENT_TIMESTAMP | 创建时间 |
| updated_at | datetime | - | 是 | CURRENT_TIMESTAMP | 更新时间 |

**索引**：
- `idx_user_id` (user_id)
- `idx_book_id` (book_id)
- `uk_user_book` UNIQUE (user_id, book_id)

**说明**：
- 用户可以选择多个词书，但同一时间只有一个 is_current=1
- current_index 记录学习进度，下次学习时从该位置继续

---

### 2.7 user_word_list - 用户单词本表

| 字段名 | 类型 | 长度 | 必填 | 默认值 | 说明 |
|--------|------|------|------|--------|------|
| id | bigint | - | 是 | - | 主键，自增 |
| user_id | bigint | - | 是 | - | 用户ID |
| word_id | bigint | - | 是 | - | 单词ID |
| source | varchar | 20 | 是 | - | 来源（book=词书, translate=口语翻译） |
| status | tinyint | - | 是 | 0 | 掌握状态（0=未掌握, 1=已掌握） |
| review_count | int | - | 是 | 0 | 复习次数 |
| last_review_at | datetime | - | 否 | null | 最后复习时间 |
| next_review_at | datetime | - | 否 | null | 下次复习时间（艾宾浩斯） |
| created_at | datetime | - | 是 | CURRENT_TIMESTAMP | 添加时间 |
| updated_at | datetime | - | 是 | CURRENT_TIMESTAMP | 更新时间 |

**索引**：
- `idx_user_id` (user_id)
- `idx_word_id` (word_id)
- `uk_user_word` UNIQUE (user_id, word_id)
- `idx_next_review` (user_id, next_review_at)

**说明**：
- source: 记录单词来源，便于统计分析
- next_review_at: 基于艾宾浩斯遗忘曲线计算的下次复习时间
- 复习间隔：1天、2天、4天、7天、15天、30天

---

### 2.8 word_memory_tip - AI速记内容表

| 字段名 | 类型 | 长度 | 必填 | 默认值 | 说明 |
|--------|------|------|------|--------|------|
| id | bigint | - | 是 | - | 主键，自增 |
| word_id | bigint | - | 是 | - | 单词ID |
| tip_type | varchar | 20 | 是 | - | 记忆方法类型 |
| content | text | - | 是 | - | 速记内容 |
| like_count | int | - | 是 | 0 | 点赞数 |
| is_official | tinyint | - | 是 | 0 | 是否官方推荐 |
| created_at | datetime | - | 是 | CURRENT_TIMESTAMP | 创建时间 |

**索引**：
- `idx_word_id` (word_id)
- `idx_tip_type` (tip_type)

**说明**：
- tip_type: 
  - `phonetic` = 谐音法
  - `split` = 拆词法
  - `association` = 联想法
  - `story` = 故事法
  - `root` = 词根词缀法
- 每个单词可以有多条速记内容，用户可以点赞，点赞数高的优先展示
- 官方推荐的内容 is_official=1，优先展示

---

### 2.9 translate_history - 翻译历史表

| 字段名 | 类型 | 长度 | 必填 | 默认值 | 说明 |
|--------|------|------|------|--------|------|
| id | bigint | - | 是 | - | 主键，自增 |
| user_id | bigint | - | 是 | - | 用户ID |
| chinese_text | text | - | 是 | - | 中文原文 |
| english_text | text | - | 是 | - | 英文翻译 |
| grammar_analysis | text | - | 否 | null | 语法分析（JSON） |
| input_type | varchar | 10 | 是 | 'text' | 输入类型（text=文字, voice=语音） |
| is_favorite | tinyint | - | 是 | 0 | 是否收藏 |
| word_count | int | - | 是 | 0 | 句子中的单词数 |
| new_word_count | int | - | 是 | 0 | 用户添加到单词本的数量 |
| created_at | datetime | - | 是 | CURRENT_TIMESTAMP | 翻译时间 |

**索引**：
- `idx_user_id` (user_id)
- `idx_created_at` (created_at)
- `idx_is_favorite` (user_id, is_favorite)

**说明**：
- grammar_analysis 存储JSON格式的语法分析结果
- word_count 和 new_word_count 用于统计分析

**grammar_analysis JSON结构示例**：
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
      "point": "woke up",
      "explanation": "wake up 的过去式，表示醒来"
    }
  ]
}
```

---

### 2.10 translate_word_item - 翻译单词拆解表

| 字段名 | 类型 | 长度 | 必填 | 默认值 | 说明 |
|--------|------|------|------|--------|------|
| id | bigint | - | 是 | - | 主键，自增 |
| translate_id | bigint | - | 是 | - | 翻译记录ID |
| word_id | bigint | - | 否 | null | 单词ID（如果系统词库中有） |
| word | varchar | 100 | 是 | - | 英文单词/短语 |
| meaning_cn | varchar | 500 | 是 | - | 中文释义 |
| is_phrase | tinyint | - | 是 | 0 | 是否短语（0=单词, 1=短语） |
| sort_order | int | - | 是 | 0 | 在句子中的顺序 |
| added_to_list | tinyint | - | 是 | 0 | 是否已添加到单词本 |

**索引**：
- `idx_translate_id` (translate_id)
- `idx_word_id` (word_id)

**说明**：
- 如果 word_id 不为null，表示该单词在系统词库中存在
- added_to_list 记录用户是否已将该单词添加到单词本，避免重复添加

---

### 2.11 daily_stat - 每日学习统计表

| 字段名 | 类型 | 长度 | 必填 | 默认值 | 说明 |
|--------|------|------|------|--------|------|
| id | bigint | - | 是 | - | 主键，自增 |
| user_id | bigint | - | 是 | - | 用户ID |
| stat_date | date | - | 是 | - | 统计日期 |
| word_learned | int | - | 是 | 0 | 今日从词书学习的单词数（正式学习） |
| word_reviewed | int | - | 是 | 0 | 今日复习单词数 |
| word_mastered | int | - | 是 | 0 | 今日掌握单词数 |
| translate_count | int | - | 是 | 0 | 今日翻译句子数 |
| sentence_word_count | int | - | 是 | 0 | 今日翻译句子中出现的单词数（去重） |
| translate_word_added | int | - | 是 | 0 | 今日从翻译中添加到单词本的单词数（陌生单词） |
| study_duration | int | - | 是 | 0 | 今日学习时长（秒） |
| is_goal_reached | tinyint | - | 是 | 0 | 是否完成每日目标 |
| created_at | datetime | - | 是 | CURRENT_TIMESTAMP | 创建时间 |
| updated_at | datetime | - | 是 | CURRENT_TIMESTAMP | 更新时间 |

**索引**：
- `idx_user_id` (user_id)
- `idx_stat_date` (stat_date)
- `uk_user_date` UNIQUE (user_id, stat_date)

**统计维度说明**：

| 统计项 | 字段 | 含义 | 示例 |
|--------|------|------|------|
| 正式学习 | word_learned | 从词书学习的单词数 | 10个 |
| 额外接触 | sentence_word_count | 翻译句子中出现的单词数（去重） | 5个 |
| 陌生单词 | translate_word_added | 用户主动添加到单词本的单词数 | 1个 |

**额外接触单词去重逻辑**：
- 同一个单词在不同句子中只计算一次
- 统计维度：当天翻译的所有句子中出现的单词，按 word_id 去重
- 例如：今天句子有ABCDE，明天句子有ACDFG，则今天额外接触5个，明天额外接触2个（FG）

---

### 2.12 learning_streak - 连续学习记录表

| 字段名 | 类型 | 长度 | 必填 | 默认值 | 说明 |
|--------|------|------|------|--------|------|
| id | bigint | - | 是 | - | 主键，自增 |
| user_id | bigint | - | 是 | - | 用户ID |
| current_streak | int | - | 是 | 0 | 当前连续天数 |
| longest_streak | int | - | 是 | 0 | 最长连续天数 |
| last_study_date | date | - | 否 | null | 最后学习日期 |
| total_days | int | - | 是 | 0 | 总学习天数 |
| created_at | datetime | - | 是 | CURRENT_TIMESTAMP | 创建时间 |
| updated_at | datetime | - | 是 | CURRENT_TIMESTAMP | 更新时间 |

**索引**：
- `idx_user_id` UNIQUE (user_id)

**说明**：
- 每次用户学习时，检查 last_study_date
- 如果是今天，不变
- 如果是昨天，current_streak + 1
- 如果更早，current_streak 重置为 1
- longest_streak 取历史最大值

---

### 2.13 feedback - 用户反馈表

| 字段名 | 类型 | 长度 | 必填 | 默认值 | 说明 |
|--------|------|------|------|--------|------|
| id | bigint | - | 是 | - | 主键，自增 |
| user_id | bigint | - | 是 | - | 用户ID |
| type | varchar | 20 | 是 | - | 反馈类型 |
| target_id | bigint | - | 否 | null | 关联对象ID |
| content | text | - | 否 | null | 反馈内容 |
| rating | tinyint | - | 否 | null | 评分（1-5） |
| created_at | datetime | - | 是 | CURRENT_TIMESTAMP | 创建时间 |

**索引**：
- `idx_user_id` (user_id)
- `idx_type` (type)
- `idx_target_id` (target_id)

**说明**：
- type:
  - `memory_tip` = 对AI速记的反馈
  - `translation` = 对翻译的反馈
  - `bug` = Bug反馈
  - `suggestion` = 建议
- target_id: 当 type=memory_tip 时，关联 word_memory_tip.id

---

## 三、关键业务SQL示例

### 3.1 获取用户当前词书的下一个待学习单词

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

### 3.2 获取用户今日待复习的单词

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

### 3.3 获取用户的翻译历史（带单词拆解）

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

### 3.4 获取用户今日学习统计

```sql
SELECT * FROM daily_stat 
WHERE user_id = ? AND stat_date = CURDATE();
```

### 3.5 更新用户连续学习天数

```sql
UPDATE learning_streak 
SET 
  current_streak = CASE 
    WHEN last_study_date = CURDATE() THEN current_streak
    WHEN last_study_date = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN current_streak + 1
    ELSE 1
  END,
  longest_streak = GREATEST(
    longest_streak,
    CASE 
      WHEN last_study_date = CURDATE() THEN current_streak
      WHEN last_study_date = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN current_streak + 1
      ELSE 1
    END
  ),
  last_study_date = CURDATE(),
  total_days = IF(last_study_date = CURDATE(), total_days, total_days + 1),
  updated_at = NOW()
WHERE user_id = ?;
```

### 3.6 更新每日学习统计（含三维度单词统计）

```sql
INSERT INTO daily_stat (user_id, stat_date, word_learned, translate_count, sentence_word_count, translate_word_added)
VALUES (?, CURDATE(), ?, ?, ?, ?)
ON DUPLICATE KEY UPDATE
  word_learned = word_learned + VALUES(word_learned),
  translate_count = translate_count + VALUES(translate_count),
  sentence_word_count = sentence_word_count + VALUES(sentence_word_count),
  translate_word_added = translate_word_added + VALUES(translate_word_added),
  updated_at = NOW();
```

### 3.7 计算当天翻译句子中出现的单词数（去重）

```sql
SELECT COUNT(DISTINCT twi.word_id) as sentence_word_count
FROM translate_history th
JOIN translate_word_item twi ON th.id = twi.translate_id
WHERE th.user_id = ?
  AND DATE(th.created_at) = CURDATE()
  AND twi.word_id IS NOT NULL;
```

### 3.8 获取用户某段时间内的学习统计（支持日/周/月）

```sql
-- 按天统计
SELECT stat_date, 
       word_learned as 正式学习, 
       sentence_word_count as 额外接触, 
       translate_word_added as 陌生单词,
       translate_count as 翻译句子数
FROM daily_stat
WHERE user_id = ? AND stat_date BETWEEN ? AND ?
ORDER BY stat_date;

-- 按周统计
SELECT YEAR(stat_date) as year, 
       WEEK(stat_date) as week,
       SUM(word_learned) as 正式学习, 
       SUM(sentence_word_count) as 额外接触, 
       SUM(translate_word_added) as 陌生单词,
       SUM(translate_count) as 翻译句子数
FROM daily_stat
WHERE user_id = ? AND stat_date BETWEEN ? AND ?
GROUP BY YEAR(stat_date), WEEK(stat_date);

-- 按月统计
SELECT DATE_FORMAT(stat_date, '%Y-%m') as month,
       SUM(word_learned) as 正式学习, 
       SUM(sentence_word_count) as 额外接触, 
       SUM(translate_word_added) as 陌生单词,
       SUM(translate_count) as 翻译句子数
FROM daily_stat
WHERE user_id = ? AND stat_date BETWEEN ? AND ?
GROUP BY DATE_FORMAT(stat_date, '%Y-%m');
```

---

## 四、数据字典

### 4.1 枚举值定义

**用户英语等级 (user.level)**：
| 值 | 说明 |
|----|------|
| 1 | 零基础 |
| 2 | 初级 |
| 3 | 中级 |
| 4 | 高级 |
| 5 | 精通 |

**会员等级 (user.vip_level)**：
| 值 | 说明 |
|----|------|
| 0 | 免费用户 |
| 1 | 月度会员 |
| 2 | 年度会员 |
| 3 | 终身会员 |

**单词掌握状态 (user_word_list.status)**：
| 值 | 说明 |
|----|------|
| 0 | 未掌握 |
| 1 | 已掌握 |

**词书学习状态 (user_word_book.status)**：
| 值 | 说明 |
|----|------|
| 0 | 未开始 |
| 1 | 学习中 |
| 2 | 已完成 |

**速记类型 (word_memory_tip.tip_type)**：
| 值 | 说明 |
|----|------|
| phonetic | 谐音法 |
| split | 拆词法 |
| association | 联想法 |
| story | 故事法 |
| root | 词根词缀法 |

**翻译来源 (user_word_list.source)**：
| 值 | 说明 |
|----|------|
| book | 词书学习 |
| translate | 口语翻译 |

---

## 五、数据库选型建议

### 5.1 主数据库
- **推荐**：MySQL 8.0 或 PostgreSQL 14
- **理由**：成熟稳定，社区活跃，适合中小型应用

### 5.2 缓存
- **推荐**：Redis
- **用途**：
  - 用户会话缓存
  - 热门单词缓存
  - 学习统计数据缓存
  - AI速记内容缓存

### 5.3 文件存储
- **推荐**：阿里云OSS / 腾讯云COS
- **用途**：
  - 用户头像
  - 词书封面
  - 单词发音音频

---

## 六、数据量预估

### 6.1 基础数据量
| 表 | 预估数据量 | 说明 |
|----|-----------|------|
| word | 10,000-50,000 | 常用英语单词 |
| word_book | 10-20 | 预置词书数量 |
| word_book_item | 500,000-1,000,000 | 单词-词书关联 |
| word_memory_tip | 50,000-200,000 | AI生成的速记内容 |

### 6.2 用户数据增长（按1万活跃用户估算）
| 表 | 日增长 | 月增长 | 说明 |
|----|--------|--------|------|
| user_word_list | 20,000 | 600,000 | 每人每天添加20个单词 |
| translate_history | 10,000 | 300,000 | 每人每天翻译1次 |
| daily_stat | 10,000 | 300,000 | 每人每天1条统计 |

---

**文档版本**：v3.0  
**创建日期**：2026年5月14日  
**文档状态**：初稿完成
