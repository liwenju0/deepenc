#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hexie_auth 动态加载器

专门用于动态加载 hexie_auth.so 文件，避免循环导入问题。
遵循 Linux 内核的模块加载设计原则。
"""

import importlib.util
import sys
from pathlib import Path


def load_hexie_auth():
    """动态加载 hexie_auth 模块

    支持多种 Python 版本的 SO 文件。
    采用延迟加载策略，避免循环导入。

    Returns:
        module: 加载成功的 hexie_auth 模块，失败返回 None
    """
    try:
        # 获取当前 Python 版本信息
        python_major = sys.version_info.major
        python_minor = sys.version_info.minor
        python_version = f"{python_major}{python_minor}"

        # 只允许 38 到 313 之间的 Python 版本
        allowed_versions = [f"{i}" for i in range(38, 314)]
        if python_version not in allowed_versions:
            print(
                f"❌ hexie auth 不支持的 Python 版本: {python_major}.{python_minor} (仅支持 3.8 ~ 3.13)"
            )
            return None

        # 构建可能的 SO 文件路径
        current_dir = Path(__file__).parent
        so_files = [
            current_dir / f"hexie_auth.cpython-{python_version}-x86_64-linux-gnu.so",
            current_dir / f"hexie_auth.cpython-{python_version}-linux-gnu.so",
            current_dir / "hexie_auth.so",
        ]
        # 查找可用的 SO 文件
        so_file = None
        for file_path in so_files:
            if file_path.exists():
                so_file = file_path
                break

        # 如果没有找到精确匹配的版本，尝试查找所有可用的 SO 文件
        if not so_file:
            print(f"🔍 未找到精确匹配 Python {python_version} 的 SO 文件，搜索所有可用文件...")
            for file_path in current_dir.glob("hexie_auth.cpython-*.so"):
                print(f"  发现: {file_path.name}")
                # 选择第一个可用的文件
                so_file = file_path
                break

        if not so_file:
            print(f"❌ 未找到任何可用的 hexie_auth.so 文件")
            return None

        print(f"🔍 选择 SO 文件: {so_file}")

        # 动态加载 SO 文件
        spec = importlib.util.spec_from_file_location("hexie_auth", so_file)
        if not spec:
            print("❌ 无法创建模块规格")
            return None

        # 创建并执行模块
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        print("✅ 成功动态加载 hexie_auth 模块")
        return module

    except Exception as e:
        import traceback

        print(f"❌ 动态加载 hexie_auth 失败: {e}")
        print(f"详细错误信息: {traceback.format_exc()}")
        return None


def get_auth_class():
    """获取 Auth 类

    Returns:
        class: Auth 类，失败返回 None
    """
    try:
        module = load_hexie_auth()
        if module and hasattr(module, "Auth"):
            return module.Auth
        else:
            print("❌ hexie_auth 模块中未找到 Auth 类")
            return None
    except Exception as e:
        print(f"❌ 获取 Auth 类失败: {e}")
        return None


# 导出主要接口
__all__ = ["load_hexie_auth", "get_auth_class"]
