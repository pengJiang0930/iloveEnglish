# Dev01 - 后端环境搭建

## 目标

搭建 FastAPI 后端开发环境，创建基础项目结构。

## 任务清单

### 1.1 创建项目结构

- [ ] 创建 `server` 目录
- [ ] 创建 Python 虚拟环境
- [ ] 创建 `requirements.txt` 文件

### 1.2 安装依赖

依赖列表：
- **Web框架**: fastapi, uvicorn
- **数据库**: sqlalchemy, aiomysql, alembic
- **缓存**: redis, aioredis
- **数据校验**: pydantic, pydantic-settings
- **认证**: python-jose, passlib, python-multipart
- **工具**: python-dotenv, loguru, httpx

### 1.3 创建核心模块

- [ ] `app/core/config.py` - 配置管理（pydantic-settings）
- [ ] `app/core/database.py` - 数据库连接（SQLAlchemy 异步引擎）
- [ ] `.env.example` - 环境变量模板

### 1.4 创建主入口

- [ ] `main.py` - FastAPI 应用入口
- [ ] 配置 CORS 中间件
- [ ] 注册路由

## 验证标准

- [ ] 后端服务启动无报错
- [ ] Swagger 文档可访问: http://localhost:8000/docs
- [ ] 健康检查接口返回 200: http://localhost:8000/api/health
