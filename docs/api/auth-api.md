# 用户认证 API

---

## 接口概览

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| POST | `/api/auth/register` | 否 | 用户注册 |
| POST | `/api/auth/login` | 否 | 用户登录 |
| GET | `/api/auth/me` | 是 | 获取当前用户信息 |

---

## 通用返回结构

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

---

## 1. 用户注册

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

**字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| phone | string | 是 | 手机号（11-20位） |
| password | string | 是 | 密码（6-50位） |
| nickname | string | 否 | 昵称，默认空字符串 |

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
      "avatar": null,
      "level": 1,
      "daily_goal": 20,
      "vip_level": 0,
      "created_at": "2026-05-14T10:00:00"
    }
  }
}
```

**错误码**：

| 状态码 | 说明 |
|--------|------|
| 400 | 手机号已注册 / 参数校验失败 |
| 500 | 服务器内部错误 |

---

## 2. 用户登录

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

**字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| phone | string | 是 | 手机号 |
| password | string | 是 | 密码 |

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
      "avatar": null,
      "level": 1,
      "daily_goal": 20,
      "vip_level": 0,
      "created_at": "2026-05-14T10:00:00"
    }
  }
}
```

**错误码**：

| 状态码 | 说明 |
|--------|------|
| 400 | 密码错误 / 用户不存在 |
| 500 | 服务器内部错误 |

---

## 3. 获取当前用户信息

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

**错误码**：

| 状态码 | 说明 |
|--------|------|
| 401 | Token无效或过期 |

---

## 认证原理

- JWT Token 使用 python-jose 生成，包含 `sub`（用户UID）和 `exp`（过期时间）
- 密码使用 SHA256 预哈希后再 bcrypt 处理
- Token 通过 `Authorization: Bearer <token>` 请求头传递
- Token 过期时间由 `ACCESS_TOKEN_EXPIRE_MINUTES` 配置
