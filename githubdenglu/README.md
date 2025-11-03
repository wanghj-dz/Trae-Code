# GitHub登录与配置工具

## 工具简介

这是一个基于PowerShell的GitHub登录与配置工具，采用文件输入方式替代终端直接输入，解决系统无法复制粘贴到终端的限制问题。工具提供了图形化菜单界面，操作简单直观。

## 临时文件说明

### 临时文件位置
临时文件位于脚本所在目录（即`d:\Trae Code\githubdenglu\`），包括：

- `temp_token.txt` - 用于输入GitHub token
- `temp_user.txt` - 用于输入Git用户名
- `temp_email.txt` - 用于输入Git邮箱

### 临时文件使用方法

1. **文件准备**：在运行相应功能前，请确保在脚本目录下创建并编辑好对应的临时文件
2. **使用方式**：工具会自动读取这些临时文件中的内容进行操作
3. **安全提示**：请在使用完毕后手动删除包含敏感信息的临时文件
4. **注意事项**：
   - 临时文件需要手动创建和编辑
   - 文件内容格式为单行文本，请勿添加额外字符或空格

## 使用方法

1. 在PowerShell终端中执行：
   ```powershell
   cd d:\Trae Code\githubdenglu
   .\github_login.ps1
   ```
2. 在显示的菜单中选择相应功能（输入数字0-5）
3. 工具会自动读取相应的临时文件内容
4. 完成操作后，根据提示继续或退出

## 主要功能

`github_login.ps1`脚本支持以下功能：

1. **使用浏览器登录GitHub CLI** - 通过浏览器进行交互式身份验证
2. **使用Token登录GitHub CLI** - 从`temp_token.txt`文件读取token进行登录
3. **查看GitHub登录状态** - 检查当前登录信息和权限
4. **登出GitHub CLI** - 退出当前GitHub会话
5. **配置Git用户信息** - 从临时文件设置用户名和邮箱
6. **退出程序** - 结束工具运行

## 文件夹内容

- `github_login.ps1` - 主脚本文件，提供图形化GitHub登录与配置工具
- `temp_token.txt` - 用于输入GitHub个人访问令牌的临时文件

## 注意事项

1. **安全提示**：请妥善保管您的GitHub令牌，不要分享给他人
2. **令牌权限**：建议为令牌设置最小必要权限
3. **环境要求**：需要安装GitHub CLI (`gh`命令)
4. **PowerShell执行策略**：如果遇到执行策略限制，请以管理员身份运行PowerShell并执行`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned`

## 常见问题

- **无法找到gh命令**：请先安装GitHub CLI，可通过Scoop、Winget或官网下载安装
- **令牌读取失败**：确保`temp_token.txt`文件存在且包含有效的GitHub令牌
- **权限不足**：如果操作仓库时遇到权限问题，请检查令牌权限配置

## 相关资源

- [GitHub CLI官方文档](https://cli.github.com/manual/)
- [GitHub创建个人访问令牌指南](https://docs.github.com/cn/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)