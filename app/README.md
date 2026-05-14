# I Love English - APP端

## 技术栈

- **框架**: uni-app (Vue 3)
- **构建工具**: Vite
- **状态管理**: Pinia
- **UI**: uni-app 内置组件

## 项目结构

```
app/
├── pages/              # 页面目录
│   ├── index/          # 首页
│   ├── word/           # 单词页
│   ├── speaking/       # 口语页
│   └── profile/        # 我的页面
├── components/         # 公共组件
├── stores/             # 状态管理
├── api/                # API请求封装
├── static/             # 静态资源
├── pages.json          # 页面配置
└── package.json        # 依赖配置
```

## 快速开始

### 1. 环境准备

- Node.js 18.x+
- HBuilderX (推荐) 或 npm

### 2. 安装依赖

```bash
npm install
```

### 3. 运行项目

**方式一：HBuilderX运行**
1. 打开 HBuilderX
2. 文件 → 导入 → 从本地目录导入
3. 选择 `app` 目录
4. 运行 → 运行到浏览器 → Chrome

**方式二：命令行运行**
```bash
# H5端
npm run dev:h5

# 微信小程序
npm run dev:mp-weixin

# APP
npm run dev:app
```

### 4. 访问

- H5端: 运行后会自动打开浏览器
- 微信小程序: 使用微信开发者工具打开 `dist/dev/mp-weixin` 目录

## 构建生产版本

```bash
# H5端
npm run build:h5

# 微信小程序
npm run build:mp-weixin

# APP
npm run build:app
```

## 开发文档

详细的开发任务文档请查看 [devDoc](./devDoc/) 目录。
