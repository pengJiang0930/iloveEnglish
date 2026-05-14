# Dev v1 - 三端开发环境搭建与Demo

> 目标：搭建基础开发环境，跑通三端Demo，验证技术栈可行性

---

## 一、开发环境准备

### 1.1 本机环境要求

| 工具 | 版本 | 用途 |
|------|------|------|
| Node.js | 18.x+ | 前端开发 |
| Python | 3.10+ | 后端开发 |
| MySQL | 8.0+ | 数据库 |
| Redis | 7.0+ | 缓存 |
| Git | 最新版 | 版本控制 |
| VS Code | 最新版 | 代码编辑器 |
| HBuilderX | 最新版 | uni-app开发 |

### 1.2 VS Code 插件推荐

**通用插件**：
- Chinese (Simplified) Language Pack
- GitLens
- Error Lens

**Python 插件**：
- Python
- Pylance
- Python Debugger
- Black Formatter

**前端插件**：
- Vue - Official
- ESLint
- Prettier

---

## 二、项目目录结构

```
iloveEnglish/
├── Doc/                    # 文档目录
│   ├── PRD/                # 产品需求文档
│   ├── DEV/                # 开发文档
│   └── prototype/          # UI原型
│
├── server/                 # 后端项目（FastAPI）
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic模型
│   │   ├── services/       # 业务逻辑
│   │   └── utils/          # 工具函数
│   ├── alembic/            # 数据库迁移
│   ├── tests/              # 测试
│   ├── requirements.txt    # 依赖
│   └── main.py             # 入口
│
├── web/                    # 网页端项目（Vue3）
│   ├── src/
│   │   ├── api/            # API请求
│   │   ├── components/     # 组件
│   │   ├── router/         # 路由
│   │   ├── stores/         # 状态管理
│   │   ├── views/          # 页面
│   │   └── App.vue
│   └── package.json
│
└── app/                    # APP端项目（uni-app）
    ├── pages/              # 页面
    ├── components/         # 组件
    ├── stores/             # 状态管理
    ├── api/                # API请求
    ├── static/             # 静态资源
    └── pages.json          # 页面配置
```

---

## 三、后端环境搭建（FastAPI）

### 3.1 创建项目

1. 创建 `server` 目录
2. 创建 Python 虚拟环境：`python -m venv venv`
3. 激活虚拟环境：
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

### 3.2 安装依赖

创建 `requirements.txt`，包含以下依赖：
- **Web框架**：fastapi, uvicorn
- **数据库**：sqlalchemy, aiomysql, alembic
- **缓存**：redis, aioredis
- **数据校验**：pydantic, pydantic-settings
- **认证**：python-jose, passlib, python-multipart
- **工具**：python-dotenv, loguru, httpx

运行 `pip install -r requirements.txt` 安装

### 3.3 创建项目结构

按以下结构创建目录和文件：
- `app/api/` - API路由模块
- `app/core/` - 核心配置（数据库连接、配置文件）
- `app/models/` - SQLAlchemy数据模型
- `app/schemas/` - Pydantic请求/响应模型
- `app/services/` - 业务逻辑层
- `app/utils/` - 工具函数（认证、加密等）

### 3.4 核心模块说明

**配置模块 (app/core/config.py)**：
- 使用 pydantic-settings 管理配置
- 从 `.env` 文件读取环境变量
- 包含数据库、Redis、JWT等配置

**数据库模块 (app/core/database.py)**：
- 使用 SQLAlchemy 2.0 异步模式
- 创建异步引擎和会话工厂
- 提供 `get_db` 依赖注入

**用户模型 (app/models/user.py)**：
- 定义 users 表结构
- 包含 id, uid, phone, nickname, level 等字段

**认证模块 (app/utils/auth.py)**：
- JWT token 生成和验证
- 用户密码加密
- 当前用户依赖注入

**API路由**：
- `app/api/health.py` - 健康检查接口
- `app/api/auth.py` - 认证接口（登录、注册、获取用户信息）

**主入口 (main.py)**：
- 创建 FastAPI 实例
- 配置 CORS 中间件
- 注册路由
- 启动/关闭事件处理

### 3.5 环境变量

创建 `.env` 文件，配置以下变量：
- MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
- REDIS_HOST, REDIS_PORT, REDIS_DB
- SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

### 3.6 启动后端

