# FreeCAD 开发环境与脚本示例

这是一个完整的 FreeCAD 开发环境，包含脚本示例、调试配置和GUI宏，用于快速开始 FreeCAD 自动化开发。

## 项目结构

```
├── .gitignore               # Git忽略文件配置
├── .logs\                   # 日志文件夹
├── .vscode\                 # VS Code 配置目录
├── FCMacros\                # FreeCAD宏文件夹
│   └── create_cube_gui.FCMacro  # FreeCAD GUI宏示例
├── FCStds\                  # FreeCAD标准文档文件夹
├── FreeCadpys\              # FreeCAD Python脚本文件夹
│   └── create_cube.py       # 命令行立方体创建脚本
├── README.md                # 项目说明文档
├── githubdenglu\            # GitHub登录相关文件夹
│   ├── README.md            # GitHub登录说明
│   └── github_login.ps1     # GitHub登录脚本
├── modules\                 # 自定义模块文件夹
├── putongpys\               # 通用Python脚本文件夹
│   └── hello_world.py       # 示例脚本
├── scripts\                 # 辅助脚本文件夹
│   ├── README_FIXED_PATH.md # 固定路径运行说明
│   ├── run_cube_with_fixed_path.ps1 # 固定路径运行脚本
│   └── run_cube_with_params.ps1 # 带参数运行脚本
└── stls\                    # STL文件输出文件夹
```

## 环境要求

- **FreeCAD**：通过Scoop安装的FreeCAD 1.0.2或更高版本
- **Python**：使用FreeCAD内置的Python解释器
- **VS Code**：推荐1.70.0或更高版本
- **插件**：Python扩展（ms-python.python）

## 安装与设置

### 1. FreeCAD安装

已通过Scoop安装FreeCAD：

```powershell
scoop install freecad
```

FreeCAD安装路径：`C:\Users\admin\scoop\apps\freecad\current\bin\`

### 2. VS Code配置

所有VS Code配置文件已经预配置完成，包括：

- **调试配置**：通过`launch.json`支持FreeCAD脚本调试
- **任务配置**：通过`tasks.json`支持一键运行FreeCAD脚本
- **环境设置**：通过`settings.json`配置代码补全、格式化等功能

## 使用方法

### 1. 命令行脚本使用

**pys/create_cube.py** - 创建立方体的命令行脚本

#### 运行方式：

```powershell
# 直接运行（使用默认参数）
& 'C:\Users\admin\scoop\apps\freecad\current\bin\freecadcmd.exe' '.\pys\create_cube.py'

# 使用环境变量设置参数
$env:FC_LENGTH=20; $env:FC_WIDTH=15; $env:FC_HEIGHT=10; & 'C:\Users\admin\scoop\apps\freecad\current\bin\freecadcmd.exe' '.\pys\create_cube.py'

# 使用命令行参数
& 'C:\Users\admin\scoop\apps\freecad\current\bin\freecadcmd.exe' '.\pys\create_cube.py' --length=20 --width=15 --height=10

