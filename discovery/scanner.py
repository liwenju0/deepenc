#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件扫描器

实现智能的文件发现和扫描功能。
遵循 Linux 内核的设备发现机制。
"""

import os
import glob
from pathlib import Path
from .filters import FileFilter
from ..core.errors import FileDiscoveryError


class FileScanner:
    """文件扫描器
    
    智能扫描项目中的 Python 文件和 ONNX 模型文件。
    """
    
    def __init__(self, project_root=None, filter_rules=None):
        """初始化文件扫描器
        
        Args:
            project_root: 项目根目录，默认为当前目录
            filter_rules: 自定义过滤规则
        """
        self.project_root = Path(project_root or '.').resolve()
        self.file_filter = FileFilter(filter_rules)
        
        # 验证项目根目录
        if not self.project_root.exists():
            raise FileDiscoveryError(f"项目根目录不存在: {self.project_root}")
        
        print(f"📁 项目根目录: {self.project_root}")
    
    def discover_python_files(self):
        """发现所有 Python 文件
        
        Returns:
            list: Python 文件信息列表
        """
        try:
            python_files = []
            
            # 递归扫描所有 .py 文件
            for py_file in self.project_root.rglob('*.py'):
                if self.file_filter.should_include_file(py_file, self.project_root):
                    file_info = self._create_python_file_info(py_file)
                    python_files.append(file_info)
            
            print(f"🐍 发现 {len(python_files)} 个 Python 文件")
            return python_files
            
        except Exception as e:
            raise FileDiscoveryError(f"发现 Python 文件失败: {e}")
    
    def discover_onnx_files(self):
        """发现所有 ONNX 文件
        
        Returns:
            list: ONNX 文件信息列表
        """
        try:
            onnx_files = []
            
            # 递归扫描所有 .onnx 文件
            for onnx_file in self.project_root.rglob('*.onnx'):
                if self.file_filter.should_include_file(onnx_file, self.project_root):
                    file_info = self._create_onnx_file_info(onnx_file)
                    onnx_files.append(file_info)
            
            print(f"🧠 发现 {len(onnx_files)} 个 ONNX 模型")
            return onnx_files
            
        except Exception as e:
            raise FileDiscoveryError(f"发现 ONNX 文件失败: {e}")
    
    def discover_all_files(self):
        """发现所有相关文件
        
        Returns:
            dict: 包含 Python 文件和 ONNX 文件的字典
        """
        try:
            python_files = self.discover_python_files()
            onnx_files = self.discover_onnx_files()
            
            discovery_result = {
                'python_files': python_files,
                'onnx_files': onnx_files,
                'total_files': len(python_files) + len(onnx_files),
                'project_root': str(self.project_root)
            }
            
            print(f"📊 文件发现完成:")
            print(f"  - Python 文件: {len(python_files)} 个")
            print(f"  - ONNX 模型: {len(onnx_files)} 个")
            print(f"  - 总计: {discovery_result['total_files']} 个文件")
            
            return discovery_result
            
        except Exception as e:
            raise FileDiscoveryError(f"文件发现失败: {e}")
    
    def _create_python_file_info(self, py_file):
        """创建 Python 文件信息
        
        Args:
            py_file: Python 文件路径对象
            
        Returns:
            dict: 文件信息
        """
        relative_path = py_file.relative_to(self.project_root)
        module_name = self._path_to_module_name(relative_path)
        
        return {
            'file_path': str(py_file),
            'relative_path': str(relative_path),
            'module_name': module_name,
            'file_size': py_file.stat().st_size,
            'file_type': 'python'
        }
    
    def _create_onnx_file_info(self, onnx_file):
        """创建 ONNX 文件信息
        
        Args:
            onnx_file: ONNX 文件路径对象
            
        Returns:
            dict: 文件信息
        """
        relative_path = onnx_file.relative_to(self.project_root)
        model_name = self._path_to_model_name(relative_path)
        
        return {
            'file_path': str(onnx_file),
            'relative_path': str(relative_path),
            'model_name': model_name,
            'file_size': onnx_file.stat().st_size,
            'file_type': 'onnx'
        }
    
    def _path_to_module_name(self, relative_path):
        """将文件路径转换为模块名
        
        Args:
            relative_path: 相对路径
            
        Returns:
            str: 模块名
        """
        # 移除 .py 扩展名
        module_path = relative_path.with_suffix('')
        
        # 转换为 Python 模块名格式
        module_name = '.'.join(module_path.parts)
        
        return module_name
    
    def _path_to_model_name(self, relative_path):
        """将文件路径转换为模型名
        
        Args:
            relative_path: 相对路径
            
        Returns:
            str: 模型名
        """
        # 使用文件名（不含扩展名）作为模型名
        model_name = relative_path.stem
        
        # 如果在子目录中，包含目录名
        if len(relative_path.parts) > 1:
            parent_dir = relative_path.parent.name
            model_name = f"{parent_dir}.{model_name}"
        
        return model_name
    
    def scan_directory(self, directory, file_pattern='*'):
        """扫描指定目录
        
        Args:
            directory: 目录路径
            file_pattern: 文件模式
            
        Returns:
            list: 文件路径列表
        """
        try:
            dir_path = Path(directory)
            
            if not dir_path.exists() or not dir_path.is_dir():
                raise FileDiscoveryError(f"目录不存在或不是目录: {directory}")
            
            # 检查目录是否应该包含
            if not self.file_filter.should_include_directory(dir_path):
                print(f"⏭️ 跳过排除目录: {directory}")
                return []
            
            # 扫描文件
            files = []
            for file_path in dir_path.rglob(file_pattern):
                if self.file_filter.should_include_file(file_path, self.project_root):
                    files.append(str(file_path))
            
            return files
            
        except Exception as e:
            raise FileDiscoveryError(f"扫描目录失败 {directory}: {e}")
    
    def get_scan_stats(self):
        """获取扫描统计信息
        
        Returns:
            dict: 扫描统计信息
        """
        try:
            # 统计所有文件
            all_py_files = list(self.project_root.rglob('*.py'))
            all_onnx_files = list(self.project_root.rglob('*.onnx'))
            
            # 统计过滤后的文件
            filtered_py = self.file_filter.filter_files(
                [str(f) for f in all_py_files], 
                str(self.project_root)
            )
            filtered_onnx = self.file_filter.filter_files(
                [str(f) for f in all_onnx_files], 
                str(self.project_root)
            )
            
            return {
                'project_root': str(self.project_root),
                'total_python_files': len(all_py_files),
                'total_onnx_files': len(all_onnx_files),
                'filtered_python_files': len(filtered_py),
                'filtered_onnx_files': len(filtered_onnx),
                'python_exclusion_rate': 1 - (len(filtered_py) / len(all_py_files)) if all_py_files else 0,
                'onnx_exclusion_rate': 1 - (len(filtered_onnx) / len(all_onnx_files)) if all_onnx_files else 0
            }
            
        except Exception as e:
            raise FileDiscoveryError(f"获取扫描统计信息失败: {e}")
    
    def find_files_by_pattern(self, pattern):
        """根据模式查找文件
        
        Args:
            pattern: 文件模式（支持通配符）
            
        Returns:
            list: 匹配的文件列表
        """
        try:
            matched_files = []
            
            for file_path in self.project_root.rglob(pattern):
                if self.file_filter.should_include_file(file_path, self.project_root):
                    matched_files.append(str(file_path))
            
            return matched_files
            
        except Exception as e:
            raise FileDiscoveryError(f"按模式查找文件失败 {pattern}: {e}")
    
    def find_files_by_size(self, min_size=0, max_size=None):
        """根据文件大小查找文件
        
        Args:
            min_size: 最小文件大小（字节）
            max_size: 最大文件大小（字节），None 表示无限制
            
        Returns:
            list: 匹配的文件列表
        """
        try:
            matched_files = []
            
            # 扫描所有相关文件
            for file_pattern in ['*.py', '*.onnx']:
                for file_path in self.project_root.rglob(file_pattern):
                    if self.file_filter.should_include_file(file_path, self.project_root):
                        file_size = file_path.stat().st_size
                        
                        # 检查文件大小
                        if file_size >= min_size:
                            if max_size is None or file_size <= max_size:
                                matched_files.append({
                                    'file_path': str(file_path),
                                    'file_size': file_size,
                                    'file_type': file_path.suffix[1:]  # 移除点号
                                })
            
            return matched_files
            
        except Exception as e:
            raise FileDiscoveryError(f"按大小查找文件失败: {e}")
