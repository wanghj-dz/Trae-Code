# Python项目说明文档

## 项目概述
这是一个简单的Python项目，已适配Trae AI环境。

## 环境配置

### Python版本信息
- **python命令**: Python 3.14.0 (通过scoop安装) - 用于运行普通Python程序
- **py命令**: Python 3.13.5 (FreeCAD自带) - 用于运行FreeCAD相关Python程序

### 项目配置文件
项目包含以下主要配置文件：

1. **.env** - 环境变量配置
   - 包含Python路径设置
   - Trae环境特定配置
   - 日志级别设置

2. **setup.cfg** - 项目安装配置
   - 项目元数据
   - Python版本要求 (>=3.13)
   - 代码风格检查配置 (flake8)
   - 测试配置 (pytest)
   - 代码覆盖率配置
   - Trae特定配置部分

## Trae环境适配
项目已针对Trae AI环境进行了适配：
- 在.env文件中添加了Trae特定环境变量
- 在setup.cfg中添加了Trae配置部分
- 支持多Python版本环境

## 运行项目

### 普通Python程序
使用Python 3.14.0运行：
```
python hello_world.py
```

### 检查Python版本
```
python --version  # 应显示 Python 3.14.0
py --version      # 应显示 Python 3.13.5
```

## 已安装Python库
本项目已通过腾讯云镜像源安装了以下常用Python库：

| 库名称 | 版本 | 用途 |
|-------|------|------|
| numpy | 2.3.4 | 科学计算和数组操作 |
| pandas | 2.3.3 | 数据分析和处理 |
| matplotlib | 3.10.7 | 数据可视化 |
| scikit-learn | 1.7.2 | 机器学习算法 |
| requests | 2.32.5 | HTTP请求处理 |

库安装位置：`C:\Users\admin\scoop\apps\python\current\Lib\site-packages`

## 库调用配置

### 基本导入示例
```python
# 导入numpy进行数组操作
import numpy as np

# 导入pandas进行数据处理
import pandas as pd

# 导入matplotlib进行绘图
import matplotlib.pyplot as plt

# 导入scikit-learn进行机器学习
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# 导入requests进行网络请求
import requests
```

### 示例代码
```python
# 使用numpy创建数组
data = np.array([1, 2, 3, 4, 5])
print(f"Numpy数组: {data}")

# 使用pandas创建DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35]
})
print(f"\nPandas DataFrame:\n{df}")

# 使用matplotlib绘图
plt.figure(figsize=(8, 6))
plt.plot([1, 2, 3, 4], [10, 20, 25, 30])
plt.title('示例图表')
plt.xlabel('X轴')
plt.ylabel('Y轴')
plt.savefig('example_plot.png')
print("\n图表已保存为example_plot.png")

# 使用requests发送请求
response = requests.get('https://httpbin.org/get')
print(f"\n请求状态码: {response.status_code}")
```

## Python镜像源管理工具

本项目包含一个镜像源管理工具`pypi_mirror_manager.py`，用于管理国内Python包镜像源。

### 功能介绍
- 测试多个国内镜像源的连接速度
- 使用最快的镜像源安装/更新Python包
- 设置/取消默认镜像源
- 列出所有可用镜像源
- 批量更新已安装的包

### 使用示例
```bash
# 测试所有镜像源速度
python pypi_mirror_manager.py test

# 列出所有可用镜像源
python pypi_mirror_manager.py list

# 使用特定镜像源安装包
python pypi_mirror_manager.py install package_name -m "腾讯云"

# 更新所有已安装的包
python pypi_mirror_manager.py update-all

# 设置默认镜像源
python pypi_mirror_manager.py set-default "清华大学"

# 取消默认镜像源设置
python pypi_mirror_manager.py unset-default

# 显示当前默认镜像源
python pypi_mirror_manager.py show-default
```

## 注意事项
- 确保环境变量正确加载
- 根据程序类型选择合适的Python版本运行
- Trae环境下自动启用相关配置
- 使用镜像源管理工具可以提高Python包安装速度，避免网络问题
- 如需要安装其他库，推荐使用项目中的镜像源管理工具或直接通过腾讯云镜像源安装