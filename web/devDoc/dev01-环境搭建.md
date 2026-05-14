# Dev01 - 管理后台环境搭建

## 目标

搭建 Vue3 + TypeScript 管理后台开发环境，创建基础项目结构。

## 技术栈

- **框架**: Vue 3 + TypeScript
- **构建工具**: Vite
- **路由**: Vue Router 4
- **状态管理**: Pinia
- **HTTP客户端**: Axios
- **UI组件库**: Element Plus
- **图表**: ECharts（可选）

## 项目结构

```
web/
├── src/
│   ├── api/            # API请求封装
│   │   ├── index.ts    # axios配置
│   │   ├── auth.ts     # 认证API
│   │   ├── wordBook.ts # 词书API
│   │   ├── word.ts     # 单词API
│   │   └── memoryTip.ts# AI速记API
│   ├── components/     # 公共组件
│   │   ├── Layout/     # 布局组件
│   │   └── common/     # 通用组件
│   ├── router/         # 路由配置
│   ├── stores/         # 状态管理
│   ├── views/          # 页面组件
│   │   ├── auth/       # 认证页面
│   │   ├── wordBook/   # 词书管理
│   │   ├── word/       # 单词管理
│   │   ├── memoryTip/  # AI速记管理
│   │   └── user/       # 用户管理
│   └── App.vue
├── public/
├── package.json
└── vite.config.ts
```

## 任务清单

### 1.1 项目初始化

- [ ] 确认 Vue3 + Vite + TypeScript 项目已创建
- [ ] 安装依赖：vue-router@4, pinia, axios, element-plus
- [ ] 安装图标库：@element-plus/icons-vue

### 1.2 配置项目

- [ ] `vite.config.ts` - 配置路径别名 `@` 指向 `src`
- [ ] 配置开发服务器代理，将 `/api` 转发到后端

### 1.3 创建核心模块

- [ ] `src/api/index.ts` - axios 实例配置
  - 请求拦截器：自动添加 token
  - 响应拦截器：统一处理错误，401 跳转登录
- [ ] `src/router/index.ts` - 路由配置
  - 路由守卫：未登录跳转登录页
- [ ] `src/stores/user.ts` - 用户状态管理

### 1.4 创建布局组件

- [ ] `src/components/Layout/index.vue` - 后台布局
  - 顶部导航栏
  - 左侧菜单
  - 主内容区域
- [ ] `src/components/Layout/Menu.vue` - 菜单组件

## 验证标准

- [ ] 项目启动无报错
- [ ] 访问 http://localhost:3000 显示登录页
- [ ] 登录后显示后台管理界面
- [ ] 左侧菜单可正常切换
