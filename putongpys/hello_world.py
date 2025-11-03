#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Hello World Python示例程序
这是一个简单的示例，演示如何打印Hello World
"""

# 打印Hello World消息
print("Hello, World!")

# 可选：添加一些额外的功能
def greet(name="World"):
    """向指定名称的人或默认的World打招呼"""
    return f"Hello, {name}!"

# 调用函数并打印结果
if __name__ == "__main__":
    print(greet())  # 打印默认问候
    print(greet("Python"))  # 打印自定义问候