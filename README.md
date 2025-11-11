# Trae-Code 仓库（汇总说明）

本 README 为仓库根的快速说明，包含 FreeCAD 开发环境与示例脚本的引用说明。

## FreeCadpys 目录使用说明（已摘录并同步）

本目录包含 FreeCAD Draft 工作台的示例脚本、运行包装脚本和调试日志，方便在无 GUI 的 `freecadcmd` 环境下运行并将结果保存到仓库根的 `FCStds/` 目录。

主要文件

- `FreeCadpys/draft_line_example.py`：Draft 工作台示例脚本。
  - 功能：使用 Draft.makeLine 在 FreeCAD 文档中创建一条直线（Line），并可将文档保存为 `.FCStd`。
  - 参数：支持命令行参数（`--x1 --y1 --z1 --x2 --y2 --z2 --name --fcstd`），也支持通过环境变量回退（`FC_LENGTH`、`FC_WIDTH`、`FC_HEIGHT`、`FC_NAME`、`FC_FCSTD`）。
  - 调试：脚本会在同目录下写入 `FreeCadpys/draft_line_debug.txt`，记录启动参数、解析结果、创建和保存状态，以及可能的错误堆栈。

- `FreeCadpys/scripts/run_draft_line.ps1`：PowerShell wrapper（推荐使用）。
  - 目的：解决在 Windows PowerShell 下直接用 `freecadcmd --pass` 传参时的引号/转义问题。
  - 工作方式：生成一个临时 Python wrapper（设置 `sys.argv`），然后调用 `freecadcmd` 去运行该临时文件，从而可靠地把参数传给 `FreeCadpys/draft_line_example.py`。

为何使用 wrapper

- 在 PowerShell 中使用 `freecadcmd --pass '...args...'` 常出现引号/转义问题，导致脚本无法正确接收到参数或参数被拆分/转义。
- `run_draft_line.ps1` 通过生成临时 Python 文件并直接交给 `freecadcmd` 来运行，从而避免了 `--pass` 的复杂转义，运行稳定可靠。

运行示例（推荐，使用 wrapper）

在仓库根的 `FreeCadpys` 目录下运行：

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\FreeCadpys\scripts\run_draft_line.ps1 \
  -x1 0 -y1 0 -z1 0 -x2 50 -y2 0 -z2 0 -name MyLine -fcstd '..\FCStds\myline_from_wrapper.FCStd'
```

运行后你应该看到类似输出：

- Created line 'MyLine' from Vector (0.0, 0.0, 0.0) to Vector (50.0, 0.0, 0.0)
- Saved document to ..\FCStds\myline_from_wrapper.FCStd

并在仓库根的 `FCStds/` 中生成 `myline_from_wrapper.FCStd`。

直接用 freecadcmd（可选，常受转义问题影响）

如果你想直接调用 `freecadcmd`，可以尝试下面这种形式（注意 PowerShell 中的引号）：

```powershell
& 'C:\Users\admin\scoop\apps\freecad\current\bin\freecadcmd.exe' '.\FreeCadpys\draft_line_example.py' --pass '--x1 0 --y1 0 --z1 0 --x2 50 --y2 0 --z2 0 --name "MyLine" --fcstd "..\FCStds\myline.FCStd"'
```

说明：如果参数被转发错误，脚本会尝试以下回退策略（按顺序）：

1. argparse.parse_known_args（忽略未知参数）
2. 从原始 argv 字符串用正则提取常用参数（处理被拆分或换行的情况）
3. 使用环境变量（`FC_LENGTH` / `FC_WIDTH` / `FC_HEIGHT` / `FC_NAME` / `FC_FCSTD`）

调试信息

- 调试日志文件：`FreeCadpys/draft_line_debug.txt`。
  - 包含：脚本启动时的 argv、解析到的参数、unknown argv、创建对象标签、保存结果或保存错误的堆栈信息。

注意事项与限制

- 直线只是边（线），不是实体；对于导出 STL 或 3D 打印，需要先把线转换为体（例如生成窄长的长方体或使用 Sweep/Pad 等操作）。
- 脚本依赖 FreeCAD 环境（需用 `freecadcmd` 或 FreeCAD 的 Python 解释器运行）；在非 FreeCAD 的普通系统 Python 中运行会直接退出并提示错误。
- 如果你在其它机器上运行，请确认 `freecadcmd.exe` 的路径与你机器上的安装路径一致（示例中假定使用 Scoop 安装路径）。

下一步建议

- 我可以把该示例的使用说明保持在这里，或根据需要把更详细的步骤写入仓库根 README 的特定节。
- 我也可以把示例扩展为：先由直线生成一个窄长实体并导出 STL（如需生成可打印模型）。

如果你需要我把 README 内容格式或内容调整为其它风格（英文、更多示例、或把 wrapper 改为跨平台的 Python 脚本），告诉我具体偏好，我会继续修改。

# FreeCAD远程服务器

一个功能完整的FreeCAD远程控制服务器，支持通过网络远程执行FreeCAD命令并获取结果。

## 项目概述

本项目提供了一个基于TCP/IP协议的FreeCAD远程控制服务器，允许客户端通过网络连接发送FreeCAD命令并接收执行结果。服务器支持多线程并发处理，使用JSON格式进行数据交换，具有完善的错误处理机制。

## 核心功能

- ✅ **远程FreeCAD控制**：通过TCP/IP协议远程执行FreeCAD命令
- ✅ **多线程处理**：支持多个客户端并发连接
- ✅ **JSON通信协议**：使用JSON格式进行命令传输和结果返回
- ✅ **安全的命令执行**：在隔离的命名空间中执行用户命令
- ✅ **错误处理与调试**：完善的异常捕获和堆栈跟踪
- ✅ **资源管理**：自动清理连接资源

## 文件结构

```
d:\Trae-Code\
├── freecad_server_direct.py      # 核心服务器程序
├── test_freecad_commands.py      # 命令测试客户端
├── freecad_server_simple.py      # 简化版服务器（调试用）
├── test_server_client.py         # 基础连接测试客户端
└── README.md                     # 项目文档（当前文件）
```

## 服务器程序

### freecad_server_direct.py

核心服务器实现，包含以下功能：

- FreeCAD模块加载与初始化
- TCP服务器创建与配置
- 多线程客户端连接处理
- JSON命令解析与执行
- 错误捕获与异常处理
- 结果格式化与返回

## 客户端程序

### test_freecad_commands.py

全面的命令测试客户端，用于验证服务器功能：

- 连接到FreeCAD服务器
- 发送预定义的测试命令序列
- 显示命令执行结果
- 错误处理与用户友好提示

## 安装要求

- FreeCAD 1.0.2 或更高版本
- Python 3.11 或更高版本
- 标准库（socket, threading, json, traceback）

## 使用方法

### 启动服务器

```bash
& 'C:\Users\admin\scoop\apps\freecad\current\bin\freecadcmd.exe' '.\freecad_server_direct.py'
```

服务器将启动并监听在 `127.0.0.1:5555` 端口。

### 运行测试客户端

```bash
python test_freecad_commands.py
```

测试客户端将连接到服务器并执行一系列测试命令。

### 自定义客户端开发

您可以开发自己的客户端程序，通过以下步骤与服务器通信：

1. 创建TCP连接到服务器地址（127.0.0.1:5555）
2. 发送JSON格式的命令请求：

   ```json
   {"command": "FreeCAD.Version()"}
   ```

3. 接收JSON格式的响应：

   ```json
   {
     "status": "success",
     "result": {
       "value": "['1', '0', '2', ...]"
     }
   }
   ```

## 测试结果

测试客户端执行以下命令：

1. **获取FreeCAD版本信息**：`result = FreeCAD.Version()`
   - 成功返回FreeCAD的详细版本信息

2. **创建3D模型**：

   ```python

