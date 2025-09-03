#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI 命令实现

实现所有命令行工具的功能。
遵循 Linux 命令行工具的设计风格。
"""

import os
import sys
import json
from pathlib import Path
from ..builders.project_builder import ProjectBuilder
from ..discovery.scanner import FileScanner
from ..bootstrap import initialize, get_system
from ..core.errors import BuildError, FileDiscoveryError


class EncryptCLI:
    """加密框架 CLI 实现
    
    提供完整的命令行接口。
    """
    
    def __init__(self):
        """初始化 CLI"""
        self.project_root = Path.cwd()
    
    def build(self, project_path=None, output_dir=None, entry_point=None, clean=True, verbose=False):
        """构建加密项目
        
        Args:
            project_path: 项目路径，默认当前目录
            output_dir: 输出目录，默认 project_path/build
            entry_point: 项目入口Python文件，默认src/grpc_main.py
            clean: 是否清理构建目录
            verbose: 是否显示详细信息
            
        Returns:
            int: 退出码 (0=成功, 1=失败)
        """
        try:
            project_root = Path(project_path or '.').resolve()
            build_dir = Path(output_dir or project_root / 'build').resolve()
            
            print(f"🔨 构建加密项目")
            print(f"📁 项目路径: {project_root}")
            print(f"🏗️ 输出目录: {build_dir}")
            if entry_point:
                print(f"🚪 项目入口: {entry_point}")
            
            # 创建项目构建器
            builder = ProjectBuilder(project_root, build_dir, entry_point)
            
            # 构建项目
            build_report = builder.build_project(auto_discover=True, clean=clean)
            
            if verbose:
                self._print_verbose_report(build_report)
            
            return 0
            
        except Exception as e:
            print(f"❌ 构建失败: {e}")
            return 1
    
    def scan(self, project_path=None, output_format='table'):
        """扫描项目文件
        
        Args:
            project_path: 项目路径，默认当前目录
            output_format: 输出格式 ('table', 'json', 'simple')
            
        Returns:
            int: 退出码
        """
        try:
            project_root = Path(project_path or '.').resolve()
            
            print(f"🔍 扫描项目文件: {project_root}")
            
            # 创建文件扫描器
            scanner = FileScanner(project_root)
            
            # 发现文件
            discovery_result = scanner.discover_all_files()
            
            # 输出结果
            if output_format == 'json':
                print(json.dumps(discovery_result, indent=2, ensure_ascii=False))
            elif output_format == 'simple':
                self._print_simple_scan_result(discovery_result)
            else:  # table
                self._print_table_scan_result(discovery_result)
            
            return 0
            
        except Exception as e:
            print(f"❌ 扫描失败: {e}")
            return 1
    
    def status(self):
        """显示系统状态
        
        Returns:
            int: 退出码
        """
        try:
            system = get_system()
            
            if system is None:
                print("❌ 加密系统未初始化")
                return 1
            
            status_info = system.get_status()
            self._print_status_info(status_info)
            
            return 0
            
        except Exception as e:
            print(f"❌ 获取状态失败: {e}")
            return 1
    
    def init(self, project_path=None):
        """初始化加密系统
        
        Args:
            project_path: 项目路径，默认当前目录
            
        Returns:
            int: 退出码
        """
        try:
            project_root = Path(project_path or '.').resolve()
            
            print(f"🚀 初始化加密系统: {project_root}")
            
            # 切换到项目目录
            os.chdir(project_root)
            
            # 尝试自动初始化
            from ..bootstrap import auto_initialize
            system = auto_initialize()
            
            if system:
                print("✅ 加密系统初始化成功")
                return 0
            else:
                print("❌ 加密系统初始化失败")
                return 1
            
        except Exception as e:
            print(f"❌ 初始化失败: {e}")
            return 1
    
    def clean(self, project_path=None, build_dir=None):
        """清理构建目录
        
        Args:
            project_path: 项目路径，默认当前目录
            build_dir: 构建目录，默认 project_path/build
            
        Returns:
            int: 退出码
        """
        try:
            project_root = Path(project_path or '.').resolve()
            build_dir = Path(build_dir or project_root / 'build').resolve()
            
            print(f"🧹 清理构建目录: {build_dir}")
            
            # 创建项目构建器
            builder = ProjectBuilder(project_root, build_dir)
            builder.clean_build()
            
            return 0
            
        except Exception as e:
            print(f"❌ 清理失败: {e}")
            return 1
    
    def verify(self, build_dir=None):
        """验证构建结果
        
        Args:
            build_dir: 构建目录，默认当前目录/build
            
        Returns:
            int: 退出码
        """
        try:
            project_root = Path('.').resolve()
            build_dir = Path(build_dir or project_root / 'build').resolve()
            
            print(f"🔍 验证构建结果: {build_dir}")
            
            # 创建项目构建器
            builder = ProjectBuilder(project_root, build_dir)
            
            if builder.verify_build():
                print("✅ 构建验证通过")
                return 0
            else:
                print("❌ 构建验证失败")
                return 1
            
        except Exception as e:
            print(f"❌ 验证失败: {e}")
            return 1
    
    def _print_verbose_report(self, build_report):
        """打印详细构建报告
        
        Args:
            build_report: 构建报告
        """
        print("\n📋 详细构建报告:")
        print("=" * 60)
        
        # 构建信息
        print("🔨 构建信息:")
        print(f"  开始时间: {build_report['build_info']['start_time']}")
        print(f"  结束时间: {build_report['build_info']['end_time']}")
        print(f"  构建时长: {build_report['build_info']['duration_seconds']:.2f} 秒")
        print(f"  构建状态: {'成功' if build_report['build_info']['success'] else '失败'}")
        
        # 文件发现信息
        print("\n🔍 文件发现:")
        print(f"  Python 文件: {build_report['discovery']['total_python_files']} 个")
        print(f"  ONNX 模型: {build_report['discovery']['total_onnx_files']} 个")
        
        # 加密信息
        print("\n🔐 加密结果:")
        print(f"  加密 Python 模块: {build_report['encryption']['encrypted_python_modules']} 个")
        print(f"  加密 ONNX 模型: {build_report['encryption']['encrypted_onnx_models']} 个")
        
        if build_report['encryption']['python_modules']:
            print("\n  Python 模块列表:")
            for module in build_report['encryption']['python_modules']:
                print(f"    - {module}")
        
        if build_report['encryption']['onnx_models']:
            print("\n  ONNX 模型列表:")
            for model in build_report['encryption']['onnx_models']:
                print(f"    - {model}")
        
        # 输出信息
        print("\n📁 输出文件:")
        print(f"  构建目录: {build_report['output']['build_dir']}")
        print(f"  加密目录: {build_report['output']['encrypted_dir']}")
        print(f"  配置文件: {build_report['output']['config_file']}")
        print(f"  启动脚本: {build_report['output']['bootstrap_script']}")
        
        # 授权信息
        print("\n🔑 授权信息:")
        print(f"  授权模式: {build_report['auth_info']['auth_mode']}")
        print(f"  密钥来源: {build_report['auth_info']['key_source']}")
        print(f"  硬件授权: {'可用' if build_report['auth_info']['hardware_auth_available'] else '不可用'}")
        print(f"  授权状态: {'有效' if build_report['auth_info']['authorization_valid'] else '无效'}")
    
    def _print_simple_scan_result(self, discovery_result):
        """打印简单扫描结果
        
        Args:
            discovery_result: 发现结果
        """
        print(f"\nPython 文件 ({len(discovery_result['python_files'])} 个):")
        for file_info in discovery_result['python_files']:
            print(f"  {file_info['module_name']} -> {file_info['relative_path']}")
        
        print(f"\nONNX 模型 ({len(discovery_result['onnx_files'])} 个):")
        for file_info in discovery_result['onnx_files']:
            print(f"  {file_info['model_name']} -> {file_info['relative_path']}")
    
    def _print_table_scan_result(self, discovery_result):
        """打印表格格式扫描结果
        
        Args:
            discovery_result: 发现结果
        """
        print("\n📊 文件扫描结果:")
        print("=" * 80)
        
        # Python 文件表格
        if discovery_result['python_files']:
            print("\n🐍 Python 文件:")
            print(f"{'模块名':<30} {'文件路径':<40} {'大小':<10}")
            print("-" * 80)
            
            for file_info in discovery_result['python_files']:
                size_kb = file_info['file_size'] / 1024
                print(f"{file_info['module_name']:<30} {file_info['relative_path']:<40} {size_kb:.1f}KB")
        
        # ONNX 模型表格
        if discovery_result['onnx_files']:
            print("\n🧠 ONNX 模型:")
            print(f"{'模型名':<30} {'文件路径':<40} {'大小':<10}")
            print("-" * 80)
            
            for file_info in discovery_result['onnx_files']:
                size_mb = file_info['file_size'] / (1024 * 1024)
                print(f"{file_info['model_name']:<30} {file_info['relative_path']:<40} {size_mb:.1f}MB")
    
    def _print_status_info(self, status_info):
        """打印状态信息
        
        Args:
            status_info: 状态信息
        """
        print("📊 系统状态:")
        print("=" * 50)
        
        # 系统状态
        init_status = "✅ 已初始化" if status_info['initialized'] else "❌ 未初始化"
        print(f"系统状态: {init_status}")
        
        if status_info['initialization_error']:
            print(f"初始化错误: {status_info['initialization_error']}")
        
        # 加载器状态
        module_status = "✅ 已安装" if status_info['module_loader_installed'] else "❌ 未安装"
        onnx_status = "✅ 已安装" if status_info['onnx_loader_installed'] else "❌ 未安装"
        
        print(f"模块加载器: {module_status}")
        print(f"ONNX 加载器: {onnx_status}")
        
        # 缓存信息
        module_cache = status_info['module_cache_info']
        onnx_cache = status_info['onnx_cache_info']
        
        if module_cache:
            print(f"模块缓存: {module_cache.get('cached_modules', 0)} 个")
        
        if onnx_cache:
            print(f"模型缓存: {onnx_cache.get('cached_models', 0)} 个")
            print(f"临时文件: {onnx_cache.get('temp_files', 0)} 个")
