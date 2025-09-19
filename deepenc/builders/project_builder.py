#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的项目构建器

核心功能:
1. 复制整个项目到build目录
2. 加密ONNX模型和Python文件
3. 支持排除特定目录和文件
4. 不生成配置文件，依赖用户自定义loader
"""

import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from ..core.auth import AuthManager
from ..core.crypto import AESCrypto
from ..core.errors import BuildError
from ..discovery.scanner import FileScanner


class BuildConstants:
    """构建系统常量定义"""

    # 目录结构
    BUILD_DIR_NAME = "build"

    # 文件扩展名
    PYTHON_ENCRYPTED_EXT = ".encrypted"
    ONNX_ENCRYPTED_EXT = ".encrypt"

    # 不复制到build目录的目录
    EXCLUDED_COPY_DIRS = [
        "release",
        "3thirdParty",
        "build",
        "dist",
        ".git",
        "__pycache__",
        "*.egg-info",
    ]

    # 不加密的文件
    EXCLUDED_ENCRYPT_FILES = ["src/grpc_main.py", "*.pyc", "__pycache__"]


class ProjectBuilder:
    """简化的项目构建器"""

    def __init__(
        self,
        project_root=None,
        build_dir=None,
        exclude_dirs=None,
        exclude_files=None,
        skip_encryption=False,
    ):
        """初始化项目构建器

        Args:
            project_root: 项目根目录
            build_dir: 构建输出目录
            exclude_dirs: 要排除的目录列表
            exclude_files: 要排除的文件列表
            skip_encryption: 是否跳过加密，仅进行打包
        """
        # 路径设置
        self.project_root = Path(project_root or ".").resolve()
        self.build_dir = Path(
            build_dir or self.project_root / BuildConstants.BUILD_DIR_NAME
        ).resolve()

        # 排除规则
        self.exclude_dirs = set(exclude_dirs or [])
        self.exclude_files = set(exclude_files or [])

        # 加密控制
        self.skip_encryption = skip_encryption

        # 初始化核心组件
        self.scanner = FileScanner(self.project_root)
        self.crypto = AESCrypto()
        self.auth_manager = AuthManager()

        # 设置日志
        self.logger = logging.getLogger(__name__)
        self._setup_logging()

        self.logger.info("项目构建器初始化完成")
        self.logger.info(f"项目根目录: {self.project_root}")
        self.logger.info(f"构建目录: {self.build_dir}")
        if self.skip_encryption:
            self.logger.info("🔓 跳过加密模式：仅进行文件复制和打包")
        if self.exclude_dirs:
            self.logger.info(f"排除目录: {', '.join(self.exclude_dirs)}")
        if self.exclude_files:
            self.logger.info(f"排除文件: {', '.join(self.exclude_files)}")

    def _setup_logging(self):
        """设置日志配置"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    def build_project(self, clean=True) -> Dict[str, Any]:
        """构建项目（支持加密或非加密模式）

        构建流程:
        1. 清理并准备构建目录
        2. 复制项目文件到build目录
        3. 如果启用加密：加密Python文件和ONNX模型
        4. 如果跳过加密：仅复制文件，不进行加密

        Args:
            clean: 是否清理构建目录

        Returns:
            Dict[str, Any]: 构建结果信息
        """
        try:
            if self.skip_encryption:
                self.logger.info("开始构建项目（跳过加密模式）...")
            else:
                self.logger.info("开始构建加密项目...")
            start_time = datetime.now()

            # 步骤1: 准备构建目录
            self._prepare_build_directory(clean)

            # 步骤2: 复制项目文件
            self._copy_project_files()

            # 步骤3和4: 根据配置决定是否加密
            if self.skip_encryption:
                # 跳过加密模式：仅复制文件
                python_result = {}
                onnx_result = {}
                self.logger.info("跳过加密，保持原始文件")
            else:
                # 加密模式：加密Python文件和ONNX模型
                python_result = self._encrypt_python_files()
                onnx_result = self._encrypt_onnx_files()

            # 计算构建时间
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # 创建构建报告
            build_report = {
                "success": True,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration_seconds": duration,
                "encrypted_python_files": len(python_result),
                "encrypted_onnx_files": len(onnx_result),
                "skip_encryption": self.skip_encryption,
                "build_dir": str(self.build_dir),
            }

            if self.skip_encryption:
                self.logger.info("项目构建成功完成（未加密）")
            else:
                self.logger.info("项目构建成功完成")
            self._print_build_summary(build_report)

            return build_report

        except Exception as e:
            self.logger.error(f"项目构建失败: {e}")
            raise BuildError(f"项目构建失败: {e}")

    def _prepare_build_directory(self, clean: bool):
        """准备构建目录"""
        if clean and self.build_dir.exists():
            shutil.rmtree(self.build_dir)
            self.logger.info(f"已清理构建目录: {self.build_dir}")

        self.build_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info("构建目录准备完成")

    def _copy_project_files(self):
        """复制项目文件到build目录"""
        self.logger.info("开始复制项目文件...")

        # 遍历项目根目录
        for item in self.project_root.iterdir():
            if self._should_copy_item(item):
                self._copy_item(item)

        # 如果跳过加密模式，清理可能存在的加密文件
        if self.skip_encryption:
            self._clean_encrypted_files()

        self.logger.info("项目文件复制完成")

    def _clean_encrypted_files(self):
        """清理构建目录中的加密文件"""
        if not self.build_dir.exists():
            return

        # 清理.encrypted文件
        for encrypted_file in self.build_dir.rglob("*.encrypted"):
            encrypted_file.unlink()
            self.logger.debug(f"已清理加密文件: {encrypted_file.relative_to(self.build_dir)}")

        # 清理.encrypt文件
        for encrypted_file in self.build_dir.rglob("*.encrypt"):
            encrypted_file.unlink()
            self.logger.debug(f"已清理加密文件: {encrypted_file.relative_to(self.build_dir)}")

        self.logger.info("已清理构建目录中的加密文件")

    def _should_copy_item(self, item: Path) -> bool:
        """判断是否应该复制项目项"""
        item_name = item.name

        # 检查是否在命令行指定的排除目录列表中
        if item_name in self.exclude_dirs:
            self.logger.debug(f"排除目录: {item_name}")
            return False

        # 检查是否在默认排除目录列表中
        for excluded_dir in BuildConstants.EXCLUDED_COPY_DIRS:
            if excluded_dir.startswith("*"):
                # 通配符模式
                if item_name.endswith(excluded_dir[1:]):
                    self.logger.debug(f"排除目录(默认): {item_name}")
                    return False
            else:
                # 精确匹配
                if item_name == excluded_dir:
                    self.logger.debug(f"排除目录(默认): {item_name}")
                    return False

        # 不复制构建目录本身
        if item == self.build_dir:
            return False

        return True

    def _copy_item(self, item: Path):
        """复制单个项目项"""
        target_path = self.build_dir / item.name

        if item.is_file():
            shutil.copy2(item, target_path)
            self.logger.debug(f"复制文件: {item.name}")
        elif item.is_dir():
            shutil.copytree(item, target_path, dirs_exist_ok=True)
            self.logger.debug(f"复制目录: {item.name}")

    def _encrypt_python_files(self) -> Dict[str, Any]:
        """加密Python文件"""
        self.logger.info("开始加密Python文件...")

        # 发现Python文件
        discovery_result = self.scanner.discover_all_files()
        python_files = discovery_result.get("python_files", [])

        # 过滤掉不加密的文件
        filtered_files = []
        for file_info in python_files:
            if not self._should_exclude_from_encryption(file_info):
                filtered_files.append(file_info)
            else:
                self.logger.info(
                    f"排除加密: {file_info['file_path']} (相对路径: {file_info['relative_path']})"
                )

        # 加密文件
        encryption_key = self.auth_manager.get_key()
        encrypted_files = {}

        for file_info in filtered_files:
            file_info["file_path"]
            relative_path = file_info["relative_path"]

            # 在build目录中找到对应的文件
            build_file_path = self.build_dir / relative_path
            if build_file_path.exists():
                # 创建加密文件路径
                encrypted_path = build_file_path.with_suffix(
                    build_file_path.suffix + BuildConstants.PYTHON_ENCRYPTED_EXT
                )

                # 加密文件
                self.crypto.encrypt_file(
                    str(build_file_path), str(encrypted_path), encryption_key
                )

                # 删除原始Python文件，保留加密文件
                build_file_path.unlink()
                self.logger.debug(f"已删除原始文件: {relative_path}")

                encrypted_files[relative_path] = str(encrypted_path)
                self.logger.debug(f"已加密: {relative_path}")

        self.logger.info(f"Python文件加密完成，共 {len(encrypted_files)} 个")
        return encrypted_files

    def _encrypt_onnx_files(self) -> Dict[str, Any]:
        """加密ONNX模型文件"""
        self.logger.info("开始加密ONNX模型...")

        # 发现ONNX文件
        discovery_result = self.scanner.discover_all_files()
        onnx_files = discovery_result.get("onnx_files", [])

        # 过滤掉不加密的文件
        filtered_files = []
        for file_info in onnx_files:
            if not self._should_exclude_from_encryption(file_info):
                filtered_files.append(file_info)
            else:
                self.logger.info(
                    f"排除加密: {file_info['file_path']} (相对路径: {file_info['relative_path']})"
                )

        # 加密文件
        encryption_key = self.auth_manager.get_key()
        encrypted_files = {}

        for file_info in filtered_files:
            file_info["file_path"]
            relative_path = file_info["relative_path"]

            # 在build目录中找到对应的文件
            build_file_path = self.build_dir / relative_path
            if build_file_path.exists():
                # 创建加密文件路径
                encrypted_path = build_file_path.with_suffix(
                    build_file_path.suffix + BuildConstants.ONNX_ENCRYPTED_EXT
                )

                # 加密文件
                self.crypto.encrypt_file(
                    str(build_file_path), str(encrypted_path), encryption_key
                )

                # 删除原始ONNX文件，保留加密文件
                build_file_path.unlink()
                self.logger.debug(f"已删除原始文件: {relative_path}")

                encrypted_files[relative_path] = str(encrypted_path)
                self.logger.debug(f"已加密: {relative_path}")

        self.logger.info(f"ONNX模型加密完成，共 {len(encrypted_files)} 个")
        return encrypted_files

    def _should_exclude_from_encryption(self, file_info: Dict[str, Any]) -> bool:
        """判断文件是否应该被排除加密"""
        str(file_info["file_path"])
        relative_path = str(file_info["relative_path"])

        # 检查是否匹配排除模式
        for pattern in BuildConstants.EXCLUDED_ENCRYPT_FILES:
            if pattern.startswith("*"):
                # 通配符模式
                if relative_path.endswith(pattern[1:]):
                    return True
            else:
                # 精确匹配
                if relative_path == pattern or relative_path.endswith("/" + pattern):
                    return True

        return False

    def _print_build_summary(self, build_report: Dict[str, Any]) -> None:
        """打印构建摘要"""
        print("\n📊 构建摘要:")
        duration = build_report["duration_seconds"]
        print(f"  ⏱️  构建时间: {duration:.2f} 秒")

        if build_report.get("skip_encryption", False):
            print(f"  🔓 加密模式: 跳过加密")
            print(f"  📁 构建目录: {build_report['build_dir']}")

            print("\n🎯 重要说明:")
            print("  ✅ 整个项目已复制到build目录")
            print("  ✅ 指定目录已排除（release、3thirdParty等）")
            print("  🔓 所有文件保持原始状态，未进行加密")
            print("  📦 可直接用于打包分发")
        else:
            print(f"  🐍 Python 文件: {build_report['encrypted_python_files']} 个")
            print(f"  🧠 ONNX 模型: {build_report['encrypted_onnx_files']} 个")
            print(f"  📁 构建目录: {build_report['build_dir']}")

            print("\n🎯 重要说明:")
            print("  ✅ 整个项目已复制到build目录")
            print("  ✅ 指定目录已排除（release、3thirdParty等）")
            print("  ✅ src/grpc_main.py 未被加密")
            print("  📝 请在grpc_main.py中添加加密loader进行解密")

    def clean_build(self) -> None:
        """清理构建目录"""
        try:
            if self.build_dir.exists():
                shutil.rmtree(self.build_dir)
                self.logger.info(f"已清理构建目录: {self.build_dir}")
            else:
                self.logger.info("构建目录不存在，无需清理")

        except Exception as e:
            raise BuildError(f"清理构建目录失败: {e}")

    def get_build_info(self) -> Dict[str, Any]:
        """获取构建信息"""
        return {
            "project_root": str(self.project_root),
            "build_dir": str(self.build_dir),
            "build_dir_exists": self.build_dir.exists(),
        }