doc = FreeCAD.newDocument("TestDoc");
obj = doc.addObject("Part::Box", "Box");
obj.Length=10;
obj.Width=10;
obj.Height=10;
doc.recompute();
result = obj.Shape.Volume

   ```
   - 成功创建10x10x10的立方体并计算体积

3. **文档管理**：`result = [doc.Name for doc in FreeCAD.listDocuments().values()]`
   - 正确获取创建的文档列表

## 扩展建议

1. 添加身份验证机制增强安全性
2. 实现文件上传/下载功能
3. 支持更复杂的3D模型操作
4. 添加WebSocket支持以实现双向实时通信
5. 开发Web界面进行远程控制

## 注意事项

- 本服务器设计为本地网络使用，建议不要直接暴露在互联网上
- 执行用户命令时存在一定的安全风险，生产环境中应添加额外的安全措施
- 大型模型操作可能会消耗较多系统资源，建议根据实际硬件配置调整

## 许可证

本项目采用MIT许可证 - 详情请查看LICENSE文件

## 联系方式

如有任何问题或建议，请随时联系项目维护者。

---

*最后更新：2024年*

## 推送与远程 (GitHub / GitCode)

本仓库配置了多个远程（示例）：

- `github` — 使用 SSH 地址（git@github.com:wanghj-dz/Trae-Code.git），我已将它设置为默认推送远程（`remote.pushDefault=github`），因此执行 `git push` 会推送到 GitHub（通过 SSH）。
- `gitcode` — 使用 HTTPS（示例中可能含嵌入凭证），用于同步到 GitCode 平台。
- `origin` — 当前指向 GitHub 的 HTTPS URL（原始设置），可能包含嵌入的 token 或用户名。

常用检查命令：

```

git remote -v
git config --get remote.pushDefault
git ls-remote --heads github main
git ls-remote --heads gitcode main

```

推荐的推送命令：

```

# 推送当前分支到默认远程（默认已设置为 github）

git push

# 明确推送到 gitcode

git push gitcode $(git branch --show-current)

# 推送 tags 到两个远程（如需要）

git push --tags github
git push --tags gitcode

```

安全与清理建议：

- 当前 `origin` 或 `gitcode` 的 URL 如果含有嵌入的凭证（例如 `https://user:token@...`），这会带来安全风险。建议将远程 URL 改为不含凭证的形式，或改用 SSH。示例：

```

# 把 origin 改为 SSH（若你希望统一使用 SSH）

git remote set-url origin <git@github.com>:wanghj-dz/Trae-Code.git

# 把 gitcode 改为不含凭证的 HTTPS（由系统凭证管理器处理）

git remote set-url gitcode <https://gitcode.com/wanghj_dz/Trae-Code.git>

```

如果你希望我现在把 `origin` 或 `gitcode` 的 URL 从嵌入凭证的形式改为 SSH 或清理凭证，回复想要的操作，我可以替你执行并验证推送（包括再次把更改推送到两个远程）。
