#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
显示已安装Python库的位置信息
"""

import sys
import site
import subprocess
import os

# 获取site-packages目录
def get_site_packages():
    print("Python包安装位置信息:")
    print("=" * 70)
    print(f"Python解释器路径: {sys.executable}")
    print(f"Python版本: {sys.version}")
    print("\nsite-packages目录:")
    for path in site.getsitepackages():
        print(f"  - {path}")
    print(f"用户site-packages目录: {site.USER_SITE}")
    print("=" * 70)

# 获取已安装的主要库的位置
def get_installed_packages_locations(packages):
    print("\n已安装库的具体位置:")
    print("=" * 70)
    print(f"{'库名':<20} {'版本':<15} {'安装位置':<40}")
    print("=" * 70)
    
    for package in packages:
        try:
            # 使用pip show命令获取包信息
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'show', package],
                capture_output=True,
                text=True,
                check=True
            )
            
            # 解析输出信息
            info = {}
            for line in result.stdout.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    info[key.strip()] = value.strip()
            
            # 显示包名、版本和位置
            name = info.get('Name', package)
            version = info.get('Version', '未知')
            location = info.get('Location', '未知')
            
            print(f"{name:<20} {version:<15} {location:<40}")
            
            # 显示实际代码所在目录
            package_dir = os.path.join(location, name)
            if os.path.exists(package_dir):
                print(f"{'':<36} 代码目录: {package_dir}")
            
        except subprocess.CalledProcessError:
            print(f"{package:<20} {'未安装':<15} {'N/A':<40}")
        except Exception as e:
            print(f"{package:<20} {'错误':<15} {str(e):<40}")
    
    print("=" * 70)

# 获取所有已安装的包列表
def list_all_installed_packages():
    try:
        print("\n所有已安装的Python包列表:")
        print("=" * 70)
        subprocess.run(
            [sys.executable, '-m', 'pip', 'list', '--format=columns'],
            check=True
        )
    except Exception as e:
        print(f"获取所有包列表时出错: {e}")

if __name__ == "__main__":
    # 获取site-packages位置
    get_site_packages()
    
    # 检查我们刚才安装的主要库
    main_packages = ['numpy', 'pandas', 'matplotlib', 'scikit-learn', 'requests']
    get_installed_packages_locations(main_packages)
    
    # 提示用户是否要查看所有已安装的包
    print("\n注意: 要查看所有已安装的包，请运行 'pip list'")
    print("要获取某个特定包的详细信息，请运行 'pip show 包名'")