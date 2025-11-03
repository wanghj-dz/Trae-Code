#!/usr/bin/env pwsh
# 运行FreeCAD立方体创建脚本（带自定义参数）

# 设置立方体参数
$env:FC_LENGTH = 20  # 长度
$env:FC_WIDTH = 15   # 宽度
$env:FC_HEIGHT = 12  # 高度
$env:FC_NAME = "CustomCube"  # 立方体名称
$env:FC_POS = "5,5,5"  # 位置坐标
$env:FC_ROT = "15,0,0"  # 旋转角度
$env:FC_HOLE_RADIUS = 3  # 中心孔洞半径
$env:FC_HOLE_AXIS = "Z"  # 孔洞轴向
$env:FC_FCSTD = "$PSScriptRoot\..\FCStds\custom_cube.FCStd"  # 输出FCStd文件
$env:FC_STL = "$PSScriptRoot\..\stls\custom_cube.stl"  # 输出STL文件

# 显示参数信息
Write-Host "开始创建自定义立方体..."
Write-Host "参数设置："
Write-Host "- 尺寸: ${env:FC_LENGTH}x${env:FC_WIDTH}x${env:FC_HEIGHT} mm"
Write-Host "- 名称: ${env:FC_NAME}"
Write-Host "- 位置: ${env:FC_POS}"
Write-Host "- 旋转: ${env:FC_ROT} 度"
Write-Host "- 孔洞: 半径 ${env:FC_HOLE_RADIUS} mm, 轴向 ${env:FC_HOLE_AXIS}"
Write-Host "- 输出文件: ${env:FC_FCSTD}"
Write-Host "- STL文件: ${env:FC_STL}"
Write-Host ""

# 运行FreeCAD脚本
$freecadPath = "C:\Users\admin\scoop\apps\freecad\current\bin\freecadcmd.exe"

if (Test-Path $freecadPath) {
    Write-Host "启动FreeCAD命令行工具..."
    & $freecadPath "$PSScriptRoot\..\FreeCadpys\create_cube.py"
    
    # 检查输出文件是否生成
    if (Test-Path $env:FC_FCSTD) {
        Write-Host "`n✅ 立方体创建成功!"
        Write-Host "- FCStd文件路径: $env:FC_FCSTD"
    } else {
        Write-Host "`n❌ 未找到生成的FCStd文件!"
    }
    
    if (Test-Path $env:FC_STL) {
        Write-Host "- STL文件路径: $env:FC_STL"
    }
} else {
    Write-Host "❌ 未找到FreeCAD命令行工具: $freecadPath"
    Write-Host "请确认FreeCAD已正确安装且路径正确。"
}