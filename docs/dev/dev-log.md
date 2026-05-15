# 开发日志

> 统一记录三端（后端/APP端/网页管理后台）的开发进度和已完成任务。

---

## 后端开发

### 环境搭建 ✅
- FastAPI 项目结构搭建（`app/core/`, `app/api/`, `app/models/`, `app/services/`, `app/utils/`）
- 配置管理（pydantic-settings + .env）
- 数据库连接（SQLAlchemy 2.0 async + aiomysql）
- CORS 中间件配置
- Swagger 文档：`http://localhost:8000/docs`
- 健康检查：`GET /api/health`

### 数据库搭建 ✅
- MySQL 8.0 数据库创建（`ilove_english`，utf8mb4）
- Alembic 异步迁移配置
- 模型创建：`user`, `user_setting`, `word_book`, `user_word_book`, `word`, `word_book_item`, `user_word_list`
- 模型待创建：`word_memory_tip`, `translate_history`, `translate_word_item`, `daily_stat`, `learning_streak`, `feedback`
- 词书种子数据预置

### 用户认证 ✅
- Pydantic Schema：`UserRegister`, `UserLogin`, `UserResponse`, `TokenResponse`, `ApiResponse`
- 密码工具：SHA256 预哈希 + bcrypt
- JWT Token 生成/验证（python-jose）
- API 路由：
  - `POST /api/auth/register` — 注册
  - `POST /api/auth/login` — 登录
  - `GET /api/auth/me` — 获取当前用户

### 词书管理 ✅
- Pydantic Schema：`WordBookResponse`, `SelectWordBookRequest`, `UpdateProgressRequest`
- Service 层：词书列表/详情/选择/进度更新
- API 路由：
  - `GET /api/word-books` — 词书列表（支持分类筛选）
  - `GET /api/word-books/{book_id}` — 词书详情（含用户进度）
  - `POST /api/word-books/select` — 选择词书
  - `GET /api/word-books/user/current` — 当前词书
  - `GET /api/word-books/user/list` — 用户词书列表
  - `PUT /api/word-books/user/progress` — 更新进度

### 单词管理 ✅
- 模型：`word`, `word_book_item`, `user_word_list`
- Pydantic Schema：`WordResponse`, `WordDetailResponse`, `WordListData`, `AddToWordListRequest` 等
- Service 层：词书单词列表、下一个待学、单词详情、单词本 CRUD、艾宾浩斯复习
- API 路由（8 个端点）：
  - `GET /api/words/book/{book_id}` — 词书单词列表（分页）
  - `GET /api/words/next` — 下一个待学习单词
  - `GET /api/words/{word_id}` — 单词详情（含助记信息）
  - `POST /api/words/word-list` — 添加到单词本
  - `DELETE /api/words/word-list/{word_id}` — 从单词本移除
  - `PUT /api/words/word-list/{word_id}/status` — 更新掌握状态
  - `GET /api/words/word-list` — 获取用户单词本（分页+筛选）
  - `GET /api/words/review` — 获取待复习单词

### AI速记 🔲 待开发
- 模型待创建：`word_memory_tip`
- AI服务对接规划中

### 翻译 🔲 待开发
- 表结构已设计：`translate_history`, `translate_word_item`
- API 待实现

### 统计 🔲 待开发
- 表结构已设计：`daily_stat`, `learning_streak`
- API 待实现

---

## APP端开发

### 环境搭建 ✅
- uni-app + Vue3 + TypeScript + Vite + Pinia 项目结构
- 底部 TabBar 配置（首页/单词/口语/我的）
- API 请求封装（`uni.request` + 拦截器）
- 用户状态管理（`stores/user.ts`）

### 页面开发

| 页面 | 状态 | 说明 |
|------|------|------|
| 首页 | 🔶 | 基础布局完成，数据对接中 |
| 单词列表 | 🔶 | 词书选择 + 单词卡片 |
| 单词详情 | 🔶 | 单词信息 + AI速记展示 |
| 单词本 | 🔲 | 待开发 |
| 口语输入 | 🔲 | 待开发 |
| 口语结果 | 🔲 | 待开发 |
| 我的 | 🔶 | 基础布局完成 |

---

## 网页管理后台开发

### 环境搭建 ✅
- Vue3 + TypeScript + Vite + Element Plus + Pinia + Vue Router
- Axios 请求封装（拦截器：Token + 401处理）
- 布局组件（顶部导航 + 左侧菜单）
- 路由守卫（未登录跳转登录页）

### 功能开发

| 功能 | 状态 | 说明 |
|------|------|------|
| 登录/注册 | ✅ | 对接后端 API |
| 词书管理 | 🔶 | 列表/详情页完成，新增/编辑待实现 |
| 单词管理 | ✅ | 按词书筛选列表 + 分页，对接后端 API |
| AI速记管理 | 🔲 | 待开发 |
| 用户管理 | 🔲 | 待开发 |
| 样式优化 | ✅ | 修复页面留白 + 按钮间距问题 |

---

## 迁移文件记录

| 迁移文件 | 说明 |
|---------|------|
| `56a75e93f4b3` | 创建 user + user_setting 表 |
| `a1b2c3d4e5f6` | 创建 word_book + user_word_book 表 |
| `b2c3d4e5f6a7` | 预置词书种子数据 |
| `c3d4e5f6a7b8` | 创建 word + word_book_item + user_word_list 表 |
