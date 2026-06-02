# Personal Site

HTML 个人主页，纯静态，便于 GitHub Pages 部署。

## 目录结构

```
personal-site/
├── index.html      # 入口页
├── serve.py        # 本地预览（打印 127.0.0.1 / [::] 提示后启动 http.server）
├── css/
│   └── style.css   # 样式
├── images/
│   ├── favicon.jpg
│   └── profile.png
└── README.md
```

## 本地预览

- 用浏览器直接打开 `index.html`，或
- 在项目根目录执行：`npx serve .`，或 **`python serve.py`**（推荐：会先打印 IPv4 / `[::]` 地址再启动服务），或 `python -m http.server 8000`。
- 浏览器可访问 **`http://127.0.0.1:8000`**（IPv4）；终端若出现 **`[::]:8000`**，也可用 **`http://[::]:8000`**。
