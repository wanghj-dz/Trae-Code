#!/usr/bin/env pwsh
# -*- coding: utf-8 -*-
"""
GitHub登录与配置脚本 (文件输入版本)
通过文件方式输入token，避免终端复制粘贴问题
"""

function Show-Menu {
    # 清屏，确保菜单显示清晰
    Clear-Host
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "        GitHub 登录与配置工具          " -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "🔹 1. 使用浏览器登录GitHub CLI" -ForegroundColor Green
    Write-Host "🔹 2. 使用Token登录GitHub CLI (通过文件输入)" -ForegroundColor Green
    Write-Host "🔹 3. 查看GitHub登录状态" -ForegroundColor Green
    Write-Host "🔹 4. 登出GitHub CLI" -ForegroundColor Green
    Write-Host "🔹 5. 配置Git用户信息" -ForegroundColor Green
    Write-Host "🔹 0. 退出" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
}

function Test-GhInstallation {
    try {
        $null = Get-Command gh -ErrorAction Stop
        return $true
    } catch {
        Write-Host "错误: 未找到GitHub CLI (gh)。请先安装gh工具。" -ForegroundColor Red
        Write-Host "可以通过以下方式安装:"
        Write-Host "1. 使用Scoop: scoop install gh"
        Write-Host "2. 使用Winget: winget install GitHub.cli"
        Write-Host "3. 从官网下载: https://cli.github.com/"
        return $false
    }
}

function Invoke-GhBrowserLogin {
    Write-Host "正在启动浏览器登录GitHub CLI..." -ForegroundColor Yellow
    try {
        gh auth login
        Write-Host "✓ 浏览器登录完成!" -ForegroundColor Green
    } catch {
        Write-Host "❌ 浏览器登录失败: $_" -ForegroundColor Red
    }
}

function Invoke-GhTokenLogin {
    try {
        # 定义临时token文件路径
        $tempTokenPath = Join-Path -Path $PSScriptRoot -ChildPath "temp_token.txt"
        
        # 检查文件是否存在
        if (-not (Test-Path $tempTokenPath)) {
            Write-Host "⚠️  temp_token.txt 文件不存在，正在创建..." -ForegroundColor Yellow
            New-Item -Path $tempTokenPath -ItemType File -Force | Out-Null
            Write-Host "🔹 请将GitHub Token写入以下文件:" -ForegroundColor Yellow
            Write-Host "   文件路径: $tempTokenPath" -ForegroundColor Cyan
            Write-Host "   请打开此文件，将Token粘贴进去，保存并关闭" -ForegroundColor Gray
            Write-Host "🔹 编辑完成后，按任意键继续..." -ForegroundColor Yellow
            [Console]::ReadKey($true)
        } else {
            # 文件存在，直接尝试读取
            Write-Host "✅ 检测到temp_token.txt文件存在，正在尝试读取..." -ForegroundColor Green
        }
        
        # 尝试使用多种方式读取文件内容
        $token = $null
        
        # 方式1: 使用System.IO.File
        try {
            $token = [System.IO.File]::ReadAllText($tempTokenPath).Trim()
            Write-Host "📄 使用System.IO.File成功读取文件内容" -ForegroundColor Gray
        } catch {
            Write-Host "⚠️ System.IO.File读取失败，尝试备用方式..." -ForegroundColor Yellow
            
            # 方式2: 使用Get-Content
            try {
                $token = Get-Content -Path $tempTokenPath -Raw -Encoding UTF8 -ErrorAction Stop
                $token = $token.Trim()
                Write-Host "📄 使用Get-Content成功读取文件内容" -ForegroundColor Gray
            } catch {
                Write-Host "⚠️ Get-Content读取失败，尝试简化方式..." -ForegroundColor Yellow
                
                # 方式3: 使用简化的Get-Content
                $token = Get-Content -Path $tempTokenPath | Out-String
                $token = $token.Trim()
            }
        }
        
        # 检查token是否有效
        if (-not [string]::IsNullOrEmpty($token)) {
            # 显示token预览（保护敏感信息）
            $preview = $token.Substring(0, [Math]::Min(8, $token.Length))
            Write-Host "🔑 Token读取成功（预览: $preview...）" -ForegroundColor Green
            
            # 直接使用token进行登录
            Write-Host "🚀 正在使用令牌登录GitHub..." -ForegroundColor Yellow
            
            # 创建临时管道文件以避免直接在命令中暴露token
            $tempPipeFile = Join-Path -Path $PSScriptRoot -ChildPath "temp_pipe.txt"
            $token | Set-Content -Path $tempPipeFile -Force
            Get-Content -Path $tempPipeFile | gh auth login --with-token
            Remove-Item -Path $tempPipeFile -Force -ErrorAction SilentlyContinue
            
            # 验证登录是否成功
            $authStatus = gh auth status -h github.com -t
            if ($LASTEXITCODE -eq 0) {
                Write-Host "🎉 Token登录成功!" -ForegroundColor Green
            } else {
                Write-Host "❌ Token登录失败，可能是Token无效或已过期" -ForegroundColor Red
            }
        } else {
            Write-Host "❌ Token文件内容为空或只包含空白字符" -ForegroundColor Red
            Write-Host "   请确保正确将Token写入文件" -ForegroundColor Gray
        }
    } catch {
        Write-Host "❌ Token登录处理过程中发生错误: $_" -ForegroundColor Red
        Write-Host "   错误详情: $($_.Exception.Message)" -ForegroundColor Gray
    }
}

