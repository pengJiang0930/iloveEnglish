# Dev02 - 数据库搭建

## 目标

配置 MySQL 数据库连接，创建数据模型，执行数据库迁移。

## 任务清单

### 2.1 创建 MySQL 数据库

- [ ] 创建 `ilove_english` 数据库（utf8mb4）
- [ ] 确认 MySQL 服务可正常连接

### 2.2 配置数据库连接

- [ ] 完善 `app/core/config.py` - 添加数据库配置项
- [ ] 完善 `app/core/database.py` - SQLAlchemy 异步引擎 + 会话工厂
- [ ] 创建 `.env` 文件 - 数据库连接信息

### 2.3 创建数据模型

- [ ] `app/models/base.py` - 基础模型（公共字段）
- [ ] `app/models/user.py` - 用户模型
- [ ] `app/models/user_setting.py` - 用户设置模型
- [ ] `app/models/__init__.py` - 统一导出

### 2.4 配置 Alembic 迁移

- [ ] 初始化 Alembic
- [ ] 配置异步迁移引擎
- [ ] 生成初始迁移脚本
- [ ] 执行迁移，验证表结构

## 数据库表结构

### user 表

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
  KEY `idx_phone` (`phone`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';
```

### user_setting 表

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

## 验证标准

- [ ] MySQL 数据库创建成功
- [ ] Alembic 迁移执行成功
- [ ] user、user_setting 表创建成功
- [ ] 表结构与设计一致
