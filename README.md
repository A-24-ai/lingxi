# 一个创业者的思考

把生意想明白，把日子过踏实。一个创业者的商业认知内容站，内容源自个人知识库《胡珂的想法》，覆盖赚钱与生意、个人成长、情绪价值、行业分析、职场生存、经营故事、时事观察七大栏目。

纯静态站，基于 Astro 构建，产出静态 HTML，可直接部署到 GitHub Pages，零服务器、零账号门槛。

## 快速开始

### 环境要求

- Node.js 18+（推荐 20+）

### 安装与运行

```bash
# 安装依赖
npm install

# 本地开发（默认 http://localhost:4321）
npm run dev

# 构建静态站（输出到 dist/）
npm run build

# 预览构建产物
npm run preview
```

### 部署到 GitHub Pages

1. 将 `dist/` 目录内容推送到仓库（或配置 CI 自动构建）。
2. 在仓库 Settings → Pages 中，Source 选择部署分支对应目录（推荐 `GitHub Actions` 或 `gh-pages` 分支）。

> 部署地址在 `astro.config.mjs` 的 `site` 字段中配置，需按实际仓库地址修改。

## 目录结构

```
├── src/
│   ├── content/
│   │   └── posts/        # 文章内容（Markdown）
│   ├── components/       # Header / Footer / PostCard
│   ├── layouts/          # BaseLayout
│   ├── pages/
│   │   ├── index.astro   # 首页
│   │   ├── category/[category].astro  # 栏目页
│   │   └── posts/[...slug].astro      # 文章详情页
│   ├── content.config.ts # 内容 schema
│   └── styles/global.css # 全局样式与设计令牌
├── tools/                # 内容转换脚本（知识库 → 站点文章）
└── astro.config.mjs
```

## 技术栈

- Astro 5（内容站框架）
- @astrojs/sitemap（SEO 站点地图）
- Markdown 内容集合 + 纯 CSS 设计令牌

## 内容管理

在 `src/content/posts/` 下新增 `.md` 文件即自动生成新文章。每篇 frontmatter 需包含：

```yaml
---
title: 文章标题
description: 摘要
category: 栏目名（七选一）
date: 2026-08-18
tags: ['标签1', '标签2']
---
```
