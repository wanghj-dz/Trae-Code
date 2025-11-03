#!/usr/bin/env pwsh
# 固定路径运行FreeCAD脚本的PowerShell脚本
# 此脚本使用固定的FreeCAD命令行工具路径和脚本路径

# 设置固定的FreeCAD命令行工具路径
$freecadPath = "C:\Users\admin\scoop\apps\freecad\current\bin\freecadcmd.exe"

# 设置固定的Python脚本路径
$scriptPath = "d:\Trae Code\FreeCadpys\create_cube.py"

# 输出运行信息
Write-Host "使用固定路径运行FreeCAD脚本..."
Write-Host "FreeCAD路径: $freecadPath"
Write-Host "脚本路径: $scriptPath"
Write-Host ""

# 检查FreeCAD可执行文件是否存在
if (-not (Test-Path $freecadPath)) {
    Write-Host "错误: 无法找到FreeCAD可执行文件 '$freecadPath'" -ForegroundColor Red
    exit 1
}

# 检查Python脚本是否存在
if (-not (Test-Path $scriptPath)) {
    Write-Host "错误: 无法找到脚本文件 '$scriptPath'" -ForegroundColor Red
    exit 1
}

# 运行FreeCAD脚本
Write-Host "正在运行脚本..."
Write-Host ""
& $freecadPath "$scriptPath"

# 检查命令执行结果
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "脚本执行成功!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "脚本执行失败，退出代码: $LASTEXITCODE" -ForegroundColor Red
}