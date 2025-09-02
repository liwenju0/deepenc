#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基本使用示例

演示框架的基本使用方法。
"""

import os
import sys
from pathlib import Path

# 添加框架路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import encrypt


def example_basic_usage():
    """基本使用示例"""
    print("🚀 基本使用示例")
    
    # 1. 启动加密系统
    system = encrypt.bootstrap()
    
    # 2. 获取系统状态
    status = system.get_status()
    print(f"系统状态: {status}")
    
    # 3. 正常导入模块（系统会自动处理加密/解密）
    try:
        # 这里的导入会被系统自动处理
        # 如果模块已加密，会自动解密
        # 如果模块未加密，会正常导入
        print("尝试导入模块...")
        # from src import main  # 取消注释来测试
        print("✅ 模块导入成功")
    except ImportError as e:
        print(f"⚠️ 模块导入失败: {e}")
    
    # 4. 清理系统
    system.shutdown()


def example_build_project():
    """项目构建示例"""
    print("🔨 项目构建示例")
    
    from encrypt.builders import ProjectBuilder
    
    # 创建构建器
    builder = ProjectBuilder()
    
    # 构建项目
    try:
        report = builder.build_project()
        print("✅ 构建成功")
        print(f"加密模块数: {report['encryption']['encrypted_python_modules']}")
        print(f"加密模型数: {report['encryption']['encrypted_onnx_models']}")
    except Exception as e:
        print(f"❌ 构建失败: {e}")


def example_file_discovery():
    """文件发现示例"""
    print("🔍 文件发现示例")
    
    from encrypt.discovery import FileScanner
    
    # 创建扫描器
    scanner = FileScanner()
    
    # 发现文件
    try:
        result = scanner.discover_all_files()
        print(f"发现 Python 文件: {len(result['python_files'])} 个")
        print(f"发现 ONNX 文件: {len(result['onnx_files'])} 个")
        
        # 显示前几个文件
        if result['python_files']:
            print("\nPython 文件示例:")
            for i, file_info in enumerate(result['python_files'][:3]):
                print(f"  {i+1}. {file_info['module_name']}")
        
    except Exception as e:
        print(f"❌ 文件发现失败: {e}")


if __name__ == '__main__':
    print("🎯 Python 项目加密分发框架示例")
    print("=" * 50)
    
    try:
        example_basic_usage()
        print()
        example_file_discovery()
        print()
        example_build_project()
        
    except KeyboardInterrupt:
        print("\n⚠️ 示例被用户中断")
    except Exception as e:
        print(f"\n❌ 示例运行失败: {e}")
        import traceback
        traceback.print_exc()
