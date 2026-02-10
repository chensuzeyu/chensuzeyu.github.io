# Personal Site (C 版极简预览)

HTML 个人主页，纯静态，便于 GitHub Pages 部署。

## 目录结构

```
personal-site/
├── index.html      # 入口页
├── css/
│   └── style.css   # 样式
├── images/
│   ├── favicon.jpg
│   └── profile.png
└── README.md
```

## 本地预览

- 用浏览器直接打开 `index.html`，或
- 在项目根目录执行：`npx serve .` 或 `python -m http.server 8000`，然后访问对应地址。

## GitHub 部署 (GitHub Pages)

1. 在 GitHub 新建仓库，将本目录推送到该仓库。
2. 仓库 **Settings → Pages**：
   - **Source** 选 **Deploy from a branch**
   - **Branch** 选 `main`（或你的默认分支），目录选 **/ (root)**
3. 保存后等待构建，站点地址为：`https://<用户名>.github.io/<仓库名>/`

若仓库名为 `<用户名>.github.io`，则直接为：`https://<用户名>.github.io/`。
