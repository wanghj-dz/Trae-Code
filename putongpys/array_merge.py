#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import numpy as np

"""
数组（列表）合并工具

这个程序演示了Python中不同的数组合并方法，并提供了一些实用的合并功能，
同时展示了math模块和numpy库的使用。
"""


def basic_merge(arr1, arr2):
    """
    基本合并方法 - 使用+运算符
    
    Args:
        arr1: 第一个数组
        arr2: 第二个数组
    
    Returns:
        合并后的新数组
    """
    return arr1 + arr2


def numpy_merge(arr1, arr2):
    """
    使用numpy合并数组
    
    Args:
        arr1: 第一个数组
        arr2: 第二个数组
    
    Returns:
        numpy数组格式的合并结果
    """
    # 将Python列表转换为numpy数组
    np_arr1 = np.array(arr1)
    np_arr2 = np.array(arr2)
    
    # 使用numpy的concatenate函数合并数组
    result = np.concatenate((np_arr1, np_arr2))
    
    return result


def extend_merge(arr1, arr2):
    """
    使用extend方法合并数组
    
    Args:
        arr1: 第一个数组（将被修改）
        arr2: 第二个数组
    
    Returns:
        合并后的数组（即修改后的arr1）
    """
    result = arr1.copy()  # 创建副本以避免修改原数组
    result.extend(arr2)
    return result


def list_comprehension_merge(arr1, arr2):
    """
    使用列表推导式合并数组
    
    Args:
        arr1: 第一个数组
        arr2: 第二个数组
    
    Returns:
        合并后的新数组
    """
    return [item for sublist in [arr1, arr2] for item in sublist]


def merge_without_duplicates(arr1, arr2):
    """
    合并数组并移除重复元素
    
    Args:
        arr1: 第一个数组
        arr2: 第二个数组
    
    Returns:
        去重后的合并数组
    """
    # 使用集合去重，但会丢失原始顺序
    # return list(set(arr1 + arr2))
    
    # 保持原始顺序的去重方法
    result = []
    seen = set()
    for item in arr1 + arr2:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def merge_and_sort(arr1, arr2):
    """
    合并数组并排序
    
    Args:
        arr1: 第一个数组
        arr2: 第二个数组
    
    Returns:
        合并并排序后的数组
    """
    return sorted(arr1 + arr2)


def merge_arrays_demo():
    """
    演示各种数组合并方法
    """
    print("数组（列表）合并演示程序")
    print("=" * 50)
    print(f"使用math模块计算示例: π = {math.pi:.4f}, e = {math.e:.4f}")
    print()
    
    # 示例数组
    array1 = [1, 2, 3, 4, 5]
    array2 = [4, 5, 6, 7, 8]
    
    # 使用numpy创建相同的数组
    np_array1 = np.array(array1)
    np_array2 = np.array(array2)
    
    print(f"原始数组1: {array1}")
    print(f"原始数组2: {array2}")
    print()
    
    # 方法1: 基本合并
    result1 = basic_merge(array1, array2)
    print(f"方法1 - 使用+运算符合并: {result1}")
    
    # 方法2: 使用extend方法
    result2 = extend_merge(array1, array2)
    print(f"方法2 - 使用extend方法合并: {result2}")
    
    # 方法3: 使用列表推导式
    result3 = list_comprehension_merge(array1, array2)
    print(f"方法3 - 使用列表推导式合并: {result3}")
    
    # 方法4: 合并并去重
    result4 = merge_without_duplicates(array1, array2)
    print(f"方法4 - 合并并去重: {result4}")
    
    # 方法5: 合并并排序
    result5 = merge_and_sort(array1, array2)
    print(f"方法5 - 合并并排序: {result5}")
    
    # 方法6: 使用numpy合并
    try:
        result6 = numpy_merge(array1, array2)
        print(f"方法6 - 使用numpy合并: {result6}")
        print(f"numpy数组形状: {result6.shape}, 数据类型: {result6.dtype}")
    except ImportError:
        print("方法6 - numpy不可用，请安装numpy库")
    except Exception as e:
        print(f"numpy合并出错: {e}")
    
    # 确保原数组未被修改
    print()
    print(f"确认原数组未被修改:")
    print(f"数组1: {array1}")
    print(f"数组2: {array2}")
    
    # 演示使用数学运算合并数组
    print()
    print("使用数学运算合并数组（使用前5个元素）:")
    try:
        short_arr1 = array1[:5]
        short_arr2 = array2[:5]
        
        print(f"数组1前5个元素: {short_arr1}")
        print(f"数组2前5个元素: {short_arr2}")
        print(f"加法结果: {merge_with_math_operation(short_arr1, short_arr2, 'add')}")
        print(f"乘法结果: {merge_with_math_operation(short_arr1, short_arr2, 'multiply')}")
        print(f"幂运算结果: {merge_with_math_operation(short_arr1, short_arr2, 'pow')}")
        print(f"乘积平方根: {merge_with_math_operation(short_arr1, short_arr2, 'sqrt_product')}")
        
        # 使用numpy进行数组运算
        print("\n使用numpy进行数组运算:")
        try:
            np_add = numpy_array_operations(short_arr1, short_arr2, 'add')
            np_multiply = numpy_array_operations(short_arr1, short_arr2, 'multiply')
            np_dot = numpy_array_operations(short_arr1, short_arr2, 'dot')
            
            print(f"numpy加法: {np_add}")
            print(f"numpy乘法: {np_multiply}")
            print(f"numpy点积: {np_dot}")
        except Exception as e:
            print(f"numpy运算出错: {e}")
            
    except Exception as e:
        print(f"数学运算合并出错: {e}")


