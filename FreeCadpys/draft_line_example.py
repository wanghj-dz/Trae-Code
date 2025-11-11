"""FreeCAD Draft 工作台：直线 (Line) 使用示例

说明：
- 这个脚本演示如何在 FreeCAD 中使用 Draft 工作台创建一条直线（Draft.makeLine）。
- 可在 FreeCAD 的命令行环境运行（使用 freecadcmd.exe），也可以在 FreeCAD GUI 的 Python 控制台中运行。

示例（PowerShell）：
& 'C:/Users/admin/scoop/apps/freecad/current/bin/freecadcmd.exe' './FreeCadpys/draft_line_example.py' --x1 0 --y1 0 --z1 0 --x2 50 --y2 0 --z2 0 --name "MyLine" --fcstd "FCStds/myline.FCStd"

特点：
- 支持命令行参数：起点/终点坐标、标签名、是否保存 .FCStd
- 如果运行在无 GUI 的 freecadcmd 环境，会自动跳过任何 GUI 操作

注意：导出 STL/实体格式对单纯的线段没有意义（线不是体），脚本只演示创建与保存文档。
"""

from __future__ import annotations
import sys
import os
import argparse

# 早期调试：记录启动与 argv 到工作区日志，便于在 freecadcmd 环境下排查启动错误
try:
    dbg_path = os.path.join(os.path.dirname(__file__), 'draft_line_debug.txt')
    with open(dbg_path, 'w', encoding='utf-8') as _dbg:
        _dbg.write('script started\n')
        _dbg.write('argv: ' + ' '.join(sys.argv) + '\n')
except Exception:
    # 忽略任何日志写入错误，继续执行
    pass

try:
    import FreeCAD
    from FreeCAD import Vector
except Exception as e:
    raise SystemExit("这个脚本需要在 FreeCAD 的 Python 环境中运行（例如 freecadcmd）。错误: {}".format(e))

try:
    # Draft 可能在某些 FreeCAD 安装中位于 Draft 或者 FreeCADGui 环境下
    import Draft
except Exception:
    Draft = None


def create_line(doc, p1, p2, name: str = "DraftLine"):
    """在文档中创建一条 Draft 直线并返回对象

    Args:
        doc: FreeCAD 文档对象
        p1, p2: FreeCAD.Vector 起点与终点
        name: 对象标签

    Returns:
        新创建的对象
    """
    if Draft is None:
        raise RuntimeError("Draft 模块不可用 — 请确保在包含 Draft 工作台的 FreeCAD 环境中运行")

    line_obj = Draft.makeLine(p1, p2)
    # 设置更友好的标签
    try:
        line_obj.Label = name
    except Exception:
        pass
    return line_obj


def parse_args(argv):
    p = argparse.ArgumentParser(description="FreeCAD Draft 直线示例脚本")
    p.add_argument('--x1', type=float, default=0.0, help='起点 X')
    p.add_argument('--y1', type=float, default=0.0, help='起点 Y')
    p.add_argument('--z1', type=float, default=0.0, help='起点 Z')
    p.add_argument('--x2', type=float, default=10.0, help='终点 X')
    p.add_argument('--y2', type=float, default=0.0, help='终点 Y')
    p.add_argument('--z2', type=float, default=0.0, help='终点 Z')
    p.add_argument('--name', type=str, default='DraftLine', help='对象标签名')
    p.add_argument('--fcstd', type=str, default=None, help='如果指定则保存为 .FCStd 路径')
    # 使用 parse_known_args 避免因 freecadcmd 转发带来的未知参数导致 SystemExit
    known, unknown = p.parse_known_args(argv)
    try:
        with open(os.path.join(os.path.dirname(__file__), 'draft_line_debug.txt'), 'a', encoding='utf-8') as _dbg:
            _dbg.write('unknown argv: ' + str(unknown) + '\n')
    except Exception:
        pass
    return known


