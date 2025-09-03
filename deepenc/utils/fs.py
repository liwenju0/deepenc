#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件系统工具

提供文件系统相关的工具函数。
"""

import os
import shutil
import tempfile
from pathlib import Path


class FileSystemUtils:
    """文件系统工具类"""
    
    @staticmethod
    def ensure_dir(dir_path):
        """确保目录存在
        
        Args:
            dir_path: 目录路径
        """
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def safe_remove(file_path):
        """安全删除文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否删除成功
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception:
            return False
    
    @staticmethod
    def safe_rmtree(dir_path):
        """安全删除目录树
        
        Args:
            dir_path: 目录路径
            
        Returns:
            bool: 是否删除成功
        """
        try:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
                return True
            return False
        except Exception:
            return False
    
    @staticmethod
    def create_temp_file(suffix='', prefix='encrypt_', dir=None):
        """创建临时文件
        
        Args:
            suffix: 文件后缀
            prefix: 文件前缀
            dir: 临时目录
            
        Returns:
            str: 临时文件路径
        """
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
            prefix=prefix,
            dir=dir
        )
        temp_file.close()
        return temp_file.name
    
    @staticmethod
    def get_file_size(file_path):
        """获取文件大小
        
        Args:
            file_path: 文件路径
            
        Returns:
            int: 文件大小（字节）
        """
        try:
            return os.path.getsize(file_path)
        except Exception:
            return 0
    
    @staticmethod
    def is_binary_file(file_path):
        """判断是否是二进制文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否是二进制文件
        """
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                return b'\0' in chunk
        except Exception:
            return True
    
    @staticmethod
    def copy_file(src, dst):
        """复制文件
        
        Args:
            src: 源文件路径
            dst: 目标文件路径
        """
        FileSystemUtils.ensure_dir(os.path.dirname(dst))
        shutil.copy2(src, dst)
    
    @staticmethod
    def move_file(src, dst):
        """移动文件
        
        Args:
            src: 源文件路径
            dst: 目标文件路径
        """
        FileSystemUtils.ensure_dir(os.path.dirname(dst))
        shutil.move(src, dst)
