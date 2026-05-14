# Dev01 - APP端环境搭建

## 目标

搭建 uni-app 开发环境，创建基础项目结构。

## 技术栈

- **框架**: uni-app (Vue 3)
- **构建工具**: Vite
- **状态管理**: Pinia
- **UI**: uni-app 内置组件 + uv-ui（可选）

## 项目结构

```
app/
├── pages/              # 页面目录
│   ├── index/          # 首页
│   ├── word/           # 单词学习
│   ├── wordBook/       # 词书选择
│   ├── wordList/       # 单词本
│   ├── speaking/       # 口语翻译
│   └── profile/        # 我的页面
├── components/         # 公共组件
│   ├── TabBar/         # 底部导航
│   └── common/         # 通用组件
├── stores/             # 状态管理
│   ├── user.ts         # 用户状态
│   └── word.ts         # 单词状态
├── api/                # API请求封装
│   ├── index.ts        # 请求配置
│   ├── auth.ts         # 认证API
│   ├── wordBook.ts     # 词书API
│   ├── word.ts         # 单词API
│   └── memoryTip.ts    # AI速记API
├── static/             # 静态资源
├── pages.json          # 页面配置
└── package.json
```

## 任务清单

### 1.1 项目初始化

- [ ] 确认 uni-app + Vue3 项目已创建
- [ ] 安装依赖：pinia
- [ ] 配置 TypeScript

### 1.2 配置项目

- [ ] `pages.json` - 页面配置
  - 定义页面路径和导航栏样式
  - 配置底部 TabBar（首页、学习、口语、我的）
- [ ] `manifest.json` - 应用配置

### 1.3 创建核心模块

- [ ] `api/index.ts` - uni.request 封装
  - 请求拦截器：自动添加 token
  - 响应拦截器：统一处理错误，401 跳转登录
- [ ] `stores/user.ts` - 用户状态管理
- [ ] `stores/word.ts` - 单词状态管理

### 1.4 创建布局组件

- [ ] 自定义 TabBar 组件（可选）
- [ ] 页面过渡动画

## TabBar 配置

```json
{
  "tabBar": {
    "list": [
      {
        "pagePath": "pages/index/index",
        "text": "首页",
        "iconPath": "static/tabbar/home.png",
        "selectedIconPath": "static/tabbar/home-active.png"
      },
      {
        "pagePath": "pages/word/index",
        "text": "学习",
        "iconPath": "static/tabbar/word.png",
        "selectedIconPath": "static/tabbar/word-active.png"
      },
      {
        "pagePath": "pages/speaking/index",
        "text": "口语",
        "iconPath": "static/tabbar/speaking.png",
        "selectedIconPath": "static/tabbar/speaking-active.png"
      },
      {
        "pagePath": "pages/profile/index",
        "text": "我的",
        "iconPath": "static/tabbar/profile.png",
        "selectedIconPath": "static/tabbar/profile-active.png"
      }
    ]
  }
}
```

## 验证标准

- [ ] 项目启动无报错
- [ ] H5 端可正常访问
- [ ] 底部 TabBar 可正常切换
- [ ] 各页面正常显示