# 使用PowerShell脚本（推荐）
& '.\scripts\run_cube_with_params.ps1'
```

#### 支持的参数：

- `length`, `width`, `height`：立方体尺寸（mm）
- `name`：立方体名称
- `pos`：位置坐标，格式："x,y,z"
- `rot`：旋转角度，格式："rx,ry,rz"
- `holeRadius`：中心孔洞半径
- `holeAxis`：孔洞轴向（X/Y/Z）
- `fcstd`：输出的.FCStd文件路径（默认：FCStds/目录下）
- `stl`：输出的.STL文件路径

### 2. GUI宏使用

**FCMacros/create_cube_gui.FCMacro** - 在FreeCAD图形界面中运行的宏

#### 运行方式：

1. 打开FreeCAD图形界面
2. 点击菜单：**宏** > **宏管理器**
3. 点击**打开**按钮，选择`FCMacros/create_cube_gui.FCMacro`文件
4. 点击**运行**按钮执行宏

或者，您可以将宏安装到FreeCAD的用户宏目录中，便于以后使用：

1. 点击菜单：**宏** > **宏管理器**
2. 点击**从文件安装**按钮
3. 选择`FCMacros/create_cube_gui.FCMacro`文件
4. 给宏命名并保存

### 3. 在VS Code中调试

#### 调试命令行脚本：

1. 打开`pys/create_cube.py`文件
2. 在需要调试的行设置断点（点击行号左侧）
3. 点击左侧的调试图标（或按F5）
4. 在调试配置下拉菜单中选择：
   - **"FreeCAD Python 脚本调试"** - 基础调试
   - **"FreeCAD 带参数脚本调试"** - 带预设参数调试

#### 通用Python调试：

可以使用`assistant_debug_config.json`中的配置进行普通Python脚本调试。您可以将其内容复制到`launch.json`中使用。

### 4. 使用VS Code任务

项目配置了三个任务：

1. **"运行FreeCAD脚本"** - 运行当前打开的FreeCAD脚本（默认任务）
2. **"运行FreeCAD脚本(带参数)"** - 使用预设参数运行当前脚本
3. **"FreeCAD版本检查"** - 检查FreeCAD版本信息

运行任务：
- 按`Ctrl+Shift+B`运行默认任务
- 或按`Ctrl+Shift+P`，输入"任务"选择相应任务

## VS Code设置详解

### settings.json

- **Python解释器**：配置为FreeCAD内置的Python
- **代码补全**：添加FreeCAD库路径以支持自动补全
- **代码格式化**：使用black进行代码格式化
- **代码检查**：使用flake8进行代码质量检查
- **文件关联**：将.FCMacro文件识别为Python文件
- **文件监视排除**：排除.FCStd和.stl等二进制文件

### launch.json

包含两个FreeCAD脚本调试配置：
- **基础调试**：直接运行当前文件
- **带参数调试**：设置环境变量参数后运行

### tasks.json

包含三个Shell任务：
- **运行脚本**：一键运行当前FreeCAD脚本
- **带参数运行**：设置环境变量后运行脚本
- **版本检查**：验证FreeCAD安装

## FreeCAD Python API简介

FreeCAD提供了强大的Python API，主要模块包括：

- **FreeCAD**：核心模块，提供文档操作、向量计算等功能
- **Part**：提供基本几何体创建和操作功能
- **FreeCADGui**：GUI相关功能，仅在图形界面模式可用
- **Draft**：提供二维绘图功能
- **Sketch**：提供草图功能

## 常见问题解答

### 1. 为什么无法导入FreeCAD模块？

确保使用FreeCAD内置的Python解释器运行脚本，而不是系统Python。在VS Code中，settings.json已配置正确的Python路径。

### 2. 如何自定义立方体参数？

可以通过环境变量或命令行参数设置参数，详见脚本使用部分。

### 3. 如何导出STL文件？

使用`stl`参数指定STL输出路径，或在环境变量中设置`FC_STL`。

### 4. 如何在GUI中调试宏？

在FreeCAD中，可以通过宏管理器的**编辑**按钮打开宏编辑器，设置断点并调试。

### 5.如何配置GitHub
- 任务列表：
  - gh: Bootstrap (check/install) — 一键检查是否已安装 gh；若未安装支持用 Scoop 或 winget 引导安装。
  - gh: Login (browser) — 推荐。浏览器登录方式，不需要手动管理令牌。
  - gh: Login with token (masked) — 令牌输入会遮蔽，令牌通过内存管道传给 `gh auth login --with-token`，不落盘且不进入历史。
  - gh: Status — 查看当前登录状态。
  - gh: Logout — 登出当前主机（github.com）。
  - gh: PR Create (web) — 基于当前仓库与分支，在浏览器中创建 PR（自动填充）。
  - gh: PR Status — 查看当前仓库/分支的 PR 状态。
  - gh: PR View (web) — 打开当前分支关联的 PR 页面。
  - gh: Issue Create (web) — 在浏览器中创建 Issue。
  - gh: Repo View (web) — 打开当前仓库页面。
  - gh: Setup Git — 由 gh 自动配置 Git 凭据（适用于首次配置或切换账户）。
  - gh: Create Release (web) — 在浏览器中创建 Release（交互式表单）。
  - gh: Release Create (prompt, generate-notes) — 任务内交互输入 Tag（如 v0.1.1），自动生成 Release Notes 并创建发布。
  - gh: Release Create (prompt, draft) — 创建“草稿”发布（可先校对、再正式发布），同样自动生成 Release Notes。
  - gh: Releases View (web) — 在浏览器中查看 Release 页面。
  - gh: Diagnostics (log) — 采集 gh/git/环境信息并输出日志路径，便于排障。
    - gh: Release Append CN Highlights (auto) — 自动从 git 提交生成“中文要点”并追加到指定版本的 Release 说明顶部（保留原说明）。
  - gh: Install global toolkit (user tasks) — 一键将本仓库的脚本安装到用户目录（%USERPROFILE%\.vscode-gh-toolkit\scripts），并生成用户级 tasks 片段，实现在“任何路径/文件夹”中直接使用这些任务。
  - module: Install RepoToolkit (user scope) — 将轻量 PowerShell 模块 RepoToolkit 安装到用户模块目录（Documents\PowerShell\Modules），从而可直接调用函数而非脚本路径。
  - module: Repo Create & Push (public, HTTPS) — 示例：通过模块函数执行创建并推送。
  - repo: Create & Push (private/public) — 在 GitHub 上创建与文件夹同名的仓库并推送当前工作区内容。
  - repo: Create & Push (choose visibility) — 运行前交互选择 `private`/`public`/`internal` 后创建并推送（注：`internal` 仅适用于组织仓库）。
  - repo: Create & Push (public, HTTPS) / (private, HTTPS) — 使用 HTTPS 远程（适合未配置 SSH key 的环境）。

运行方式：

1) VS Code 菜单 Terminal -> Run Task…，选择上述任一任务
2) 或 Ctrl+Shift+P 输入 “Tasks: Run Task”，再选择需要的任务

注意事项：

- 如果你之前把令牌明文写在命令行里，请立即到 GitHub Settings -> Developer settings -> Tokens 页面撤销该令牌，并以最小权限重建。
- `gh: Login (browser)` 是最安全且最省心的方式；若必须使用令牌，建议仅授予必要 scope（例如：repo / workflow / gist 视你的需求）。
- 任务使用 PowerShell（pwsh）执行，已兼容你的默认 Shell。

若未安装 gh，可先运行 `gh: Bootstrap (check/install)`：

- 检测到 Scoop 时，优先提供 `scoop install gh`；
- 无 Scoop 但有 winget 时，提供 `winget install GitHub.cli -e`；
- 都没有时，会打开 gh 下载页面（<https://cli.github.com/>）。

常见问题：

- 任务如提示找不到 gh，安装完成后可能需要重启 VS Code 或终端使 PATH 生效。
- PR/Issue 相关任务需要当前工作区就是一个 git 仓库并已设置远程 `origin` 指向 GitHub。
- Release 相关任务需要当前仓库对 GitHub 有写权限；首次使用建议先运行 “gh: Setup Git”。
- 诊断日志会保存在工作区目录 `.logs/` 下，文件名形如 `gh-diagnostics-YYYYMMDD-HHMMSS.txt`。

提示：

- 若未配置 SSH key，推荐使用 HTTPS 任务或在交互式任务中勾选 HTTPS 变体（通过 -UseHttps）。
- 也可以后续在仓库中切换远程：`git remote set-url origin https://github.com/<owner>/<repo>.git`。

