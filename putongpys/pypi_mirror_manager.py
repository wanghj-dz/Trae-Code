#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python包镜像源管理工具

功能：
1. 测试多个国内镜像源的连接速度
2. 自动使用最快的镜像源安装/更新Python包
3. 一键设置/取消默认镜像源
4. 列出所有可用镜像源

支持的镜像源：
- 清华大学
- 阿里云
- 豆瓣
- 中国科学技术大学
- 华为云
- 腾讯云
"""

import os
import time
import subprocess
import sys
import json
import argparse
from concurrent.futures import ThreadPoolExecutor
import tempfile

# 国内主要Python镜像源列表
MIRRORS = {
    "清华源": "https://pypi.tuna.tsinghua.edu.cn/simple",
    "阿里云": "https://mirrors.aliyun.com/pypi/simple/",
    "豆瓣源": "https://pypi.doubanio.com/simple/",
    "中科大源": "https://pypi.mirrors.ustc.edu.cn/simple/",
    "华为云": "https://mirrors.huaweicloud.com/repository/pypi/simple/",
    "腾讯云": "https://mirrors.cloud.tencent.com/pypi/simple/"
}

# 配置文件路径
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".pypi_mirror_config.json")

# 用于测试的小型包（通常很小，下载快）
TEST_PACKAGE = "pip"

def load_config():
    """加载配置文件"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
    return {"default_mirror": None}

