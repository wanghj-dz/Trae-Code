#!/usr/bin/env pwsh
# -*- coding: utf-8 -*-
"""
GitHub登录与配置脚本
用于方便地登录GitHub CLI和配置Git设置
"""

function Show-Menu {
    Write-Host "===================================" -ForegroundColor Cyan
    Write-Host "        GitHub 登录与配置工具        " -ForegroundColor Cyan
    Write-Host "===================================" -ForegroundColor Cyan
    Write-Host "1. 使用浏览器登录GitHub CLI"
    Write-Host "2. 使用Token登录GitHub CLI"
    Write-Host "3. 查看GitHub登录状态"
    Write-Host "4. 登出GitHub CLI"
    Write-Host "5. 配置Git用户信息"
    Write-Host "6. 检查SSH连接"
    Write-Host "7. 生成新的SSH密钥"
    Write-Host "8. 复制SSH公钥到剪贴板"
    Write-Host "0. 退出"
    Write-Host "===================================" -ForegroundColor Cyan
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
        $tokenPath = Join-Path -Path $PSScriptRoot -ChildPath "登录gh cli的token.txt"
        if (Test-Path $tokenPath) {
            $token = Get-Content -Path $tokenPath -First 1 -ErrorAction Stop
            Write-Host "从token.txt文件读取登录令牌..." -ForegroundColor Yellow
            echo $token | gh auth login --with-token
            Write-Host "✓ Token登录完成!" -ForegroundColor Green
        } else {
            Write-Host "请输入GitHub令牌: " -ForegroundColor Yellow -NoNewline
            $token = Read-Host -AsSecureString
            $tokenPlain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($token))
            echo $tokenPlain | gh auth login --with-token
            Write-Host "✓ Token登录完成!" -ForegroundColor Green
        }
    } catch {
        Write-Host "❌ Token登录失败: $_" -ForegroundColor Red
    }
}

function Get-GhStatus {
    Write-Host "正在检查GitHub CLI登录状态..." -ForegroundColor Yellow
    try {
        gh auth status
        Write-Host "✓ 状态检查完成!" -ForegroundColor Green
    } catch {
        Write-Host "❌ 状态检查失败: $_" -ForegroundColor Red
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
        Write-Host "请输入Git用户名: " -ForegroundColor Yellow -NoNewline
        $username = Read-Host
        
        Write-Host "请输入Git邮箱: " -ForegroundColor Yellow -NoNewline
        $email = Read-Host
        
        git config --global user.name "$username"
        git config --global user.email "$email"
        
        Write-Host "✓ Git用户信息配置完成!" -ForegroundColor Green
        Write-Host "用户名: $username" -ForegroundColor Cyan
        Write-Host "邮箱: $email" -ForegroundColor Cyan
    } catch {
        Write-Host "❌ Git用户信息配置失败: $_" -ForegroundColor Red
    }
}

function Test-SshConnection {
    Write-Host "正在检查GitHub SSH连接..." -ForegroundColor Yellow
    try {
        if (Get-Command ssh -ErrorAction SilentlyContinue) {
            ssh -T git@github.com 2>&1 | ForEach-Object {
                if ($_ -match "successfully authenticated") {
                    Write-Host "✓ GitHub SSH连接成功!" -ForegroundColor Green
                } elseif ($_ -match "Permission denied") {
                    Write-Host "❌ GitHub SSH连接失败: 权限被拒绝" -ForegroundColor Red
                    Write-Host "请确保您的SSH密钥已添加到GitHub账户。" -ForegroundColor Yellow
                }
            }
        } else {
            Write-Host "❌ 未找到SSH命令，请确保已安装Git或OpenSSH。" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ SSH连接测试失败: $_" -ForegroundColor Red
    }
}

function New-SshKey {
    try {
        Write-Host "请输入您的邮箱地址: " -ForegroundColor Yellow -NoNewline
        $email = Read-Host
        
        Write-Host "正在生成新的SSH密钥..." -ForegroundColor Yellow
        if (Get-Command ssh-keygen -ErrorAction SilentlyContinue) {
            ssh-keygen -t ed25519 -C "$email"
            Write-Host "✓ SSH密钥生成完成!" -ForegroundColor Green
            Write-Host "密钥默认保存在: $HOME/.ssh/id_ed25519" -ForegroundColor Cyan
        } else {
            Write-Host "❌ 未找到ssh-keygen命令，请确保已安装Git或OpenSSH。" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ SSH密钥生成失败: $_" -ForegroundColor Red
    }
}

function Copy-SshPublicKey {
    try {
        $pubKeyPath = "$HOME/.ssh/id_ed25519.pub"
        if (Test-Path $pubKeyPath) {
            Get-Content -Path $pubKeyPath | Set-Clipboard
            Write-Host "✓ SSH公钥已复制到剪贴板!" -ForegroundColor Green
            Write-Host "请将其粘贴到GitHub账户设置中的SSH and GPG keys页面。" -ForegroundColor Yellow
        } else {
            Write-Host "❌ 未找到SSH公钥文件: $pubKeyPath" -ForegroundColor Red
            Write-Host "请先生成SSH密钥。" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ 复制SSH公钥失败: $_" -ForegroundColor Red
    }
}

# 主程序
Write-Host "欢迎使用GitHub登录与配置工具!" -ForegroundColor Green

while ($true) {
    Show-Menu
    Write-Host "请选择操作 (0-8): " -ForegroundColor Yellow -NoNewline
    $choice = Read-Host
    
    switch ($choice) {
        '1' {
            if (Test-GhInstallation) {
                Invoke-GhBrowserLogin
            }
        }
        '2' {
            if (Test-GhInstallation) {
                Invoke-GhTokenLogin
            }
        }
        '3' {
            if (Test-GhInstallation) {
                Get-GhStatus
            }
        }
        '4' {
            if (Test-GhInstallation) {
                Invoke-GhLogout
            }
        }
        '5' {
            Set-GitUserInfo
        }
        '6' {
            Test-SshConnection
        }
        '7' {
            New-SshKey
        }
        '8' {
            Copy-SshPublicKey
        }
        '0' {
            Write-Host "感谢使用，再见!" -ForegroundColor Green
            break
        }
        default {
            Write-Host "无效的选择，请重新输入!" -ForegroundColor Red
        }
    }
    
    if ($choice -ne '0') {
        Write-Host "`n按Enter键继续..." -ForegroundColor Gray
        Read-Host
    }
}