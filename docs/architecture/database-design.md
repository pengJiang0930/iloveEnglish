# 数据库设计

---

## 一、数据库概览

### 1.1 表清单（13张表）

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

### 1.2 ER关系图

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

## 二、基础字段规范

所有表建议包含：

| 字段 | 类型 | 说明 |
|------|------|------|
| id | bigint | 主键，自增 |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

用户相关表额外包含：
| 字段 | 类型 | 说明 |
|------|------|------|
| created_by | bigint | 创建者 |
| updated_by | bigint | 更新者 |
| deleted_at | datetime | 软删除时间 |

---

## 三、枚举值定义

### 用户英语等级 (user.level)

| 值 | 说明 |
|----|------|
| 1 | 零基础 |
| 2 | 初级 |
| 3 | 中级 |
| 4 | 高级 |
| 5 | 精通 |

### 会员等级 (user.vip_level)

| 值 | 说明 |
|----|------|
| 0 | 免费用户 |
| 1 | 月度会员 |
| 2 | 年度会员 |
| 3 | 终身会员 |

### 单词掌握状态 (user_word_list.status)

| 值 | 说明 |
|----|------|
| 0 | 未掌握 |
| 1 | 已掌握 |

### 词书学习状态 (user_word_book.status)

| 值 | 说明 |
|----|------|
| 0 | 未开始 |
| 1 | 学习中 |
| 2 | 已完成 |

### 速记类型 (word_memory_tip.tip_type)

| 值 | 说明 |
|----|------|
| phonetic | 谐音法 |
| split | 拆词法 |
| association | 联想法 |
| story | 故事法 |
| root | 词根词缀法 |

### 翻译来源 (user_word_list.source)

| 值 | 说明 |
|----|------|
| book | 词书学习 |
| translate | 口语翻译 |

---

## 四、索引策略

| 表 | 索引 | 类型 |
|----|------|------|
| user | uid | UNIQUE |
| user | phone | INDEX |
| user_setting | user_id | UNIQUE |
| word_book | category, status | INDEX |
| word | word | UNIQUE |
| word | frequency, level | INDEX |
| word_book_item | (book_id, word_id) | UNIQUE |
| user_word_book | (user_id, book_id) | UNIQUE |
| user_word_list | (user_id, word_id) | UNIQUE |
| user_word_list | (user_id, next_review_at) | INDEX |
| word_memory_tip | word_id, tip_type | INDEX |
| translate_history | user_id, created_at | INDEX |
| learning_streak | user_id | UNIQUE |
| daily_stat | (user_id, stat_date) | UNIQUE |

---

## 五、数据量预估

### 基础数据量

| 表 | 预估数据量 | 说明 |
|----|-----------|------|
| word | 10,000-50,000 | 常用英语单词 |
| word_book | 10-20 | 预置词书数量 |
| word_book_item | 500,000-1,000,000 | 单词-词书关联 |
| word_memory_tip | 50,000-200,000 | AI生成的速记内容 |

### 用户数据增长（按1万活跃用户估算）

| 表 | 日增长 | 月增长 |
|----|--------|--------|
| user_word_list | 20,000 | 600,000 |
| translate_history | 10,000 | 300,000 |
| daily_stat | 10,000 | 300,000 |

---

## 六、数据库选型

| 组件 | 选型 | 用途 |
|------|------|------|
| 主数据库 | MySQL 8.0 | 业务数据存储 |
| 缓存 | Redis 7.0 | 会话/热点数据缓存 |
| 文件存储 | 阿里云OSS/腾讯云COS | 图片/音频文件 |
| 迁移工具 | Alembic | 数据库版本管理 |

**Alembic 迁移文件位置**：`server/alembic/versions/`

已有迁移：
- `56a75e93f4b3_create_user_and_user_setting_tables.py`
- `a1b2c3d4e5f6_create_word_book_and_user_word_book_tables.py`
- `b2c3d4e5f6a7_seed_word_book_data.py`
