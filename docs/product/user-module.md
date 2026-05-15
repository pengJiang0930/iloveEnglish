# 用户模块

---

## 一、功能概述

提供用户的注册、登录、个人信息管理、学习设置等功能。

---

## 二、用户注册与登录

### 2.1 注册
- 手机号注册（必填：手机号、密码；可选：昵称）
- 注册成功后自动创建 `user_setting` 记录
- 昵称默认为空字符串

### 2.2 登录
- 手机号 + 密码登录
- 登录成功后返回 JWT Token，有效期可配置
- 更新 `last_login_at` 时间

### 2.3 认证机制
- JWT Token（python-jose），Bearer 方式传递
- 密码使用 bcrypt 哈希存储（SHA256 预哈希）
- Token 过期后返回 401

---

## 三、个人资料管理

| 字段 | 说明 |
|------|------|
| uid | 用户唯一标识（UUID） |
| phone | 手机号 |
| nickname | 昵称 |
| avatar | 头像URL |
| level | 英语等级（1-5） |
| daily_goal | 每日学习目标（单词数，默认20） |
| vip_level | 会员等级（0=免费，1=月度，2=年度，3=终身） |
| vip_expire_at | 会员过期时间 |
| last_login_at | 最后登录时间 |

### 英语等级枚举

| 值 | 说明 |
|----|------|
| 1 | 零基础 |
| 2 | 初级 |
| 3 | 中级 |
| 4 | 高级 |
| 5 | 精通 |

---

## 四、用户设置

| 字段 | 说明 | 默认值 |
|------|------|--------|
| daily_reminder | 每日提醒开关 | 1（开） |
| reminder_time | 提醒时间 | 20:00 |
| pronunciation | 发音偏好（us=美音, uk=英音） | us |
| theme | 主题（light/dark） | light |
| font_size | 字体大小 | medium |

---

## 五、数据表结构

### user

```sql
CREATE TABLE `user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `uid` varchar(32) NOT NULL COMMENT '用户唯一标识(UUID)',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机号',
  `password_hash` varchar(128) NOT NULL COMMENT '密码哈希',
  `nickname` varchar(50) NOT NULL DEFAULT '' COMMENT '昵称',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像URL',
  `level` tinyint NOT NULL DEFAULT 1 COMMENT '英语等级(1-5)',
  `daily_goal` int NOT NULL DEFAULT 20 COMMENT '每日学习目标(单词数)',
  `vip_level` tinyint NOT NULL DEFAULT 0 COMMENT '会员等级(0=免费)',
  `vip_expire_at` datetime DEFAULT NULL COMMENT '会员过期时间',
  `last_login_at` datetime DEFAULT NULL COMMENT '最后登录时间',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` datetime DEFAULT NULL COMMENT '软删除时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_uid` (`uid`),
  KEY `idx_phone` (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';
```

### user_setting

```sql
CREATE TABLE `user_setting` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `daily_reminder` tinyint NOT NULL DEFAULT 1 COMMENT '每日提醒(0=关,1=开)',
  `reminder_time` time NOT NULL DEFAULT '20:00:00' COMMENT '提醒时间',
  `pronunciation` varchar(10) NOT NULL DEFAULT 'us' COMMENT '发音偏好(us/uk)',
  `theme` varchar(20) NOT NULL DEFAULT 'light' COMMENT '主题(light/dark)',
  `font_size` varchar(10) NOT NULL DEFAULT 'medium' COMMENT '字体大小',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户设置表';
```

---

## 六、业务规则

1. 手机号必须唯一，重复注册返回"手机号已注册"
2. 密码长度 6-50 位，使用 bcrypt + SHA256 预哈希存储
3. 注册时自动创建 `user_setting` 默认配置
4. 登录时校验密码，错误返回"密码错误"
5. Token 无效或过期返回 401
6. 软删除用户通过 `deleted_at` 字段标记
