# iLoveEnglish APP端

## 项目说明

基于 uni-app + Vue3 开发的APP端。

## 运行方式

### 方式一：HBuilderX运行（推荐）

1. 下载安装 [HBuilderX](https://www.dcloud.io/hbuilderx.html)
2. 打开 HBuilderX
3. 文件 → 导入 → 从本地目录导入
4. 选择 `app` 目录
5. 运行 → 运行到浏览器 → Chrome
6. 或 运行 → 运行到手机或模拟器

### 方式二：命令行运行

```bash
# 安装依赖
npm install

# 运行到H5
npm run dev:h5

# 运行到微信小程序
npm run dev:mp-weixin
```

## 项目结构

```
app/
├── src/
│   ├── api/            # API请求封装
│   ├── pages/          # 页面目录
│   │   ├── index/      # 首页
│   │   ├── word/       # 单词页
│   │   ├── speaking/   # 口语页
│   │   └── profile/    # 我的页面
│   ├── stores/         # 状态管理
│   ├── static/         # 静态资源
│   ├── App.vue         # 根组件
│   ├── main.ts         # 入口文件
│   ├── pages.json      # 页面配置
│   └── manifest.json   # 应用配置
├── package.json
├── vite.config.ts
└── tsconfig.json
```

## TabBar图标

TabBar图标需要放在 `src/static/tab/` 目录下：

- home.png / home-active.png
- word.png / word-active.png
- speaking.png / speaking-active.png
- profile.png / profile-active.png

图标尺寸建议：81x81 像素

## 开发说明

1. 当前为Demo版本，部分功能未实现
2. 后端API地址配置在 `src/api/index.ts` 中
3. 默认连接 `http://localhost:8000/api`