def save_config(config):
    """保存配置文件"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存配置文件失败: {e}")

def test_mirror_speed(mirror_name, mirror_url):
    """测试单个镜像源的下载速度"""
    start_time = time.time()
    try:
        # 创建临时目录用于下载
        with tempfile.TemporaryDirectory() as temp_dir:
            # 使用pip下载包信息，不安装
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'download', '--no-deps', '-d', temp_dir, 
                 f'--index-url={mirror_url}', '--trusted-host', mirror_url.split('//')[1].split('/')[0],
                 '--quiet', TEST_PACKAGE],
                check=True,
                capture_output=True,
                text=True
            )
            elapsed_time = time.time() - start_time
            return mirror_name, mirror_url, elapsed_time, True
    except subprocess.CalledProcessError as e:
        return mirror_name, mirror_url, float('inf'), False
    except Exception as e:
        return mirror_name, mirror_url, float('inf'), False

def test_all_mirrors():
    """测试所有镜像源的速度"""
    print("正在测试所有镜像源的连接速度...\n")
    
    results = []
    # 使用线程池并行测试所有镜像源
    with ThreadPoolExecutor(max_workers=len(MIRRORS)) as executor:
        future_to_mirror = {executor.submit(test_mirror_speed, name, url): (name, url) 
                           for name, url in MIRRORS.items()}
        
        for future in future_to_mirror:
            result = future.result()
            results.append(result)
    
    # 按速度排序（最快的在前）
    results.sort(key=lambda x: x[2])
    
    # 显示结果
    print("镜像源速度测试结果:")
    print("-" * 70)
    print(f"{'排名':<5} {'镜像源':<10} {'URL':<50} {'速度(秒)':<10} {'状态':<10}")
    print("-" * 70)
    
    rank = 1
    fastest_mirror = None
    
    for name, url, elapsed_time, success in results:
        status = "可用" if success else "不可用"
        speed_str = f"{elapsed_time:.2f}" if success else "N/A"
        
        if success and fastest_mirror is None:
            fastest_mirror = (name, url)
        
        print(f"{rank:<5} {name:<10} {url:<50} {speed_str:<10} {status:<10}")
        rank += 1
    
    print("-" * 70)
    
    if fastest_mirror:
        print(f"\n最快的镜像源是: {fastest_mirror[0]} ({fastest_mirror[1]})")
    
    return results

def install_with_mirror(packages, mirror_name=None, mirror_url=None, upgrade=False):
    """使用指定镜像源安装包"""
    if mirror_name and mirror_url:
        print(f"使用 {mirror_name} 安装包...")
    else:
        # 如果未指定镜像源，使用最快的
        print("未指定镜像源，正在测试并选择最快的镜像源...")
        results = test_all_mirrors()
        # 找到第一个可用的镜像源
        available_mirrors = [(name, url) for name, url, _, success in results if success]
        if not available_mirrors:
            print("错误：没有可用的镜像源！")
            return False
        
        mirror_name, mirror_url = available_mirrors[0]
        print(f"使用最快的镜像源: {mirror_name}")
    
    # 构建命令
    cmd = [sys.executable, '-m', 'pip', 'install']
    if upgrade:
        cmd.append('--upgrade')
    
    # 添加镜像源参数
    cmd.extend(['--index-url', mirror_url])
    # 添加trusted-host参数（处理可能的SSL问题）
    host = mirror_url.split('//')[1].split('/')[0]
    cmd.extend(['--trusted-host', host])
    
    # 添加包名
    cmd.extend(packages)
    
    # 执行命令
    print(f"执行命令: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
        print(f"成功使用 {mirror_name} 安装/更新包")
        return True
    except subprocess.CalledProcessError as e:
        print(f"安装失败: {e}")
        return False

def set_default_mirror(mirror_name=None, mirror_url=None):
    """设置默认镜像源"""
    config = load_config()
    
    if mirror_name and mirror_url:
        # 验证镜像源是否在支持列表中
        if mirror_name not in MIRRORS or MIRRORS[mirror_name] != mirror_url:
            print(f"警告: 提供的镜像源 {mirror_name} 不在预定义列表中或URL不匹配")
        
        config["default_mirror"] = {"name": mirror_name, "url": mirror_url}
        save_config(config)
        print(f"已将 {mirror_name} 设置为默认镜像源")
    else:
        # 如果未指定，测试并设置最快的
        print("正在测试并设置最快的镜像源作为默认...")
        results = test_all_mirrors()
        available_mirrors = [(name, url) for name, url, _, success in results if success]
        
        if not available_mirrors:
            print("错误：没有可用的镜像源！")
            return False
        
        mirror_name, mirror_url = available_mirrors[0]
        config["default_mirror"] = {"name": mirror_name, "url": mirror_url}
        save_config(config)
        print(f"已将 {mirror_name} 设置为默认镜像源")
    
    return True

def unset_default_mirror():
    """取消默认镜像源设置"""
    config = load_config()
    if "default_mirror" in config:
        del config["default_mirror"]
        save_config(config)
        print("已取消默认镜像源设置")
    else:
        print("没有设置默认镜像源")

def show_default_mirror():
    """显示当前默认镜像源"""
    config = load_config()
    if "default_mirror" in config and config["default_mirror"]:
        mirror = config["default_mirror"]
        print(f"当前默认镜像源: {mirror['name']} ({mirror['url']})")
    else:
        print("未设置默认镜像源")

def list_mirrors():
    """列出所有支持的镜像源"""
    print("支持的Python镜像源列表:")
    print("-" * 70)
    print(f"{'序号':<5} {'镜像源名称':<10} {'URL':<60}")
    print("-" * 70)
    
    for i, (name, url) in enumerate(MIRRORS.items(), 1):
        print(f"{i:<5} {name:<10} {url:<60}")
    
    print("-" * 70)

def update_all_packages():
    """更新所有已安装的包"""
    config = load_config()
    
    # 获取默认镜像源
    mirror_name = None
    mirror_url = None
    if "default_mirror" in config and config["default_mirror"]:
        mirror_name = config["default_mirror"]["name"]
        mirror_url = config["default_mirror"]["url"]
        print(f"使用默认镜像源: {mirror_name}")
    else:
        # 如果没有默认镜像源，使用最快的
        print("未设置默认镜像源，正在测试并选择最快的镜像源...")
        results = test_all_mirrors()
        available_mirrors = [(name, url) for name, url, _, success in results if success]
        
        if not available_mirrors:
            print("错误：没有可用的镜像源！")
            return False
        
        mirror_name, mirror_url = available_mirrors[0]
        print(f"使用最快的镜像源: {mirror_name}")
    
    # 获取已安装的包列表
    print("获取已安装的包列表...")
    try:
        # 获取可更新的包
        outdated_result = subprocess.run(
            [sys.executable, '-m', 'pip', 'list', '--outdated', '--format=json'],
            check=True,
            capture_output=True,
            text=True
        )
        
        outdated_packages = json.loads(outdated_result.stdout)
        
        if not outdated_packages:
            print("所有包都是最新的，无需更新")
            return True
        
        print(f"发现 {len(outdated_packages)} 个可更新的包:")
        for pkg in outdated_packages:
            print(f"  - {pkg['name']} ({pkg['version']} -> {pkg['latest_version']})")
        
        # 更新所有包
        print(f"\n开始使用 {mirror_name} 更新所有包...")
        
        # 构建更新命令
        cmd = [sys.executable, '-m', 'pip', 'install', '--upgrade', 
               '--index-url', mirror_url, 
               '--trusted-host', mirror_url.split('//')[1].split('/')[0]]
        
        # 添加所有需要更新的包名
        package_names = [pkg['name'] for pkg in outdated_packages]
        cmd.extend(package_names)
        
        print(f"执行命令: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        print("所有包已成功更新")
        return True
        
    except Exception as e:
        print(f"更新包时出错: {e}")
        return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Python包镜像源管理工具')
    
    # 添加子命令
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 测试镜像源速度命令
    test_parser = subparsers.add_parser('test', help='测试所有镜像源速度')
    
    # 安装包命令
    install_parser = subparsers.add_parser('install', help='使用镜像源安装包')
    install_parser.add_argument('packages', nargs='+', help='要安装的包名')
    install_parser.add_argument('--mirror', '-m', choices=MIRRORS.keys(), help='指定镜像源')
    install_parser.add_argument('--upgrade', '-u', action='store_true', help='升级已安装的包')
    
    # 设置默认镜像源命令
    set_default_parser = subparsers.add_parser('set-default', help='设置默认镜像源')
    set_default_parser.add_argument('--mirror', '-m', choices=MIRRORS.keys(), help='指定镜像源')
    
    # 取消默认镜像源命令
    unset_default_parser = subparsers.add_parser('unset-default', help='取消默认镜像源设置')
    
    # 显示默认镜像源命令
    show_default_parser = subparsers.add_parser('show-default', help='显示当前默认镜像源')
    
    # 列出所有镜像源命令
    list_parser = subparsers.add_parser('list', help='列出所有支持的镜像源')
    
    # 更新所有包命令
    update_parser = subparsers.add_parser('update-all', help='更新所有已安装的包')
    
    # 解析参数
    args = parser.parse_args()
    
    # 处理不同的命令
    if args.command == 'test':
        test_all_mirrors()
    
    elif args.command == 'install':
        mirror_name = None
        mirror_url = None
        
        if args.mirror:
            mirror_name = args.mirror
            mirror_url = MIRRORS[mirror_name]
        else:
            # 检查是否有默认镜像源
            config = load_config()
            if "default_mirror" in config and config["default_mirror"]:
                mirror_name = config["default_mirror"]["name"]
                mirror_url = config["default_mirror"]["url"]
        
        install_with_mirror(args.packages, mirror_name, mirror_url, args.upgrade)
    
    elif args.command == 'set-default':
        if args.mirror:
            set_default_mirror(args.mirror, MIRRORS[args.mirror])
        else:
            set_default_mirror()
    
    elif args.command == 'unset-default':
        unset_default_mirror()
    
    elif args.command == 'show-default':
        show_default_mirror()
    
    elif args.command == 'list':
        list_mirrors()
    
    elif args.command == 'update-all':
        update_all_packages()
    
    else:
        # 如果没有指定命令，显示帮助信息
        print("Python包镜像源管理工具\n")
        print("使用方法:")
        print("  python pypi_mirror_manager.py <command> [options]\n")
        print("可用命令:")
        print("  test             测试所有镜像源的速度")
        print("  list             列出所有支持的镜像源")
        print("  install <pkg>... 使用镜像源安装包")
        print("  update-all       更新所有已安装的包")
        print("  set-default      设置默认镜像源")
        print("  unset-default    取消默认镜像源设置")
        print("  show-default     显示当前默认镜像源")
        print("\n使用 'python pypi_mirror_manager.py <command> -h' 查看具体命令的帮助")

if __name__ == "__main__":
    main()