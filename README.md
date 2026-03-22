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

## 推送与网络（推荐路径）

**默认做法：全程 SSH**，不依赖 `https://github.com/...`（国内/部分网络下 HTTPS 易超时或 reset）。

### 1. SSH 密钥：先检查，再生成（与官方顺序一致）

官方说明（细节与 macOS / Linux 见文中）：[Checking for existing SSH keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/checking-for-existing-ssh-keys) → [生成新的 SSH 密钥并添加到 ssh-agent](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) → [将 SSH 公钥添加到 GitHub 账户](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)。

下面为 **Windows PowerShell** 下的命令流程（路径、邮箱请换成你的）：

**（1）检查是否已有密钥** — 若已存在 `id_ed25519`、`id_rsa` 等密钥对，可跳过生成，直接把对应 **`.pub` 公钥** 加到 GitHub 并执行后面的 `ssh-agent` / `ssh-add`。

```powershell
Get-ChildItem $env:USERPROFILE\.ssh -Force
```

使用 **Git Bash** 时可用官方写法：`ls -al ~/.ssh`。GitHub 认可的默认公钥文件名见 [检查文档](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/checking-for-existing-ssh-keys)。

**（2）没有可用密钥时再生成**（`-C` 后为你的 GitHub 邮箱）：

```powershell
ssh-keygen -t ed25519 -C "your_email@example.com"
```

提示保存路径时直接回车即默认 `C:\Users\<用户名>\.ssh\id_ed25519`；passphrase 可按需设置或留空（详见官方文档）。

**（3）启动 ssh-agent 并加入私钥**（若密钥文件名不是 `id_ed25519`，请改路径）：

在 Windows 上，**把 `ssh-agent` 设为手动启动并启动服务** 会改系统服务配置，必须在 **「以管理员身份运行」的 PowerShell** 里执行；若在普通终端运行，会出现 **`Access is denied` / 无法配置服务**（与权限有关，不是密钥坏了）。

1. **右键「开始」→ Windows 终端 / PowerShell → 以管理员身份运行**，执行：

```powershell
Get-Service ssh-agent | Set-Service -StartupType Manual
Start-Service ssh-agent
```

2. **关掉管理员窗口**，回到你平时用的 **普通权限** PowerShell（或 Cursor 内置终端），再执行：

```powershell
ssh-add $env:USERPROFILE\.ssh\id_ed25519
```

若已完成 **（4）（5）** 且公钥已在 GitHub，也可先试 **不做（3）** 直接跑 **（6）**：部分环境会直接读默认私钥。**只有**在需要 agent、或带 passphrase 的密钥希望免反复输入时，再完成（3）。

**（4）查看并复制公钥**（整段为一行，从 `ssh-ed25519` 或 `ssh-rsa` 起到邮箱结尾）：

```powershell
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub
```

也可复制到剪贴板：`Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub | Set-Clipboard`

**（5）** 打开 GitHub → **Settings → SSH and GPG keys → New SSH key**，粘贴公钥保存（步骤说明见 [添加 SSH 公钥](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)）。

**（6）自检连接**（须出现成功认证类提示；首次会问主机真实性，对照 [GitHub SSH 指纹](https://docs.github.com/zh/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints) 后输入 `yes`）：

```powershell
ssh -T git@github.com
```

若出现类似：

```text
Hi chensuzeyu! You've successfully authenticated, but GitHub does not provide shell access.
```

即为 **自检通过**：`Hi <用户名>!` 说明 **当前 SSH 公钥已与该 GitHub 账户绑定**；`does not provide shell access` 是固定说明，表示 GitHub **不提供远程登录服务器的 shell**（不能像 VPS 那样 `ssh` 进去敲命令），**不是错误**，**不影响** `git push` / `git pull`。可继续 **§2** 改 `origin` 并推送。

**（7）若仍 `Permission denied (publickey)`**：

- **若已出现 `ssh-add ... Identity added`，但 `ssh -T` 仍失败**：说明 **agent 里已有私钥，但 GitHub 没有接受对应公钥**——与「是否做（3）」无关，不是 README 里「跳过（3）先试（6）」能单独解决的。请回到 **（4）（5）**：用 `Get-Content ...\.ssh\id_ed25519.pub` 打出 **完整一行**，与 GitHub → **Settings → SSH and GPG keys** 里已有密钥 **逐字一致**（常见问题是 **还没添加**、**复制缺字/换行**、或 **登到了另一个 GitHub 账号**）。核对后可 **New SSH key** 重新粘贴保存。
- 需要看本机到底递了哪把钥匙时，可运行 `ssh -vT git@github.com`（输出里搜 `Offering public key`）。
- Windows 上若 Git 与终端用的不是同一套 `ssh`，可让 Git 走系统 OpenSSH（与官方 Troubleshooting 一致）：

```powershell
git config --global core.sshCommand "C:/Windows/System32/OpenSSH/ssh.exe"
```

### 2. 改 `origin` 为 SSH 并推送

在仓库根目录执行（第一行路径按本机修改）：

```powershell
cd E:\code\chensuzeyu.github.io
git remote set-url origin git@github.com:chensuzeyu/chensuzeyu.github.io.git
git remote -v
git push origin main
```

`git pull` / `git push` 与上共用同一 `origin`；已在 `main` 且设好上游时可简写 `git push`。

**仅当 SSH 22 被拦**：在 `~/.ssh/config` 为 `Host github.com` 配置 `HostName ssh.github.com`、`Port 443`、`User git`，见 [经 HTTPS 端口的 SSH](https://docs.github.com/zh/authentication/troubleshooting-ssh/using-ssh-over-the-https-port)。

**其它**：HTTPS 推送若报 `RPC failed` / 连不上 443，多为网络问题，换线路或坚持用 SSH 即可。仓库开 Pages 后 Actions 里出现 *pages build* 属 GitHub 自带发布，不是你必须维护的 CI。
