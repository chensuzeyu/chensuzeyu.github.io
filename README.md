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
  3. 自检：执行 `ssh -T git@github.com`。
     - **首次连接**时若出现 `The authenticity of host ... can't be established`，以及 `ED25519 key fingerprint is SHA256:...`：这是 **SSH 主机密钥确认**，**不是报错**。原因是本机 `~/.ssh/known_hosts` 里还没有该主机的记录，OpenSSH 无法自动认定对方就是 GitHub，因此停下来询问。
     - 请将终端里打印的 **SHA256 指纹** 与 [GitHub 公布的 SSH 密钥指纹](https://docs.github.com/zh/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints) **对照**；**一致**再输入 **`yes`**，会把该主机写入 `known_hosts`，之后一般不再出现此提示（除非 GitHub 轮换密钥）。**不一致**应输入 **`no`**，并排查 DNS 是否被劫持、是否连到了伪造站点。
     - 通过后应看到类似「You've successfully authenticated, but GitHub does not provide shell access」的成功说明。
  4. **拉取**：`git pull origin main`（若跟踪分支已是 `main`，也可直接 `git pull`）。**推送**：`git push origin main`（或 `git push`）。

### 本仓库：把 `origin` 改成 SSH 并推送（命令说明）

**前提**：已在 GitHub 添加 SSH 公钥，且 `ssh -T git@github.com` 能通过（见上文步骤 3）。若出现 `Permission denied (publickey)`，说明密钥未配置或未加载，需先完成 [GitHub 文档：生成 SSH 密钥并添加到 ssh-agent](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) 与账户里的 SSH key。**若 `github.com:443` 的 HTTPS 连不上**，把远程改为 SSH 后，`push` / `pull` 会走 SSH（默认 22 端口，或由 `~/.ssh/config` 指定），不再依赖 `https://github.com/...`。

在终端中依次执行（第一行为 **Windows 下进入本仓库的示例路径**，请按你本机实际目录修改；macOS / Linux 则 `cd` 到你的克隆路径即可）：

```powershell
cd E:\code\chensuzeyu.github.io
git remote set-url origin git@github.com:chensuzeyu/chensuzeyu.github.io.git
git remote -v
git push origin main
```

| 命令 | 说明 |
|------|------|
| `cd E:\code\chensuzeyu.github.io` | 进入本地仓库根目录（必须与包含 `.git` 的目录一致）。 |
| `git remote set-url origin git@github.com:chensuzeyu/chensuzeyu.github.io.git` | 将远程名 **`origin`** 的地址改为 SSH；格式为 `git@github.com:<GitHub用户名>/<仓库名>.git`。改完后 **`git push` / `git pull` 都走 SSH**。 |
| `git remote -v` | 查看当前远程；`fetch` 与 `push` 应都显示 `git@github.com:chensuzeyu/chensuzeyu.github.io.git`。 |
| `git push origin main` | 将本地分支 **`main`** 推送到 **`origin`**。若当前已在 `main` 且已设置上游跟踪，也可简写为 **`git push`**。 |

若 **22 端口** 被限制，再在 `~/.ssh/config` 中为 `github.com` 配置走 **`ssh.github.com:443`**（见上文步骤 1 与官方文档）。

详见 [GitHub：使用 SSH 通过 HTTPS 端口连接](https://docs.github.com/zh/authentication/troubleshooting-ssh/using-ssh-over-the-https-port)（官方文档已从旧路径迁移，若收藏了旧链接会 404）。
