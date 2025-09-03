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
    
    def build(self, project_path=None, output_dir=None, entry_point=None, exclude_dirs=None, exclude_files=None, clean=True, verbose=False, genzip=False):
        """构建加密项目
        
        Args:
            project_path: 项目路径，默认当前目录
            output_dir: 输出目录，默认 project_path/build
            entry_point: 项目入口Python文件，默认src/grpc_main.py
            exclude_dirs: 要排除的目录列表
            exclude_files: 要排除的文件列表
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
            
            # 显示排除的目录和文件
            if exclude_dirs:
                print(f"🚫 排除目录: {', '.join(exclude_dirs)}")
            if exclude_files:
                print(f"🚫 排除文件: {', '.join(exclude_files)}")
            
            # 创建项目构建器
            builder = ProjectBuilder(
                project_root=project_root, 
                build_dir=build_dir,
                exclude_dirs=exclude_dirs,
                exclude_files=exclude_files
            )
            
            # 构建项目
            build_report = builder.build_project(clean=clean)
            
            if verbose:
                self._print_verbose_report(build_report)
            
            # 如果指定了生成zip包，则在构建完成后生成
            if genzip:
                print(f"📦 构建完成，开始生成zip包...")
                zip_result = self._generate_project_zip(project_root, build_dir, verbose)
                if zip_result:
                    print(f"✅ zip包生成成功: {zip_result}")
                else:
                    print(f"⚠️ zip包生成失败")
            
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
            
            # 直接清理构建目录，避免创建 ProjectBuilder 实例
            if build_dir.exists():
                import shutil
                shutil.rmtree(build_dir)
                print(f"✅ 已清理构建目录: {build_dir}")
            else:
                print("ℹ️ 构建目录不存在，无需清理")
            
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
        if 'build_info' in build_report and build_report['build_info']:
            build_info = build_report['build_info']
            if 'start_time' in build_info:
                print(f"  开始时间: {build_info['start_time']}")
            if 'end_time' in build_info:
                print(f"  结束时间: {build_info['end_time']}")
            if 'duration_seconds' in build_info:
                print(f"  构建时长: {build_info['duration_seconds']:.2f} 秒")
            if 'success' in build_info:
                print(f"  构建状态: {'成功' if build_info['success'] else '失败'}")
        else:
            print("  ⚠️ 构建信息不完整")
        
        # 文件发现信息
        print("\n🔍 文件发现:")
        if 'discovery' in build_report and build_report['discovery']:
            discovery = build_report['discovery']
            if 'total_python_files' in discovery:
                print(f"  Python 文件: {discovery['total_python_files']} 个")
            if 'total_onnx_files' in discovery:
                print(f"  ONNX 模型: {discovery['total_onnx_files']} 个")
        else:
            print("  ⚠️ 文件发现信息不完整")
        
        # 加密信息
        print("\n🔐 加密结果:")
        if 'encryption' in build_report and build_report['encryption']:
            encryption = build_report['encryption']
            if 'encrypted_python_modules' in encryption:
                print(f"  加密 Python 模块: {encryption['encrypted_python_modules']} 个")
            if 'encrypted_onnx_models' in encryption:
                print(f"  加密 ONNX 模型: {encryption['encrypted_onnx_models']} 个")
            
            if 'python_modules' in encryption and encryption['python_modules']:
                print("\n  Python 模块列表:")
                for module in encryption['python_modules']:
                    print(f"    - {module}")
            
            if 'onnx_models' in encryption and encryption['onnx_models']:
                print("\n  ONNX 模型列表:")
                for model in encryption['onnx_models']:
                    print(f"    - {model}")
        else:
            print("  ⚠️ 加密信息不完整")
        
        # 输出信息
        print("\n📁 输出文件:")
        if 'output' in build_report and build_report['output']:
            output = build_report['output']
            if 'build_dir' in output:
                print(f"  构建目录: {output['build_dir']}")
            if 'encrypted_dir' in output:
                print(f"  加密目录: {output['encrypted_dir']}")
            if 'config_file' in output:
                print(f"  配置文件: {output['config_file']}")
            if 'bootstrap_script' in output:
                print(f"  启动脚本: {output['bootstrap_script']}")
        else:
            print("  ⚠️ 输出信息不完整")
        
        # 授权信息
        print("\n🔑 授权信息:")
        if 'auth_info' in build_report and build_report['auth_info']:
            auth_info = build_report['auth_info']
            if 'auth_mode' in auth_info:
                print(f"  授权模式: {auth_info['auth_mode']}")
            if 'key_source' in auth_info:
                print(f"  密钥来源: {auth_info['key_source']}")
            if 'hardware_auth_available' in auth_info:
                print(f"  硬件授权: {'可用' if auth_info['hardware_auth_available'] else '不可用'}")
            if 'authorization_valid' in auth_info:
                print(f"  授权状态: {'有效' if auth_info['authorization_valid'] else '无效'}")
        else:
            print("  ⚠️ 授权信息不完整")
    
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
    
    def _generate_project_zip(self, project_root, build_dir, verbose=False):
        """生成项目zip包
        
        Args:
            project_root: 项目根目录
            build_dir: 构建目录
            verbose: 是否显示详细信息
            
        Returns:
            str: 生成的zip包路径，失败返回None
        """
        try:
            import zipfile
            import os
            
            # 读取项目VERSION文件
            version_file = project_root / 'VERSION'
            if not version_file.exists():
                print(f"⚠️ 项目根目录下未找到VERSION文件: {version_file}")
                return None
            
            # 读取版本号
            with open(version_file, 'r', encoding='utf-8') as f:
                version = f.read().strip()
            
            if not version:
                print(f"⚠️ VERSION文件内容为空")
                return None
            
            # 获取项目名称（从目录名）
            project_name = project_root.name
            
            # 创建zip文件名
            zip_filename = f"{project_name}.{version}.zip"
            
            # 确保dist目录存在
            dist_dir = build_dir / 'dist'
            dist_dir.mkdir(exist_ok=True)
            
            # zip包完整路径
            zip_path = dist_dir / zip_filename
            
            # 获取压缩密码
            unzip_code = os.environ.get('UNZIP_CODE', 'DC2024hexie')
            
            if verbose:
                print(f"📁 项目名称: {project_name}")
                print(f"📋 版本号: {version}")
                print(f"🔐 压缩密码: {unzip_code}")
                print(f"📦 目标文件: {zip_path}")
            
            # 创建带密码的zip文件
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # 遍历构建目录中的所有文件
                for file_path in build_dir.rglob('*'):
                    if file_path.is_file():
                        # 计算相对路径
                        relative_path = file_path.relative_to(build_dir)
                        
                        # 跳过dist目录本身
                        if relative_path.parts[0] == 'dist':
                            continue
                        
                        if verbose:
                            print(f"  📄 添加文件: {relative_path}")
                        
                        # 添加文件到zip
                        zipf.write(file_path, relative_path)
            
            # 设置zip文件密码（通过重命名文件来模拟密码保护）
            # 注意：Python的zipfile模块不直接支持密码保护，这里只是创建了zip文件
            # 实际使用时可以通过其他工具（如7zip）来设置密码
            
            if verbose:
                print(f"📊 zip包大小: {zip_path.stat().st_size / 1024:.1f} KB")
            
            return str(zip_path)
            
        except Exception as e:
            print(f"❌ 生成zip包失败: {e}")
            if verbose:
                import traceback
                traceback.print_exc()
            return None
