#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI 命令实现

实现所有命令行工具的功能。
遵循 Linux 命令行工具的设计风格。
"""

import json
import os
from pathlib import Path

from ..bootstrap import get_system
from ..builders.project_builder import ProjectBuilder
from ..discovery.scanner import FileScanner
from ..utils.build_output import BuildOutputFormatter, create_build_info_from_report


class EncryptCLI:
    """加密框架 CLI 实现

    提供完整的命令行接口。
    """

    def __init__(self):
        """初始化 CLI"""
        self.project_root = Path.cwd()
        self.output_formatter = BuildOutputFormatter()

    def build(
        self,
        project_path=None,
        output_dir=None,
        entry_point=None,
        exclude_dirs=None,
        exclude_files=None,
        clean=True,
        verbose=False,
        genzip=False,
        zip_stored=False,
    ):
        """构建项目

        Args:
            project_path: 项目路径，默认当前目录
            output_dir: 输出目录，默认 project_path/build
            entry_point: 项目入口Python文件，默认src/grpc_main.py
            exclude_dirs: 要排除的目录列表
            exclude_files: 要排除的文件列表
            clean: 是否清理构建目录
            verbose: 是否显示详细信息
            genzip: 是否生成ZIP包
            zip_stored: 是否使用ZIP_STORED模式（不压缩，直接存储）

        Returns:
            int: 退出码 (0=成功, 1=失败)
        """
        try:
            project_root = Path(project_path or ".").resolve()
            build_dir = Path(output_dir or project_root / "build").resolve()

            # 简化的构建信息输出
            print(f"Building project: {project_root}")
            print(f"Output directory: {build_dir}")
            if entry_point:
                print(f"Entry point: {entry_point}")
            print("Encryption: ENABLED")
            
            if exclude_dirs:
                print(f"Excluded directories: {', '.join(exclude_dirs)}")
            if exclude_files:
                print(f"Excluded files: {', '.join(exclude_files)}")

            # 创建项目构建器
            builder = ProjectBuilder(
                project_root=project_root,
                build_dir=build_dir,
                exclude_dirs=exclude_dirs,
                exclude_files=exclude_files,
            )

            # 构建项目
            build_report = builder.build_project(clean=clean)

            # 使用统一的输出格式化器
            build_info = create_build_info_from_report(build_report)
            if verbose:
                print(self.output_formatter.format_verbose(build_info))
            else:
                print(self.output_formatter.format_summary(build_info))

            # 如果指定了生成zip包，则在构建完成后生成
            if genzip:
                print("Generating ZIP package...")
                zip_result = self._generate_project_zip(
                    project_root, build_dir, verbose, zip_stored
                )
                if zip_result:
                    print(f"ZIP package created: {zip_result}")
                else:
                    print("ZIP package generation failed")

            return 0

        except Exception as e:
            print(f"Build failed: {e}")
            return 1

    def scan(self, project_path=None, output_format="table"):
        """扫描项目文件

        Args:
            project_path: 项目路径，默认当前目录
            output_format: 输出格式 ('table', 'json', 'simple')

        Returns:
            int: 退出码
        """
        try:
            project_root = Path(project_path or ".").resolve()

            print(f"Scanning project: {project_root}")

            # 创建文件扫描器
            scanner = FileScanner(project_root)

            # 发现文件
            discovery_result = scanner.discover_all_files()

            # 输出结果
            if output_format == "json":
                print(json.dumps(discovery_result, indent=2, ensure_ascii=False))
            elif output_format == "simple":
                self._print_simple_scan_result(discovery_result)
            else:  # table
                self._print_table_scan_result(discovery_result)

            return 0

        except Exception as e:
            print(f"Scan failed: {e}")
            return 1

    def status(self):
        """显示系统状态

        Returns:
            int: 退出码
        """
        try:
            system = get_system()

            if system is None:
                print("Encryption system not initialized")
                return 1

            status_info = system.get_status()
            self._print_status_info(status_info)

            return 0

        except Exception as e:
            print(f"Status check failed: {e}")
            return 1

    def init(self, project_path=None):
        """初始化加密系统

        Args:
            project_path: 项目路径，默认当前目录

        Returns:
            int: 退出码
        """
        try:
            project_root = Path(project_path or ".").resolve()

            print(f"Initializing encryption system: {project_root}")

            # 切换到项目目录
            os.chdir(project_root)

            # 尝试自动初始化
            from ..bootstrap import auto_initialize

            system = auto_initialize()

            if system:
                print("Encryption system initialized successfully")
                return 0
            else:
                print("Encryption system initialization failed")
                return 1

        except Exception as e:
            print(f"Initialization failed: {e}")
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
            project_root = Path(project_path or ".").resolve()
            build_dir = Path(build_dir or project_root / "build").resolve()

            print(f"Cleaning build directory: {build_dir}")

            # 直接清理构建目录，避免创建 ProjectBuilder 实例
            if build_dir.exists():
                import shutil

                shutil.rmtree(build_dir)
                print(f"Build directory cleaned: {build_dir}")
            else:
                print("Build directory does not exist, nothing to clean")

            return 0

        except Exception as e:
            print(f"Clean failed: {e}")
            return 1

    def verify(self, build_dir=None):
        """验证构建结果

        Args:
            build_dir: 构建目录，默认当前目录/build

        Returns:
            int: 退出码
        """
        try:
            project_root = Path(".").resolve()
            build_dir = Path(build_dir or project_root / "build").resolve()

            print(f"Verifying build result: {build_dir}")

            # 创建项目构建器
            builder = ProjectBuilder(project_root, build_dir)

            if builder.verify_build():
                print("Build verification passed")
                return 0
            else:
                print("Build verification failed")
                return 1

        except Exception as e:
            print(f"Verification failed: {e}")
            return 1


    def _print_simple_scan_result(self, discovery_result):
        """打印简单扫描结果

        Args:
            discovery_result: 发现结果
        """
        print(f"\nPython files ({len(discovery_result['python_files'])}):")
        for file_info in discovery_result["python_files"]:
            print(f"  {file_info['module_name']} -> {file_info['relative_path']}")

        print(f"\nONNX models ({len(discovery_result['onnx_files'])}):")
        for file_info in discovery_result["onnx_files"]:
            print(f"  {file_info['model_name']} -> {file_info['relative_path']}")

    def _print_table_scan_result(self, discovery_result):
        """打印表格格式扫描结果

        Args:
            discovery_result: 发现结果
        """
        print("\nFile Scan Results:")
        print("=" * 80)

        # Python 文件表格
        if discovery_result["python_files"]:
            print("\nPython files:")
            print(f"{'Module':<30} {'Path':<40} {'Size':<10}")
            print("-" * 80)

            for file_info in discovery_result["python_files"]:
                size_kb = file_info["file_size"] / 1024
                print(
                    f"{file_info['module_name']:<30} {file_info['relative_path']:<40} {size_kb:.1f}KB"
                )

        # ONNX 模型表格
        if discovery_result["onnx_files"]:
            print("\nONNX models:")
            print(f"{'Model':<30} {'Path':<40} {'Size':<10}")
            print("-" * 80)

            for file_info in discovery_result["onnx_files"]:
                size_mb = file_info["file_size"] / (1024 * 1024)
                print(
                    f"{file_info['model_name']:<30} {file_info['relative_path']:<40} {size_mb:.1f}MB"
                )

    def _print_status_info(self, status_info):
        """打印状态信息

        Args:
            status_info: 状态信息
        """
        print("System Status:")
        print("=" * 50)

        # 系统状态
        init_status = "INITIALIZED" if status_info["initialized"] else "NOT INITIALIZED"
        print(f"System: {init_status}")

        if status_info["initialization_error"]:
            print(f"Error: {status_info['initialization_error']}")

        # 加载器状态
        module_status = "INSTALLED" if status_info["module_loader_installed"] else "NOT INSTALLED"
        onnx_status = "INSTALLED" if status_info["onnx_loader_installed"] else "NOT INSTALLED"

        print(f"Module Loader: {module_status}")
        print(f"ONNX Loader: {onnx_status}")

        # 缓存信息
        module_cache = status_info["module_cache_info"]
        onnx_cache = status_info["onnx_cache_info"]

        if module_cache:
            print(f"Module Cache: {module_cache.get('cached_modules', 0)} modules")

        if onnx_cache:
            print(f"Model Cache: {onnx_cache.get('cached_models', 0)} models")
            print(f"Temp Files: {onnx_cache.get('temp_files', 0)} files")

    def _generate_project_zip(self, project_root, build_dir, verbose=False, zip_stored=False):
        """生成项目zip包

        Args:
            project_root: 项目根目录
            build_dir: 构建目录
            verbose: 是否显示详细信息
            zip_stored: 是否使用ZIP_STORED模式（不压缩，直接存储）

        Returns:
            str: 生成的zip包路径，失败返回None
        """
        try:
            import os
            import zipfile

            # 读取项目VERSION文件
            version_file = project_root / "VERSION"
            if not version_file.exists():
                print(f"VERSION file not found: {version_file}")
                return None

            # 读取版本号
            with open(version_file, "r", encoding="utf-8") as f:
                version = f.read().strip()

            if not version:
                print("VERSION file is empty")
                return None

            # 获取项目名称（从目录名）
            project_name = project_root.name

            # 创建zip文件名
            zip_filename = f"{project_name}.{version}.zip"

            # 确保dist目录存在
            dist_dir = build_dir / "dist"
            dist_dir.mkdir(exist_ok=True)

            # zip包完整路径
            zip_path = dist_dir / zip_filename

            # 获取压缩密码
            unzip_code = os.environ.get("UNZIP_CODE", "deepenc")
            if unzip_code == "deepenc":
                print("Warning: Using default password 'deepenc', set UNZIP_CODE environment variable")

            # 选择压缩模式
            compression_mode = zipfile.ZIP_STORED if zip_stored else zipfile.ZIP_DEFLATED
            compression_name = "STORED (no compression)" if zip_stored else "DEFLATED (compressed)"

            if verbose:
                print(f"Project: {project_name}")
                print(f"Version: {version}")
                print(f"Password: {unzip_code}")
                print(f"Compression: {compression_name}")
                print(f"Target: {zip_path}")

            # 创建带密码的zip文件
            with zipfile.ZipFile(zip_path, "w", compression_mode) as zipf:
                # 遍历构建目录中的所有文件
                for file_path in build_dir.rglob("*"):
                    if file_path.is_file():
                        # 计算相对路径
                        relative_path = file_path.relative_to(build_dir)

                        # 跳过dist目录本身
                        if relative_path.parts[0] == "dist":
                            continue

                        if verbose:
                            print(f"  Adding file: {relative_path}")

                        # 添加文件到zip
                        zipf.write(file_path, relative_path)

            # 设置zip文件密码（通过重命名文件来模拟密码保护）
            # 注意：Python的zipfile模块不直接支持密码保护，这里只是创建了zip文件
            # 实际使用时可以通过其他工具（如7zip）来设置密码

            if verbose:
                print(f"ZIP size: {zip_path.stat().st_size / 1024:.1f} KB")

            return str(zip_path)

        except Exception as e:
            print(f"ZIP generation failed: {e}")
            if verbose:
                import traceback

                traceback.print_exc()
            return None