### 在 HTTPS 与 SSH 之间切换

已内置两条 VS Code 任务，便于一键切换当前仓库的远程 `origin`：

- repo: Switch remote to HTTPS — 将 `origin` 设置为 `https://github.com/<owner>/<repo>.git`
- repo: Switch remote to SSH — 将 `origin` 设置为 `git@github.com:<owner>/<repo>.git`
- repo: Prefer HTTPS (no SSH key) — 取消可能存在的全局 URL 重写规则（把 https 改写成 ssh），将 gh 的 git_protocol 设为 https，并切换远程到 HTTPS
- repo: Prefer SSH — 将 gh 的 git_protocol 设为 ssh，并切换远程为 SSH（可选添加 URL 重写规则，见脚本注释）

使用方法：Terminal -> Run Task… -> 选择上面任一任务。脚本会优先通过 `gh repo view` 获取标准的 `<owner>/<repo>`，若不可用则从现有 `origin` 解析。

若选择 SSH，请确保本机已配置 SSH 公钥并已添加到 GitHub：

- 生成密钥（如尚未生成）：

```pwsh
ssh-keygen -t ed25519 -C "you@example.com"
```

- 复制公钥内容到剪贴板并粘贴到 GitHub Settings -> SSH and GPG keys：

```pwsh
Get-Content $HOME/.ssh/id_ed25519.pub | Set-Clipboard
```