def robust_override_from_raw(argv, args):
    """如果标准 argparse 没解析到（或被 freecadcmd 换行/引号破坏），尝试从原始 argv 字符串中用正则提取参数并覆盖 args。"""
    import re
    raw = ' '.join(argv)
    # 允许两种格式 --x1 10 或 --x1=10
    def _get_float(name, cur):
        m = re.search(rf"(?:--{name})\s*=?\s*([+-]?\d+(?:\.\d+)?)", raw)
        if m:
            try:
                return float(m.group(1))
            except Exception:
                return cur
        return cur

    def _get_str(name, cur):
        m = re.search(rf"(?:--{name})\s*=?\s*\"([^\"]+)\"|(?:--{name})\s*=?\s*'([^']+)'|(?:--{name})\s*=?\s*([^\s]+)", raw)
        if m:
            for g in m.groups():
                if g:
                    return g
        return cur

    # 尝试覆盖
    args.x1 = _get_float('x1', args.x1)
    args.y1 = _get_float('y1', args.y1)
    args.z1 = _get_float('z1', args.z1)
    args.x2 = _get_float('x2', args.x2)
    args.y2 = _get_float('y2', args.y2)
    args.z2 = _get_float('z2', args.z2)
    args.name = _get_str('name', args.name)
    args.fcstd = _get_str('fcstd', args.fcstd)
    # 返回可能被覆盖的 args
    return args


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])

    # 记录解析到的参数到调试文件
    try:
        with open(os.path.join(os.path.dirname(__file__), 'draft_line_debug.txt'), 'a', encoding='utf-8') as _dbg:
            _dbg.write('parsed args: ' + str(args) + '\n')
    except Exception:
        pass

    # 如果解析后的参数仍然是默认值（可能因为 freecadcmd 转发问题），尝试从原始 sys.argv 字符串用正则提取
    try:
        # 仅在检测到明显没有传参时才做原始解析
        no_user_params = (('--x1' not in ' '.join(sys.argv)) and ('--x2' not in ' '.join(sys.argv)))
        if no_user_params:
            args = robust_override_from_raw(sys.argv, args)
            try:
                with open(os.path.join(os.path.dirname(__file__), 'draft_line_debug.txt'), 'a', encoding='utf-8') as _dbg:
                    _dbg.write('after raw-override args: ' + str(args) + '\n')
            except Exception:
                pass
    except Exception:
        pass

    # 如果 freecadcmd 的参数传递被破坏，尝试从环境变量读取备用参数（以 FC_ 前缀）
    try:
        env = os.environ
        def _envf(name, cast, default):
            v = env.get('FC_' + name.upper())
            if v is None:
                return default
            try:
                return cast(v)
            except Exception:
                return default

        # 仅在用户未显式传参（等于默认值）时使用环境变量覆盖
        if (args.x1 == 0.0 and args.y1 == 0.0 and args.z1 == 0.0 and
            args.x2 == 10.0 and args.y2 == 0.0 and args.z2 == 0.0):
            args.x1 = _envf('length', float, args.x1)
            args.y1 = _envf('width', float, args.y1)
            args.z1 = _envf('height', float, args.z1)
            # 终点使用 length 为 X2，保持简单映射（若需要更复杂映射可扩展）
            args.x2 = _envf('length', float, args.x2)

        # 也允许直接设置 LABEL 和 FCSTD 路径
        name_env = os.environ.get('FC_NAME')
        if name_env and args.name == 'DraftLine':
            args.name = name_env
        fcstd_env = os.environ.get('FC_FCSTD')
        if fcstd_env and args.fcstd is None:
            args.fcstd = fcstd_env
        # 记录可能的环境覆盖
        try:
            with open(os.path.join(os.path.dirname(__file__), 'draft_line_debug.txt'), 'a', encoding='utf-8') as _dbg:
                _dbg.write('after env override args: ' + str(args) + '\n')
        except Exception:
            pass
    except Exception:
        pass

    # 新建或使用已有文档
    doc = None
    if FreeCAD.ActiveDocument is None:
        doc = FreeCAD.newDocument('DraftLineDoc')
    else:
        doc = FreeCAD.ActiveDocument

    p1 = Vector(args.x1, args.y1, args.z1)
    p2 = Vector(args.x2, args.y2, args.z2)

    line = create_line(doc, p1, p2, name=args.name)

    try:
        with open(os.path.join(os.path.dirname(__file__), 'draft_line_debug.txt'), 'a', encoding='utf-8') as _dbg:
            _dbg.write(f'created: {getattr(line, "Label", None)}\n')
    except Exception:
        pass

    # 有些 FreeCAD 环境需要显式 recompute
    try:
        doc.recompute()
    except Exception:
        pass

    print(f"Created line '{line.Label}' from {p1} to {p2}")

    if args.fcstd:
        outdir = os.path.dirname(args.fcstd)
        if outdir and not os.path.exists(outdir):
            try:
                os.makedirs(outdir, exist_ok=True)
            except Exception as e:
                print(f"无法创建目录 {outdir}: {e}")
        try:
            # 保存文档
            doc.saveAs(args.fcstd)
            try:
                with open(os.path.join(os.path.dirname(__file__), 'draft_line_debug.txt'), 'a', encoding='utf-8') as _dbg:
                    _dbg.write(f'saved to: {args.fcstd}\n')
            except Exception:
                pass
            print(f"Saved document to {args.fcstd}")
        except Exception as e:
            try:
                with open(os.path.join(os.path.dirname(__file__), 'draft_line_debug.txt'), 'a', encoding='utf-8') as _dbg:
                    _dbg.write('save error: ' + str(e) + '\n')
            except Exception:
                pass
            print(f"保存 FCStd 失败: {e}")


if __name__ == '__main__':
    try:
        main()
    except Exception:
        # 在 freecadcmd 下有时堆栈不会完整显示，显式打印 traceback 以便调试
        import traceback
        traceback.print_exc()
        sys.exit(1)
