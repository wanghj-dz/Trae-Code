#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
from datetime import datetime

# 导入FreeCAD相关模块
import FreeCAD
import FreeCADGui
import Part
from FreeCAD import Base
print(f"FreeCAD版本: {FreeCAD.Version()}")

# 获取参数（优先从环境变量，然后是命令行参数）
def get_param(name, default, param_type=str):
    # 从环境变量获取
    env_value = os.environ.get(f"FC_{name.upper()}")
    if env_value is not None:
        try:
            return param_type(env_value)
        except ValueError:
            print(f"警告: 环境变量FC_{name.upper()}值 '{env_value}' 转换为{param_type.__name__}失败，使用默认值 {default}")
    
    # 从命令行参数获取（简单实现，实际项目可能需要更复杂的解析）
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg.startswith(f"--{name}="):
            try:
                return param_type(arg.split("=", 1)[1])
            except ValueError:
                print(f"警告: 参数--{name}值无效，使用默认值 {default}")
    
    return default

# 设置默认参数
length = get_param("length", 10.0, float)
width = get_param("width", 10.0, float)
height = get_param("height", 10.0, float)
cube_name = get_param("name", "MyCube", str)

# 获取位置参数
pos_str = get_param("pos", "0,0,0", str)
try:
    pos = tuple(map(float, pos_str.split(",")))
    if len(pos) != 3:
        raise ValueError
    print(f"立方体位置: {pos}")
except ValueError:
    print(f"警告: 位置参数格式无效 '{pos_str}'，使用默认位置 (0,0,0)")
    pos = (0, 0, 0)

# 获取旋转参数
rot_str = get_param("rot", "0,0,0", str)
try:
    rot = tuple(map(float, rot_str.split(",")))
    if len(rot) != 3:
        raise ValueError
    print(f"立方体旋转: {rot}")
except ValueError:
    print(f"警告: 旋转参数格式无效 '{rot_str}'，使用默认旋转 (0,0,0)")
    rot = (0, 0, 0)

# 获取孔洞参数
hole_radius = get_param("holeRadius", 0.0, float)
hole_axis = get_param("holeAxis", "Z", str).upper()

# 生成默认文件名
fcstd_path = get_param("fcstd", None, str)
if fcstd_path is None:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 默认保存到FCStds文件夹
    fcstd_path = os.path.join("FCStds", f"cube_{timestamp}.FCStd")
    # 确保文件夹存在
    os.makedirs("FCStds", exist_ok=True)

# 获取STL导出路径
stl_path = get_param("stl", None, str)
# 确保stls文件夹存在
os.makedirs("stls", exist_ok=True)

# 创建文档
doc_name = "CubeDocument"
doc = FreeCAD.newDocument(doc_name)

# 创建立方体
print(f"创建 {length}x{width}x{height} mm 的立方体...")
cube = Part.makeBox(length, width, height)

# 应用位置偏移
if pos != (0, 0, 0):
    print(f"移动立方体到位置 {pos}...")
    cube.Placement.Base = Base.Vector(pos[0], pos[1], pos[2])

# 应用旋转
if rot != (0, 0, 0):
    print(f"旋转立方体 {rot} 度...")
    # 依次绕X、Y、Z轴旋转
    cube.Placement.Rotation = Base.Rotation(rot[0], rot[1], rot[2])

# 创建Part.Shape对象并添加到文档
obj = doc.addObject("Part::Feature", cube_name)
obj.Shape = cube

# 如果需要打洞
if hole_radius > 0:
    print(f"在立方体中心沿{hole_axis}轴打半径为{hole_radius}mm的贯通孔...")
    
    # 计算圆柱体的长度和位置，确保它贯穿整个立方体
    if hole_axis == "X":
        cyl_length = length + 2  # 稍微长一点，确保贯通
        cyl_center = Base.Vector(pos[0], pos[1], pos[2])
        cylinder = Part.makeCylinder(hole_radius, cyl_length, 
                                   Base.Vector(cyl_center.x - cyl_length/2, cyl_center.y, cyl_center.z),
                                   Base.Vector(1, 0, 0))
    elif hole_axis == "Y":
        cyl_length = width + 2
        cyl_center = Base.Vector(pos[0], pos[1], pos[2])
        cylinder = Part.makeCylinder(hole_radius, cyl_length, 
                                   Base.Vector(cyl_center.x, cyl_center.y - cyl_length/2, cyl_center.z),
                                   Base.Vector(0, 1, 0))
    else:  # Z轴
        cyl_length = height + 2
        cyl_center = Base.Vector(pos[0], pos[1], pos[2])
        cylinder = Part.makeCylinder(hole_radius, cyl_length, 
                                   Base.Vector(cyl_center.x, cyl_center.y, cyl_center.z - cyl_length/2),
                                   Base.Vector(0, 0, 1))
    
    # 创建圆柱体对象
    hole_obj = doc.addObject("Part::Feature", "Hole")
    hole_obj.Shape = cylinder
    
    # 执行布尔运算（差集）
    result = doc.addObject("Part::Cut", "Body")
    result.Base = obj
    result.Tool = hole_obj
    
    # 隐藏原始对象
    obj.Visibility = False
    hole_obj.Visibility = False

# 更新文档
doc.recompute()

# 保存文件
print(f"保存文件到 {fcstd_path}...")
doc.saveAs(fcstd_path)

# 导出STL
if stl_path:
    # 确保STL文件的目录存在
    stl_dir = os.path.dirname(stl_path)
    if stl_dir and not os.path.exists(stl_dir):
        os.makedirs(stl_dir, exist_ok=True)
        print(f"创建STL输出目录: {stl_dir}")
    try:
        # 导出为STL文件
        # 使用FreeCAD的Mesh和MeshPart模块
        import Mesh
        import MeshPart
        
        # 创建网格
        if hole_radius > 0:
            mesh = MeshPart.meshFromShape(
                Shape=result.Shape,
                LinearDeflection=0.1,
                AngularDeflection=0.05,
                Relative=True
            )
        else:
            mesh = MeshPart.meshFromShape(
                Shape=obj.Shape,
                LinearDeflection=0.1,
                AngularDeflection=0.05,
                Relative=True
            )
        
        # 导出STL文件
        mesh.write(stl_path)
        print(f"✓ STL文件已导出到: {stl_path}")
    except ImportError:
        print("错误: 无法导入Mesh或MeshPart模块，无法导出STL文件")
    except Exception as e:
        print(f"✗ STL导出失败: {str(e)}")

# 完成
print(f"\n立方体创建完成！")
print(f"- FCStd文件: {fcstd_path}")
if stl_path:
    print(f"- STL文件: {stl_path}")
print("\n您可以使用FreeCAD打开.FCStd文件查看模型")

# 如果在非交互模式下，关闭文档
if not hasattr(FreeCADGui, 'ActiveDocument') or not FreeCADGui.ActiveDocument:
    FreeCAD.closeDocument(doc.Name)

print("脚本执行完毕")