# 使用固定路径运行FreeCAD脚本

本文档说明如何使用固定路径的方式运行FreeCAD相关脚本，确保无论当前工作目录如何，都能正确找到FreeCAD可执行文件和脚本文件。

## 固定路径运行脚本

我们提供了一个专门的PowerShell脚本，可以使用固定的路径运行FreeCAD命令：

### 运行方法

1. 在PowerShell中执行：
```powershell
pwsh -ExecutionPolicy Bypass -File "d:\Trae Code\scripts\run_cube_with_fixed_path.ps1"
```

2. 或者直接双击运行 `run_cube_with_fixed_path.ps1` 文件（需要确保PowerShell脚本可以执行）

### 脚本功能

- **固定的FreeCAD路径**：使用 `C:\Users\admin\scoop\apps\freecad\current\bin\freecadcmd.exe`
- **固定的脚本路径**：使用 `d:\Trae Code\FreeCadpys\create_cube.py`
- **错误检查**：会检查FreeCAD可执行文件和脚本文件是否存在
- **执行结果反馈**：显示执行是否成功

## 手动运行命令

如果需要手动运行命令，可以复制以下命令到PowerShell中执行：

```powershell
C:\Users\admin\scoop\apps\freecad\current\bin\freecadcmd.exe "d:\Trae Code\FreeCadpys\create_cube.py"
```

注意：确保路径中的引号是英文引号，否则可能会导致路径解析错误。

## 查看结果

脚本执行后，会在 `d:\Trae Code\FCStds\` 目录下生成一个新的.FCStd文件，文件名包含时间戳。

您可以使用FreeCAD软件打开这个文件来查看生成的3D模型。

## 自定义参数

要使用自定义参数运行脚本，可以修改 `run_cube_with_fixed_path.ps1` 文件，在调用FreeCAD命令时添加环境变量。例如：

```powershell
# 设置环境变量
$env:FC_LENGTH = "20"
$env:FC_WIDTH = "15"
$env:FC_HEIGHT = "10"
$env:FC_FCSTD = "d:\Trae Code\FCStds\custom_cube.FCStd"

# 运行FreeCAD脚本
& $freecadPath "$scriptPath"
```