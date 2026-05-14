# Dev03 - 用户认证

## 目标

实现用户注册、登录功能，JWT 鉴权机制。

## 任务清单

### 3.1 创建 Pydantic Schema

- [ ] `app/schemas/user.py` - 请求/响应模型
  - `UserRegister` - 注册请求（手机号、密码、昵称）
  - `UserLogin` - 登录请求（手机号、密码）
  - `UserResponse` - 用户信息响应
  - `TokenResponse` - JWT Token 响应

### 3.2 创建认证工具

- [ ] `app/utils/auth.py`
  - 密码哈希（bcrypt）
  - JWT Token 生成/验证
  - 获取当前用户依赖注入

### 3.3 创建用户服务层

- [ ] `app/services/user_service.py`
  - `register()` - 注册（校验手机号唯一 → 创建用户 → 创建默认设置）
  - `login()` - 登录（校验手机号/密码 → 生成 Token）
  - `get_user_info()` - 获取用户信息

### 3.4 创建 API 路由

- [ ] `app/api/auth.py`
  - `POST /api/auth/register` - 注册
  - `POST /api/auth/login` - 登录
  - `GET /api/auth/me` - 获取当前用户信息（需鉴权）
- [ ] `app/api/health.py`
  - `GET /api/health` - 健康检查

### 3.5 更新 main.py

- [ ] 注册路由
- [ ] 添加启动时数据库连接/关闭事件
- [ ] 配置异常处理中间件

## API 接口定义

### 注册

```
POST /api/auth/register
```

**请求体**：
```json
{
  "phone": "13800138000",
  "password": "123456",
  "nickname": "小明"
}
```

**成功响应**（200）：
```json
{
  "code": 0,
  "message": "注册成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "user": {
      "uid": "a1b2c3d4...",
      "phone": "138****8000",
      "nickname": "小明",
      "level": 1,
      "daily_goal": 20
    }
  }
}
```

### 登录

```
POST /api/auth/login
```

**请求体**：
```json
{
  "phone": "13800138000",
  "password": "123456"
}
```

**成功响应**（200）：
```json
{
  "code": 0,
  "message": "登录成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "user": {
      "uid": "a1b2c3d4...",
      "phone": "138****8000",
      "nickname": "小明",
      "level": 1,
      "daily_goal": 20
    }
  }
}
```

### 获取当前用户

```
GET /api/auth/me
Authorization: Bearer <token>
```

**成功响应**（200）：
```json
{
  "code": 0,
  "data": {
    "uid": "a1b2c3d4...",
    "phone": "138****8000",
    "nickname": "小明",
    "avatar": null,
    "level": 1,
    "daily_goal": 20,
    "vip_level": 0,
    "created_at": "2026-05-14T10:00:00"
  }
}
```

## 验证标准

- [ ] 注册接口正常工作
- [ ] 重复注册返回"手机号已注册"
- [ ] 登录接口正常工作，返回 Token
- [ ] 密码错误返回"密码错误"
- [ ] 获取用户信息接口正常工作（带 Token）
- [ ] Token 过期/无效返回 401
- [ ] user_setting 自动创建