function Get-GhLoginStatus {
    Write-Host "当前GitHub登录状态:" -ForegroundColor Yellow
    try {
        gh auth status
    } catch {
        Write-Host "❌ 检查状态失败: $_" -ForegroundColor Red
    }
}

function Invoke-GhLogout {
    Write-Host "正在登出GitHub CLI..." -ForegroundColor Yellow
    try {
        gh auth logout
        Write-Host "✓ 登出完成!" -ForegroundColor Green
    } catch {
        Write-Host "❌ 登出失败: $_" -ForegroundColor Red
    }
}

function Set-GitUserInfo {
    try {
        Write-Host "当前Git用户配置:" -ForegroundColor Yellow
        git config --global user.name
        git config --global user.email
        
        # 创建临时文件用于输入用户名
        $tempUserPath = Join-Path -Path $PSScriptRoot -ChildPath "temp_user.txt"
        
        Write-Host "`n🔹 请手动编辑临时文件设置Git用户名:" -ForegroundColor Yellow
        Write-Host "   文件路径: $tempUserPath" -ForegroundColor Cyan
        Write-Host "   (如果不想修改，保持文件为空即可)" -ForegroundColor Gray
        Write-Host "🔹 编辑完成后，按任意键继续..." -ForegroundColor Yellow
        
        # 创建空文件
        New-Item -Path $tempUserPath -ItemType File -Force | Out-Null
        
        # 等待用户编辑文件
        [Console]::ReadKey($true)
        
        # 读取用户名
        if (Test-Path $tempUserPath) {
            $userName = Get-Content -Path $tempUserPath -Raw -ErrorAction Stop | Trim-String
            
            if (-not [string]::IsNullOrEmpty($userName)) {
                git config --global user.name $userName
                Write-Host "✓ Git用户名已更新" -ForegroundColor Green
            }
            
            # 删除临时文件
            Remove-Item -Path $tempUserPath -Force -ErrorAction SilentlyContinue
        }
        
        # 创建临时文件用于输入邮箱
        $tempEmailPath = Join-Path -Path $PSScriptRoot -ChildPath "temp_email.txt"
        
        Write-Host "`n🔹 请手动编辑临时文件设置Git邮箱:" -ForegroundColor Yellow
        Write-Host "   文件路径: $tempEmailPath" -ForegroundColor Cyan
        Write-Host "   (如果不想修改，保持文件为空即可)" -ForegroundColor Gray
        Write-Host "🔹 编辑完成后，按任意键继续..." -ForegroundColor Yellow
        
        # 创建空文件
        New-Item -Path $tempEmailPath -ItemType File -Force | Out-Null
        
        # 等待用户编辑文件
        [Console]::ReadKey($true)
        
        # 读取邮箱
        if (Test-Path $tempEmailPath) {
            $userEmail = Get-Content -Path $tempEmailPath -Raw -ErrorAction Stop | Trim-String
            
            if (-not [string]::IsNullOrEmpty($userEmail)) {
                git config --global user.email $userEmail
                Write-Host "✓ Git邮箱已更新" -ForegroundColor Green
            }
            
            # 删除临时文件
            Remove-Item -Path $tempEmailPath -Force -ErrorAction SilentlyContinue
        }
    } catch {
        Write-Host "❌ 配置Git用户信息失败: $_" -ForegroundColor Red
    }
}

# 辅助函数：修剪字符串
function Trim-String {
    param (
        [string]$InputString
    )
    return $InputString.Trim()
}

# 主程序
Write-Host "欢迎使用GitHub登录与配置工具! (文件输入版本)" -ForegroundColor Green
Write-Host "📝 本版本通过文件方式输入信息，避免终端复制粘贴限制" -ForegroundColor Cyan

# 检查GitHub CLI是否安装
if (-not (Test-GhInstallation)) {
    Write-Host "请先安装GitHub CLI后再使用此工具。" -ForegroundColor Yellow
    exit 1
}

# 主循环
while ($true) {
    Show-Menu
    # 增加明显的输入提示和更长的延迟
    Write-Host "
请输入您的选择 (0-5)，然后按Enter键: " -ForegroundColor Yellow -NoNewline
    # 增加延迟时间，确保用户有足够时间查看菜单
    Start-Sleep -Seconds 1
    $choice = Read-Host
    
    # 检查输入是否为空
    if ([string]::IsNullOrEmpty($choice)) {
        Write-Host "⚠️  输入为空，请输入有效的选择 (0-5)" -ForegroundColor Yellow
    } else {
        # 转换为整数进行比较
        $intChoice = $null
        if ([int]::TryParse($choice, [ref]$intChoice)) {
            switch ($intChoice) {
                1 { Invoke-GhBrowserLogin }
                2 { Invoke-GhTokenLogin }
                3 { Get-GhLoginStatus }
                4 { Invoke-GhLogout }
                5 { Set-GitUserInfo }
                0 {
                    Write-Host "感谢使用，再见!" -ForegroundColor Green
                    exit 0
                }
                default {
                    Write-Host "❌ 无效的选择，请输入 0-5 之间的数字" -ForegroundColor Red
                }
            }
        } else {
            Write-Host "❌ 请输入有效的数字选择" -ForegroundColor Red
        }
    }
    
    Write-Host "`n按任意键继续..." -ForegroundColor Gray
    [Console]::ReadKey($true)
}