```bash
# 确保虚拟环境已激活
python main.py

# 或使用uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**验证**：
- API文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/api/health

---

## 四、网页端环境搭建（Vue3）

### 4.1 创建项目

使用 Vite 创建 Vue3 + TypeScript 项目：
```bash
npm create vite@latest web -- --template vue-ts
cd web
npm install
```

### 4.2 安装额外依赖

- **路由**：vue-router@4
- **状态管理**：pinia
- **HTTP客户端**：axios
- **UI组件库**：element-plus
- **图标**：@element-plus/icons-vue

### 4.3 项目结构

**核心目录**：
- `src/api/` - API请求封装（axios配置、各模块API）
- `src/router/` - 路由配置
- `src/stores/` - Pinia状态管理
- `src/views/` - 页面组件（Home, Login, Word等）
- `src/components/` - 公共组件

### 4.4 核心模块说明

**Vite配置 (vite.config.ts)**：
- 配置路径别名 `@` 指向 `src`
- 配置开发服务器代理，将 `/api` 转发到后端

**路由配置 (src/router/index.ts)**：
- 配置页面路由：首页、登录页、单词页
- 使用懒加载方式引入页面组件

**API封装 (src/api/index.ts)**：
- 创建 axios 实例，配置基础URL和超时时间
- 请求拦截器：自动添加 token
- 响应拦截器：统一处理错误

**状态管理 (src/stores/user.ts)**：
- 管理用户 token 和用户信息
- 提供 login、getUserInfo、logout 方法

**页面组件**：
- `Home.vue` - 首页，显示欢迎信息和快捷入口
- `Login.vue` - 登录页，手机号登录
- `Word.vue` - 单词页，Demo占位

### 4.5 启动网页端

```bash
npm run dev
```

访问 http://localhost:3000

---

## 五、APP端环境搭建（uni-app）

### 5.1 创建项目

**方式一：HBuilderX创建**
1. 打开 HBuilderX
2. 文件 → 新建 → 项目
3. 选择 `uni-app` → `Vue3` 模板
4. 项目名称：`app`

**方式二：命令行创建**
```bash
npx degit dcloudio/uni-preset-vue#vite-ts app
cd app
npm install
```

### 5.2 安装额外依赖

- **状态管理**：pinia

### 5.3 项目结构

**核心目录**：
- `pages/` - 页面目录（index, word, speaking, profile）
- `components/` - 公共组件
- `stores/` - Pinia状态管理
- `api/` - API请求封装
- `static/` - 静态资源（图标等）

### 5.4 核心模块说明

**页面配置 (pages.json)**：
- 定义页面路径和导航栏样式
- 配置底部 TabBar（首页、单词、口语、我的）

**请求封装 (api/index.ts)**：
- 封装 uni.request
- 自动添加 token
- 统一错误处理
- 401 自动跳转登录

**状态管理 (stores/user.ts)**：
- 与网页端类似的用户状态管理
- 使用 uni.setStorageSync 存储 token

**页面组件**：
- `pages/index/index.vue` - 首页，显示学习数据和快捷入口
- `pages/word/index.vue` - 单词页，Demo占位
- `pages/speaking/index.vue` - 口语页，Demo占位
- `pages/profile/index.vue` - 我的页面，Demo占位

### 5.5 运行APP端

**HBuilderX运行**：
1. 运行 → 运行到浏览器 → Chrome
2. 或 运行 → 运行到手机或模拟器

**命令行运行**：
```bash
npm run dev:h5
```

---

## 六、数据库初始化

### 6.1 创建数据库

连接 MySQL，执行：
```sql
CREATE DATABASE IF NOT EXISTS ilove_english 
DEFAULT CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
```

### 6.2 创建用户表

使用 SQL 语句创建 `users` 表，包含以下字段：
- id: 主键，自增
- uid: 用户唯一标识（UUID）
- phone: 手机号，唯一
- nickname: 昵称
- avatar: 头像URL
- level: 英语等级（1-5）
- daily_goal: 每日学习目标
- vip_level: 会员等级
- created_at, updated_at: 时间戳

### 6.3 插入测试数据

插入 1-2 条测试用户数据，用于登录测试。

---

## 七、联调验证

### 7.1 启动顺序

1. 启动 MySQL 和 Redis 服务
2. 启动后端：`cd server && python main.py`
3. 启动网页端：`cd web && npm run dev`
4. 启动APP端：HBuilderX 运行或 `cd app && npm run dev:h5`

### 7.2 验证清单

| 验证项 | 预期结果 | 状态 |
|--------|----------|------|
| 后端健康检查 | http://localhost:8000/api/health 返回 200 | □ |
| Swagger文档 | http://localhost:8000/docs 可访问 | □ |
| 网页端首页 | http://localhost:3000 显示首页 | □ |
| 网页端登录 | 输入手机号可登录成功 | □ |
| APP端首页 | 显示首页布局 | □ |
| APP端Tab切换 | 底部导航可切换页面 | □ |
| API联调 | 前端调用后端API成功 | □ |

---

## 八、常见问题

### 8.1 后端启动失败

**问题**：ModuleNotFoundError
**解决**：确保虚拟环境已激活，运行 `pip install -r requirements.txt`

**问题**：数据库连接失败
**解决**：检查 `.env` 文件中的数据库配置，确保 MySQL 服务已启动

### 8.2 网页端启动失败

**问题**：npm install 报错
**解决**：删除 node_modules 后重新安装，或使用 `npm install --legacy-peer-deps`

**问题**：API请求跨域
**解决**：检查 vite.config.ts 中的 proxy 配置

### 8.3 APP端启动失败

**问题**：uni-app编译报错
**解决**：检查 HBuilderX 版本，确保使用最新版

---

## 九、后续开发计划

完成本阶段后，下一步开发内容：

1. **用户模块完善**：验证码登录、用户设置
2. **单词模块开发**：词书列表、单词详情、AI速记
3. **口语模块开发**：翻译接口、句子拆解、语法讲解
4. **统计模块开发**：每日统计、学习趋势

详见 PRD-v3-coding.md 中的任务清单。

---

**文档版本**：v1.0  
**创建日期**：2026年5月14日  
**文档状态**：初稿完成
