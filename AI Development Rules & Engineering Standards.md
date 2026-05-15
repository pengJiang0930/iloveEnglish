# AI Development Rules & Engineering Standards

> 本文档用于约束 AI 在本项目中的开发行为。
>
> 所有 AI（ChatGPT、Claude、Cursor、Copilot 等）在参与开发前，
> 必须优先阅读本规范，并严格遵守。

---

# 1. 项目目标

本项目目标：

- 保持长期可维护性
- 保持架构一致性
- 避免 AI 随意生成代码
- 保持前后端接口统一
- 保持文档与代码同步
- 保持模块职责清晰
- 所有改动必须可追踪

AI 必须以“工程化开发”而不是“代码生成”方式参与项目。

---

# 2. 开发核心原则

## 2.1 优先阅读文档

开发前必须优先阅读：

```text
/docs
```

重点：

```text
docs/product/
docs/architecture/
docs/api/
docs/ai/
```

禁止脱离文档直接生成业务代码。

------

## 2.2 禁止擅自修改架构

AI 不允许：

- 擅自新增技术栈
- 擅自修改模块边界
- 擅自更换框架
- 擅自修改数据库核心结构
- 擅自改变接口协议
- 擅自新增中间件

如果必须修改：

必须先更新：

```text
docs/architecture/
```

并说明原因。

------

## 2.3 优先复用已有代码

新增功能前必须：

- 搜索现有实现
- 复用已有 Service
- 复用已有 DTO
- 复用已有工具类
- 保持代码风格一致

禁止重复造轮子。

------

## 2.4 禁止生成“演示型代码”

禁止：

- TODO 代码
- mock 代码
- fake 实现
- 临时逻辑
- demo 风格代码

所有生成代码必须：

- 可运行
- 可维护
- 可扩展
- 可上线

------

# 3. 文档规范

------

## 3.1 文档即系统事实来源

系统规则必须写入 docs。

包括：

- 业务规则
- API协议
- Prompt规则
- 数据结构
- Redis Key
- 权限规则
- Agent行为
- Workflow流程

禁止：

“代码改了但文档不更新”。

------

## 3.2 文档禁止版本化命名

禁止：

```text
user-v2.md
user-final.md
user-new.md
```

统一使用：

```text
user-module.md
```

版本通过 Git 管理。

------

## 3.3 一个模块一个长期文档

例如：

```text
docs/product/user-module.md
docs/api/user-api.md
docs/architecture/auth-design.md
```

持续维护。

------

## 3.4 文档中允许写关键代码

允许：

- API 示例
- DTO结构
- SQL结构
- Prompt
- Redis Key
- 接口 Contract
- 架构伪代码

禁止：

- 完整 Controller
- 完整 ServiceImpl
- 大段 CRUD 代码

------

# 4. 代码规范

------

## 4.1 保持模块职责单一

禁止：

- Controller 写业务逻辑
- Service 操作 HTTP
- Mapper 写业务判断
- Utils 包含业务逻辑

------

## 4.2 命名规范

必须：

- 变量名语义化
- 方法名表达行为
- 类名表达职责

禁止：

```java
doData()
handle()
test()
temp()
aaa()
```

------

## 4.3 方法长度限制

原则：

- 一个方法只做一件事
- 超过 80 行需考虑拆分
- 超过 3 层 if 应考虑重构

------

## 4.4 禁止硬编码

禁止：

- 硬编码 URL
- 硬编码 Token
- 硬编码 Redis Key
- 硬编码 Prompt
- 硬编码 SQL 条件

必须统一管理。

------

## 4.5 日志规范

必须：

- 关键流程记录日志
- 异常必须记录
- 日志包含上下文信息

禁止：

```java
log.info("error");
```

必须：

```java
log.error("用户登录失败, uid={}, reason={}", uid, reason);
```

------

# 5. API 规范

------

## 5.1 接口必须文档化

所有接口必须同步更新：

```text
docs/api/
```

必须包含：

- 请求参数
- 返回结构
- 错误码
- 示例

------

## 5.2 接口保持统一结构

统一返回：

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

禁止接口结构混乱。

------

## 5.3 禁止破坏兼容性

如果修改：

- 字段名称
- 字段类型
- 接口结构

必须：

- 增加版本号
- 更新 release note

------

# 6. 数据库规范

------

## 6.1 禁止直接修改数据库

必须通过：

- Flyway
- Liquibase
- migration SQL

管理数据库变更。

------

## 6.2 所有表必须有基础字段

建议：

```sql
id
created_at
updated_at
created_by
updated_by
deleted
```

------

## 6.3 禁止随意新增字段

新增字段前必须考虑：

- 是否冗余
- 是否可扩展
- 是否影响索引
- 是否影响历史数据

------

# 7. AI / Prompt 规范

------

## 7.1 Prompt 属于系统规则

Prompt 必须存放：

```text
docs/ai/prompts/
```

禁止：

Prompt 散落在代码中。

------

## 7.2 Prompt 修改必须记录

修改 Prompt 后：

必须更新：

```text
docs/ai/changelog.md
```

------

## 7.3 Agent 必须有行为定义

每个 Agent 必须说明：

- Role
- Goal
- Constraints
- Tool权限
- Memory策略
- Output格式

------

# 8. Git 规范

------

## 8.1 Commit 必须规范

格式：

```text
feat(user): 增加手机号登录
fix(chat): 修复SSE断流
refactor(auth): 重构JWT逻辑
docs(api): 更新登录接口文档
```

------

## 8.2 禁止直接提交垃圾代码

禁止：

- debug代码
- println
- 注释掉的大段代码
- 无意义 commit

------

# 9. 开发流程规范

标准流程：

```text
1. 更新 PRD
2. 更新技术设计
3. AI 阅读 docs
4. AI 生成代码
5. 更新 API 文档
6. 更新 DevLog
7. Git Commit
```

禁止：

```text
直接让 AI 写代码
→ 直接上线
```

------

# 10. AI 行为约束

AI 必须：

- 优先遵循 docs
- 优先遵循现有架构
- 优先遵循已有代码风格
- 优先复用已有实现

AI 禁止：

- 自作主张重构
- 擅自修改接口
- 擅自修改数据库
- 擅自改变业务逻辑
- 擅自引入新依赖

------

# 11. 输出规范

AI 输出代码时必须：

- 包含必要注释
- 保持可读性
- 保持模块边界
- 不生成废弃代码
- 不生成重复代码

------

# 12. 最终原则

AI 是：

# 工程协作者

不是：

# 随机代码生成器

所有开发行为必须：

- 可维护
- 可追踪
- 可复现
- 可扩展
- 可迭代

项目长期稳定性优先级：

高于：

短期开发速度。

```

```