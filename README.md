# Personal Site (C 版极简预览)

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

## GitHub 部署 (GitHub Pages)

1. 在 GitHub 新建仓库，将本目录推送到该仓库。
2. 仓库 **Settings → Pages**：
   - **Source** 选 **Deploy from a branch**
   - **Branch** 选 `main`（或你的默认分支），目录选 **/ (root)**
3. 保存后等待构建，站点地址为：`https://<用户名>.github.io/<仓库名>/`

若仓库名为 `<用户名>.github.io`，则直接为：`https://<用户名>.github.io/`。

---

## 补充说明（常识与排障）

### 推送后 GitHub 上为何像有「自动 Action」？

- 仓库名 **`用户名.github.io`** 的作用是：**GitHub Pages 用户站** 的默认域名在 `https://用户名.github.io/`，与「是否写了自己的工作流」无必然关系。
- 在 **Settings → Pages** 中若使用 **Deploy from a branch**，每次向该分支推送后，GitHub 会执行 **内置的 Pages 发布流程**，在 **Actions** 里可能显示为 *pages build and deployment* 等；这**不等于**你在仓库里提交了 `.github/workflows/*.yml` 才会跑。
- **自定义 Action** 仍依赖仓库内（或组织级）的工作流配置；单靠起名不会自动生成你的业务 CI。

### Git 报错：`RPC failed` / `curl 28` / `Recv failure: Connection was reset`

- 多出现在 **`git push` / `git pull` 走 HTTPS** 时，表示与 `github.com` 的 **连接在传输过程中被重置或超时**，一般是 **当前网络、防火墙、代理、运营商路径** 等问题，而不是仓库损坏。
- 可依次尝试：**换网络或热点**、**调整 VPN 开关**、**重试**；也可在 Git 中尝试（可按需 `--global` 或仅本仓库 `git config`）：
  - `git config http.version HTTP/1.1` — 部分环境下比 HTTP/2 更稳。
  - `git config http.postBuffer 524288000` — 增大 HTTP 缓冲。
  - `git config http.lowSpeedLimit 0` 与 `git config http.lowSpeedTime 999999` — 降低因瞬时低速被中断的概率。
  - `git config core.compression 0` — 推送时不压缩对象，减轻 CPU 与部分链路问题。
  - Windows 上可试 `git config http.sslBackend schannel`（改用系统证书链）；若变差可 `git config --unset http.sslBackend`。
- **若 HTTPS 长期不稳定**，可改用 **SSH，并走 443 端口**（与 `git push` / `git pull` 共用同一远程，改一次即可）：
  1. 在 GitHub 账户中配置好 **SSH 公钥**；编辑 `~/.ssh/config`，为 **`Host github.com`** 写入 `HostName ssh.github.com`、`Port 443`、`User git`（与官方说明一致）。
  2. 在仓库目录执行：`git remote set-url origin git@github.com:用户名/仓库.git`（将 `用户名/仓库` 换成你的路径，例如本仓库为 `chensuzeyu/chensuzeyu.github.io`）。
  3. 可选自检：`ssh -T git@github.com`，应出现成功认证提示。
  4. **拉取**：`git pull origin main`（若跟踪分支已是 `main`，也可直接 `git pull`）。**推送**：`git push origin main`（或 `git push`）。

  详见 [GitHub：使用 SSH 通过 HTTPS 端口连接](https://docs.github.com/zh/authentication/troubleshooting-ssh/using-ssh-over-the-https-port)（官方文档已从旧路径迁移，若收藏了旧链接会 404）。