def advanced_merge(arrays):
    """
    合并多个数组
    
    Args:
        arrays: 数组的数组
    
    Returns:
        合并后的新数组
    """
    result = []
    for arr in arrays:
        result.extend(arr)
    return result


def merge_with_math_operation(arr1, arr2, operation='add'):
    """
    使用数学运算合并两个等长数组
    
    Args:
        arr1: 第一个数组
        arr2: 第二个数组
        operation: 数学运算类型 ('add', 'subtract', 'multiply', 'divide', 'pow')
    
    Returns:
        包含运算结果的新数组
    """
    if len(arr1) != len(arr2):
        raise ValueError("两个数组必须具有相同的长度")
    
    result = []
    for a, b in zip(arr1, arr2):
        if operation == 'add':
            result.append(a + b)
        elif operation == 'subtract':
            result.append(a - b)
        elif operation == 'multiply':
            result.append(a * b)
        elif operation == 'divide':
            result.append(a / b if b != 0 else float('inf'))
        elif operation == 'pow':
            result.append(math.pow(a, b))
        elif operation == 'sqrt_product':
            result.append(math.sqrt(abs(a * b)))
        else:
            raise ValueError(f"不支持的运算类型: {operation}")
    
    return result


def numpy_array_operations(arr1, arr2, operation='add'):
    """
    使用numpy进行数组运算
    
    Args:
        arr1: 第一个数组
        arr2: 第二个数组
        operation: 数学运算类型 ('add', 'subtract', 'multiply', 'divide', 'dot')
    
    Returns:
        numpy数组格式的运算结果
    """
    # 将Python列表转换为numpy数组
    np_arr1 = np.array(arr1)
    np_arr2 = np.array(arr2)
    
    # 执行numpy数组运算
    if operation == 'add':
        result = np_arr1 + np_arr2
    elif operation == 'subtract':
        result = np_arr1 - np_arr2
    elif operation == 'multiply':
        result = np_arr1 * np_arr2  # 元素级乘法
    elif operation == 'divide':
        result = np.divide(np_arr1, np_arr2, out=np.zeros_like(np_arr1, dtype=float), where=np_arr2!=0)
    elif operation == 'dot':
        # 确保数组可以进行点积运算
        if len(np_arr1) == len(np_arr2):
            result = np.dot(np_arr1, np_arr2)
        else:
            raise ValueError("进行点积运算需要数组长度相同")
    else:
        raise ValueError(f"不支持的numpy运算类型: {operation}")
    
    return result