- 验证连通：

```pwsh
ssh -T git@github.com
```

切换完成后，可用 `git remote -v` 查看当前远程是否已更新。

提示：若你看到 `git push` 到 https 仍然走 SSH 并报 “Permission denied (publickey)” 的情况，多半是全局配置里有一条 URL 重写规则：

```ini
[url "git@github.com:"]
  insteadof = https://github.com/
```

执行 “repo: Prefer HTTPS (no SSH key)” 任务会自动移除此规则，并将远程切回 HTTPS；随后再推送即可。

### 全局安装（任何路径/文件夹可用）

如果你希望在任意项目中都能直接使用这些任务，而不必复制 `.vscode` 和 `scripts`，可执行任务：

- gh: Install global toolkit (user tasks)

它会：

- 将本仓库的脚本复制到 `%USERPROFILE%\.vscode-gh-toolkit\scripts`
- 生成用户级任务文件片段：`%USERPROFILE%\.vscode-gh-toolkit\tasks.user.json`
- 如用户级任务尚未存在，会直接安装到 `%APPDATA%\Code\User\tasks.json`
- 若已存在，则保留现有文件，并提示你在 VS Code 中通过 “Tasks: Open User Tasks” 打开并合并（拷贝片段内容到你的 user tasks）

从此以后，即使新建一个空文件夹打开 VS Code，也可以通过 Terminal -> Run Task… 直接使用以 `global:` 前缀开头的任务（例如 `global: repo: Create & Push (private, HTTPS)`）。
另外还提供：`global: gh: Release Create (prompt, generate-notes)`，在任意仓库目录下交互创建发布。
以及：`global: gh: Release Create (prompt, draft)`，用于先创建草稿版发布。
以及：`global: gh: Release Append CN Highlights (auto)`，可在任意目录为指定 tag 追加中文要点。

## 六、PowerShell 模块：RepoToolkit（可选，更优雅）

为获得更优雅的命令式体验（无需硬编码脚本路径），我们提供轻量模块 `RepoToolkit`（当前版本：0.1.0）：

- 安装（VS Code 任务）：`module: Install RepoToolkit (user scope)`
- 安装（命令行）：

```pwsh
pwsh -NoProfile -ExecutionPolicy Bypass -File "${workspaceFolder}/scripts/install-module-RepoToolkit.ps1"
```

安装后可用的函数（示例）：

- `Invoke-RepoCreateAndPush -Visibility public -UseHttps -NoPrompt`
- `Set-RepoRemoteHttps` / `Set-RepoRemoteSsh`
- `Set-GitPreferenceHttps` / `Set-GitPreferenceSsh`
- `Install-RepoToolkitGlobalTasks`（安装用户级全局任务）
- `Invoke-GhBootstrap` / `Invoke-GhDiagnostics` / `Invoke-GhLoginToken`

你也可以将这些函数放入 VS Code 用户级任务中直接调用（无需引用脚本路径）。

### 自更新（覆盖安装）

- 工作区任务：`module: Self-update RepoToolkit`（重新复制并导入 0.1.x 版本模块）
- 全局任务片段也包含：`global: module: Self-update RepoToolkit`（前提：已运行一次 “gh: Install global toolkit (user tasks)”）

### 全局模块任务（依赖 RepoToolkit 已安装）

运行 `gh: Install global toolkit (user tasks)` 后，你将看到以 `global: module:` 开头的任务，例如：

- global: module: Repo Create & Push (public, HTTPS)
- global: module: Set Remote HTTPS / SSH
- global: module: Prefer HTTPS / SSH
- global: module: Self-update RepoToolkit

### 一键创建远程仓库并 Push（与文件夹同名）

1) 先确保已登录 gh（运行任务：`gh: Login (browser)`）并完成 Git 凭据配置（`gh: Setup Git`）。
2) 运行任务：

   - `repo: Create & Push (private)` — 创建私有仓库并推送
   - `repo: Create & Push (public)` — 创建公开仓库并推送

脚本会：

- 以工作区文件夹名作为 GitHub 仓库名（例如 `D:\FreeCad` -> `FreeCad`）
- 如未初始化 git，则自动 `git init`、首个提交并将默认分支统一为 `main`
- 使用 `gh repo create <name> --<visibility> --source . --remote origin --push` 创建远程并推送
- 若远程已存在，则直接 `git push -u origin HEAD`

