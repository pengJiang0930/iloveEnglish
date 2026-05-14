# I Love English - 后端服务

## 技术栈

- **框架**: FastAPI (Python 3.10+)
- **数据库**: MySQL 8.0+ (SQLAlchemy 2.0 异步模式)
- **缓存**: Redis 7.0+
- **认证**: JWT (python-jose)
- **迁移**: Alembic
- **日志**: Loguru

## 项目结构

```
server/
├── app/
│   ├── api/            # API路由
│   ├── core/           # 核心配置
│   ├── models/         # 数据模型
│   ├── schemas/        # Pydantic模型
│   ├── services/       # 业务逻辑
│   └── utils/          # 工具函数
├── alembic/            # 数据库迁移
├── tests/              # 测试
├── requirements.txt    # 依赖
└── main.py             # 入口
```

## 快速开始

### 1. 环境准备

- Python 3.10+
- MySQL 8.0+
- Redis 7.0+

### 2. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env`，并填写配置：

```bash
cp .env.example .env
```

### 4. 数据库初始化

```bash
# 执行数据库迁移
alembic upgrade head
```

### 5. 启动服务

```bash
# 方式一：直接运行
python main.py

# 方式二：使用uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. 验证

- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/api/health

## 开发文档

详细的开发任务文档请查看 [devDoc](./devDoc/) 目录。
