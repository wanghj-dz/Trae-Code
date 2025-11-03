# GitHub登录与配置工具

本文件夹包含用于GitHub登录和操作的相关工具和配置文件，方便用户进行GitHub账户管理、仓库操作和代码推送等工作。

## 文件夹内容

- **登录gh cli的token.txt** - 存储GitHub CLI登录令牌
- **github_login.ps1** - 图形化GitHub登录与配置工具脚本

## 使用说明

### GitHub CLI 登录令牌

`登录gh cli的token.txt`文件存储了GitHub个人访问令牌（PAT），用于非交互式登录GitHub CLI。令牌格式为单行字符串，请勿在令牌前后添加额外字符或空格。

### GitHub登录与配置工具

`github_login.ps1`是一个功能完整的PowerShell脚本，提供了图形化菜单界面，支持以下功能：

1. **使用浏览器登录GitHub CLI** - 推荐的最安全登录方式
2. **使用Token登录GitHub CLI** - 自动从token.txt文件读取令牌
3. **查看GitHub登录状态** - 检查当前登录信息和权限
4. **登出GitHub CLI** - 退出当前GitHub账户
5. **配置Git用户信息** - 设置用户名和邮箱
6. **检查SSH连接** - 测试与GitHub的SSH连接
7. **生成新的SSH密钥** - 创建新的ED25519密钥对
8. **复制SSH公钥到剪贴板** - 方便添加到GitHub账户

#### 运行方法

1. 在Windows系统中，右键点击`github_login.ps1`文件
2. 选择"使用PowerShell运行"
3. 或者在PowerShell终端中执行：
   ```powershell
   cd d:\Trae Code\githubdenglu
   .\github_login.ps1
   ```

## 注意事项

1. **安全提示**：请妥善保管您的GitHub令牌，不要分享给他人
2. **令牌权限**：建议为令牌设置最小必要权限
3. **SSH密钥**：首次使用SSH连接GitHub前，请确保已将公钥添加到GitHub账户
4. **环境要求**：
   - 需要安装GitHub CLI (`gh`命令)
   - 生成SSH密钥需要安装Git或OpenSSH

## 常见问题

- **无法找到gh命令**：请先安装GitHub CLI，可通过Scoop、Winget或官网下载安装
- **SSH连接失败**：确保SSH公钥已正确添加到GitHub账户设置中
- **权限不足**：如果操作仓库时遇到权限问题，请检查令牌权限或SSH密钥配置

## 相关资源

- [GitHub CLI官方文档](https://cli.github.com/manual/)
- [GitHub创建个人访问令牌指南](https://docs.github.com/cn/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [GitHub SSH密钥设置](https://docs.github.com/cn/authentication/connecting-to-github-with-ssh)