# I Love English - 网页端

## 技术栈

- **框架**: Vue 3 + TypeScript
- **构建工具**: Vite
- **路由**: Vue Router 4
- **状态管理**: Pinia
- **HTTP客户端**: Axios
- **UI组件库**: Element Plus

## 项目结构

```
web/
├── src/
│   ├── api/            # API请求封装
│   ├── components/     # 公共组件
│   ├── router/         # 路由配置
│   ├── stores/         # 状态管理
│   ├── views/          # 页面组件
│   └── App.vue         # 根组件
├── public/             # 静态资源
├── package.json        # 依赖配置
└── vite.config.ts      # Vite配置
```

## 快速开始

### 1. 环境准备

- Node.js 18.x+
- npm 或 yarn

### 2. 安装依赖

```bash
npm install
# 或
yarn install
```

### 3. 启动开发服务器

```bash
npm run dev
# 或
yarn dev
```

### 4. 访问

打开浏览器访问 http://localhost:3000

## 构建生产版本

```bash
npm run build
# 或
yarn build
```

## 开发文档

详细的开发任务文档请查看 [devDoc](./devDoc/) 目录。
