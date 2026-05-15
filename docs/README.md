# iLoveEnglish 文档索引

> 所有系统规则和设计文档的统一入口。开发前必须优先阅读。

---

## 文档结构

```
docs/
│
├── README.md                    # 总索引 + 新人入门指南 + 快速导航
│
├── product/                     # 📋 产品文档 — 描述"做什么"
│   ├── overview.md              #   产品全貌：定位、两大功能、差异化、MVP计划
│   ├── user-module.md           #   用户模块：注册/登录、资料、设置、业务规则
│   ├── word-module.md           #   单词模块：词书、单词学习、AI速记、单词本、复习
│   └── speaking-module.md       #   口语模块：中文→英文翻译、句子拆解、语法讲解
│
├── architecture/                # 🏗️ 架构文档 — 描述"怎么做"
│   ├── system-architecture.md   #   系统架构图、三端技术栈、模块划分、接口规范
│   ├── database-design.md       #   13张表清单、ER图、枚举定义、索引策略、数据预估
│   └── ui-design.md             #   色彩/字体/间距/圆角/阴影/组件规范、页面布局
│
├── api/                         # 🔌 接口契约 — 前后端的"合同"
│   ├── auth-api.md              #   注册/登录/获取用户信息（3个接口，含DTO定义）
│   ├── word-book-api.md         #   词书列表/详情/选择/进度（6个接口）
│   ├── word-api.md              #   单词学习/单词本/复习（8个接口）
│   ├── memory-tip-api.md        #   AI速记生成/查询/点赞（4个接口）
│   └── translate-api.md         #   翻译接口（规划中，4个接口）
│
├── ai/                          # 🤖 AI规则 — Prompt和Agent行为
│   ├── prompts/
│   │   └── memory-tip-prompt.md #   5种速记Prompt + 翻译Prompt模板
│   └── changelog.md             #   Prompt修改记录（追溯每次调整）
│
└── dev/                         # 📝 开发日志 — 追踪进度
    ├── dev-log.md               #   后端/APP/Web三端已完成和待开发任务清单
    └── style-changelog.md       #   CSS样式修复记录（问题→原因→改动）
```

> **快速记忆**：想了解"做什么"看 product/，想了解"怎么做"看 architecture/，前后端对接看 api/，AI行为看 ai/，当前进度看 dev/。

---

## 快速导航

### 新人入门
1. [产品概述](product/overview.md) — 了解项目是什么
2. [系统架构](architecture/system-architecture.md) — 了解技术栈和模块划分
3. [开发日志](dev/dev-log.md) — 了解当前开发进度

### 后端开发
1. [数据库设计](architecture/database-design.md) — 表结构参考
2. [API文档](api/) — 接口规范

### 前端开发
1. [UI设计规范](architecture/ui-design.md) — 设计约束
2. [API文档](api/) — 前后端接口契约

### AI/产品
1. [产品模块文档](product/) — 业务逻辑
2. [AI Prompt](ai/prompts/memory-tip-prompt.md) — Prompt 模板

---

## 开发规范

所有开发行为严格遵循 `AI Development Rules & Engineering Standards.md`，核心原则：

1. **文档优先** — 开发前必须阅读 docs/
2. **一个模块一个文档** — 长期维护，版本由 Git 管理
3. **禁止版本化命名** — 不使用 v1/v2/final 等后缀
4. **代码与文档同步** — 接口变更必须同步更新 API 文档
5. **Prompt 属于系统规则** — 必须存放于 docs/ai/prompts/
