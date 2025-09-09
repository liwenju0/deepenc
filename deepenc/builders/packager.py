#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目打包器

实现项目的打包和分发功能。
"""

import zipfile
from pathlib import Path

from ..core.errors import BuildError


class ProjectPackager:
    """项目打包器"""

    def __init__(self, build_dir):
        """初始化打包器

        Args:
            build_dir: 构建目录
        """
        self.build_dir = Path(build_dir)

    def create_package(self, package_name=None, password=None):
        """创建项目包

        Args:
            package_name: 包名称
            password: 压缩包密码

        Returns:
            str: 包文件路径
        """
        try:
            if not package_name:
                package_name = f"{self.build_dir.parent.name}-encrypted.zip"

            package_path = self.build_dir.parent / package_name

            # 创建压缩包
            with zipfile.ZipFile(package_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for file_path in self.build_dir.rglob("*"):
                    if file_path.is_file():
                        arcname = file_path.relative_to(self.build_dir)
                        zipf.write(file_path, arcname)

            print(f"📦 创建包: {package_path}")
            return str(package_path)

        except Exception as e:
            raise BuildError(f"创建包失败: {e}")