def numpy_statistics(arr):
    """
    使用numpy计算数组统计信息
    
    Args:
        arr: 输入数组
    
    Returns:
        包含统计信息的字典
    """
    np_arr = np.array(arr)
    
    stats = {
        'length': len(np_arr),
        'mean': np.mean(np_arr),
        'median': np.median(np_arr),
        'std': np.std(np_arr),
        'var': np.var(np_arr),
        'min': np.min(np_arr),
        'max': np.max(np_arr),
        'sum': np.sum(np_arr),
        'cumsum': np.cumsum(np_arr)  # 累积和
    }
    
    return stats


if __name__ == "__main__":
    # 运行演示
    merge_arrays_demo()
    
    # 额外演示 - 合并多个数组
    print("\n" + "=" * 50)
    print("额外演示: 合并多个数组")
    multiple_arrays = [[1, 2], [3, 4], [5, 6], [7, 8]]
    result = advanced_merge(multiple_arrays)
    print(f"多个数组: {multiple_arrays}")
    print(f"合并结果: {result}")
    
    # 用户交互部分
    print("\n" + "=" * 50)
    print("交互式数组合并")
    try:
        # 获取用户输入的两个数组
        input1 = input("请输入第一个数组的元素（用逗号分隔）: ")
        input2 = input("请输入第二个数组的元素（用逗号分隔）: ")
        
        # 转换为数字列表
        user_array1 = [int(x.strip()) for x in input1.split(',')]
        user_array2 = [int(x.strip()) for x in input2.split(',')]
        
        # 执行所有合并方法
        print(f"\n您的数组1: {user_array1}")
        print(f"您的数组2: {user_array2}")
        print(f"\n合并结果:")
        print(f"基本合并: {basic_merge(user_array1, user_array2)}")
        print(f"去重合并: {merge_without_duplicates(user_array1, user_array2)}")
        print(f"排序合并: {merge_and_sort(user_array1, user_array2)}")
        
    except ValueError:
        print("输入格式错误，请确保输入的是逗号分隔的数字。")
    except Exception as e:
        print(f"发生错误: {e}")
    
    # 数学统计功能演示
    print("\n" + "=" * 50)
    print("数组数学统计")
    try:
        # 计算合并数组的统计信息
        merged_array = basic_merge(user_array1, user_array2)
        
        print(f"合并数组: {merged_array}")
        print(f"数组长度: {len(merged_array)}")
        print(f"最大值: {max(merged_array)}")
        print(f"最小值: {min(merged_array)}")
        print(f"平均值: {sum(merged_array) / len(merged_array):.2f}")
        
        # 使用math模块计算标准差
        mean = sum(merged_array) / len(merged_array)
        variance = sum((x - mean) ** 2 for x in merged_array) / len(merged_array)
        std_dev = math.sqrt(variance)
        print(f"标准差(常规计算): {std_dev:.4f}")
        
        # 使用numpy进行统计分析
        print("\n使用numpy进行统计分析:")
        try:
            np_stats = numpy_statistics(merged_array)
            print(f"numpy平均值: {np_stats['mean']:.4f}")
            print(f"numpy中位数: {np_stats['median']:.4f}")
            print(f"numpy标准差: {np_stats['std']:.4f}")
            print(f"numpy方差: {np_stats['var']:.4f}")
            print(f"numpy总和: {np_stats['sum']}")
            print(f"numpy累积和: {np_stats['cumsum']}")
            
            # 创建numpy数组并展示更多功能
            np_merged = np.array(merged_array)
            print(f"\nnumpy数组形状: {np_merged.shape}")
            print(f"numpy数组维度: {np_merged.ndim}")
            print(f"numpy数组元素类型: {np_merged.dtype}")
            print(f"numpy数组描述性统计:\n{np.around(np_merged, decimals=2)}")
            
        except Exception as e:
            print(f"numpy统计分析出错: {e}")
            
    except Exception as e:
        print(f"统计计算出错: {e}")
    
    print("\n程序执行完毕！")