可能的提示：

- 首次提交若失败，多半是 git 用户名/邮箱未配置；可运行 `gh: Setup Git` 或手动：

  ```pwsh
  git config user.name "Your Name"
  git config user.email you@example.com
  ```



 
## 七、重装后的备份/恢复与一键引导

为了在重装 VS Code 或换机后快速恢复你的用户配置（设置、快捷键、任务、代码片段与扩展列表），本仓库提供了三条开箱即用的任务与对应脚本：

- VS Code: Backup user (zip) — 备份用户配置为一个 zip
- VS Code: Restore user (latest, merge tasks) — 从最新备份恢复，并“合并”任务（避免覆盖你当前已有的用户任务）
- VS Code: Bootstrap after reinstall — 一键引导：安装全局工具任务、安装 RepoToolkit 模块、合并用户任务；可选同时自动安装扩展

你可以在当前工作区通过 Terminal -> Run Task… 直接运行上述三条任务；或者先运行“gh: Install global toolkit (user tasks)”，之后在任何目录都能看到以 global: 开头的同名任务：

- global: VS Code: Backup user (zip)
- global: VS Code: Restore user (latest, merge tasks)
- global: VS Code: Bootstrap after reinstall

备份 zip 默认保存到：`%USERPROFILE%\.vscode-gh-toolkit\backups\vscode-user-YYYYMMDD-HHMMSS.zip`

备份内容包含：

- `%APPDATA%\Code\User\settings.json`
- `%APPDATA%\Code\User\keybindings.json`
- `%APPDATA%\Code\User\tasks.json`
- `%APPDATA%\Code\User\snippets\` 下的全部文件
- 当前已安装扩展列表（extensions.txt）
- 如果存在，还会包含全局任务片段：`%USERPROFILE%\.vscode-gh-toolkit\tasks.user.json`

恢复说明：

- Restore 脚本默认取“最新”的备份 zip；也可通过 `-ZipPath` 指定某个备份文件。
- 带 `-MergeTasks` 时，会将备份中的用户任务与当前用户任务按 label 去重合并；不带此参数则直接覆盖用户任务。
- 带 `-InstallExtensions` 时，会按备份中的 extensions.txt 安装扩展（可选）。

一键引导（Bootstrap）说明：

- 重装 VS Code 后，先在任意文件夹打开 VS Code，运行任务“VS Code: Bootstrap after reinstall”。
- 它会：
  - 安装/更新全局工具任务（复制脚本到 `%USERPROFILE%\\.vscode-gh-toolkit\\scripts` 并生成用户级任务）
  - 安装/更新 PowerShell 模块 RepoToolkit（用户作用域）
  - 合并用户任务（避免覆盖现有）
  - 如果附带 `-InstallExtensions`，还会从你的最新备份中自动安装扩展
- 完成后重载 VS Code，即可在任何目录直接使用以 `global:` 开头的任务。

提示：如果你之前尚未创建任何备份，建议先在当前环境运行一次“VS Code: Backup user (zip)”。



## 八、版本历史 / 变更日志

- v0.1.1 — Release Create（交互/自动说明）
  - 新增发布任务与脚本：`gh: Release Create (prompt, generate-notes)`（工作区）与 `global: gh: Release Create (prompt, generate-notes)`（全局）
  - 新增 Draft 变体：`gh: Release Create (prompt, draft)` 与 `global: gh: Release Create (prompt, draft)`
  - 链接：<https://github.com/wanghj-dz/FreeCad/releases/tag/v0.1.1>

- v0.1.0 — 备份/恢复/引导（VS Code 用户配置）
  - 新增 `backup-vscode-user.ps1`、`restore-vscode-user.ps1`、`bootstrap-after-reinstall.ps1`
  - 全局安装器集成以上脚本并生成 global: 任务；补充工作区任务
  - 修复备份 zip 目标路径问题；完善 README
  - 链接：<https://github.com/wanghj-dz/FreeCad/releases/tag/v0.1.0>




## 许可证

本项目为示例代码，可自由使用和修改。

## 版本历史

- **v1.0**：初始版本，包含基本的立方体创建脚本和调试配置
- **v1.1**：添加了GUI宏示例和完整的VS Code配置

## 联系方式

如有问题或建议，请在此项目中提交issue或联系项目维护者。