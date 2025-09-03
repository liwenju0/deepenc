#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件过滤器

实现智能的文件过滤规则。
遵循 Linux 内核的过滤器链设计模式。
"""

import os
import fnmatch
from pathlib import Path
from ..core.errors import FileDiscoveryError


class FileFilter:
    """文件过滤器
    
    提供灵活的文件过滤规则，支持多种过滤条件。
    """
    
    # 默认排除的目录
    DEFAULT_EXCLUDE_DIRS = {
        '.git', '.svn', '.hg',           # 版本控制
        '__pycache__', '.pytest_cache',  # Python 缓存
        'node_modules', '.npm',          # Node.js
        'build', 'dist', '.build',       # 构建目录
        'venv', 'env', '.venv',          # 虚拟环境
        '.idea', '.vscode',              # IDE
        'logs', 'log', '.logs',          # 日志目录
        'tmp', 'temp', '.tmp',           # 临时目录
        'test', 'tests', 'testing',      # 测试目录
        'docs', 'doc', 'documentation',  # 文档目录
        'examples', 'example', 'demo',   # 示例目录
        ".cursor",                       # cursor目录
    }
    
    # 默认排除的文件模式
    DEFAULT_EXCLUDE_FILES = {
        '__init__.py',                   # Python 包初始化文件
        'setup.py', 'setup.cfg',         # 安装脚本
        'requirements*.txt',             # 依赖文件
        'Pipfile*', 'poetry.lock',       # 包管理文件
        '*.pyc', '*.pyo', '*.pyd',       # Python 编译文件
        '*.so', '*.dll', '*.dylib',      # 动态库
        '*.log', '*.tmp', '*.bak',       # 临时文件
        '.*',                            # 隐藏文件
        'README*', 'LICENSE*', 'CHANGELOG*',  # 文档文件
        '*.md', '*.rst', '*.txt',        # 文档文件
        'Dockerfile*', '*.dockerfile',   # Docker 文件
        '*.yaml', '*.yml', '*.json',     # 配置文件
        '*.xml', '*.toml', '*.ini',      # 配置文件
    }
    
    # 默认排除的路径模式
    DEFAULT_EXCLUDE_PATHS = {
        '*/test/*', '*/tests/*',         # 测试路径
        '*/docs/*', '*/doc/*',           # 文档路径
        '*/examples/*', '*/example/*',   # 示例路径
        '*/scripts/*', '*/tools/*',      # 工具路径
        '*/sandbox/*', '*/playground/*', # 沙盒路径
    }
    
    def __init__(self, custom_rules=None):
        """初始化文件过滤器
        
        Args:
            custom_rules: 自定义过滤规则
        """
        self.exclude_dirs = self.DEFAULT_EXCLUDE_DIRS.copy()
        self.exclude_files = self.DEFAULT_EXCLUDE_FILES.copy()
        self.exclude_paths = self.DEFAULT_EXCLUDE_PATHS.copy()
        
        # 应用自定义规则
        if custom_rules:
            self._apply_custom_rules(custom_rules)
    
    def _apply_custom_rules(self, custom_rules):
        """应用自定义过滤规则
        
        Args:
            custom_rules: 自定义规则字典
        """
        if 'exclude_dirs' in custom_rules:
            self.exclude_dirs.update(custom_rules['exclude_dirs'])
        
        if 'exclude_files' in custom_rules:
            self.exclude_files.update(custom_rules['exclude_files'])
        
        if 'exclude_paths' in custom_rules:
            self.exclude_paths.update(custom_rules['exclude_paths'])
        
        if 'include_dirs' in custom_rules:
            # 从排除列表中移除指定目录
            for include_dir in custom_rules['include_dirs']:
                self.exclude_dirs.discard(include_dir)
        
        if 'include_files' in custom_rules:
            # 从排除列表中移除指定文件
            for include_file in custom_rules['include_files']:
                self.exclude_files.discard(include_file)
    
    def should_include_file(self, file_path, project_root=None):
        """判断文件是否应该包含
        
        Args:
            file_path: 文件路径
            project_root: 项目根目录
            
        Returns:
            bool: 是否应该包含
        """
        try:
            path_obj = Path(file_path)
            
            # 检查文件是否存在
            if not path_obj.exists():
                return False
            
            # 检查是否是文件
            if not path_obj.is_file():
                return False
            
            # 获取相对路径（用于路径模式匹配）
            if project_root:
                try:
                    relative_path = path_obj.relative_to(Path(project_root))
                    relative_path_str = str(relative_path)
                except ValueError:
                    # 文件不在项目根目录下
                    relative_path_str = str(path_obj)
            else:
                relative_path_str = str(path_obj)
            
            # 检查目录排除规则 - 只检查相对路径中的目录
            if project_root:
                relative_path_obj = Path(relative_path_str)
                for exclude_dir in self.exclude_dirs:
                    if exclude_dir in relative_path_obj.parts:
                        return False
            else:
                # 如果没有项目根目录，检查完整路径
                for exclude_dir in self.exclude_dirs:
                    if exclude_dir in path_obj.parts:
                        return False
            
            # 检查文件名排除规则
            file_name = path_obj.name
            for exclude_pattern in self.exclude_files:
                if fnmatch.fnmatch(file_name, exclude_pattern):
                    return False
            
            # 检查路径排除规则
            for exclude_pattern in self.exclude_paths:
                if fnmatch.fnmatch(relative_path_str, exclude_pattern):
                    return False
            
            return True
            
        except Exception as e:
            print(f"⚠️ 文件过滤检查失败 {file_path}: {e}")
            return False
    
    def should_include_directory(self, dir_path):
        """判断目录是否应该包含
        
        Args:
            dir_path: 目录路径
            
        Returns:
            bool: 是否应该包含
        """
        try:
            path_obj = Path(dir_path)
            
            # 检查目录是否存在
            if not path_obj.exists() or not path_obj.is_dir():
                return False
            
            # 检查目录名是否在排除列表中
            dir_name = path_obj.name
            if dir_name in self.exclude_dirs:
                return False
            
            # 检查是否是隐藏目录
            if dir_name.startswith('.') and dir_name != '.':
                return False
            
            return True
            
        except Exception as e:
            print(f"⚠️ 目录过滤检查失败 {dir_path}: {e}")
            return False
    
    def filter_files(self, file_list, project_root=None):
        """批量过滤文件
        
        Args:
            file_list: 文件路径列表
            project_root: 项目根目录
            
        Returns:
            list: 过滤后的文件列表
        """
        filtered_files = []
        
        for file_path in file_list:
            if self.should_include_file(file_path, project_root):
                filtered_files.append(file_path)
        
        return filtered_files
    
    def get_filter_stats(self, file_list, project_root=None):
        """获取过滤统计信息
        
        Args:
            file_list: 文件路径列表
            project_root: 项目根目录
            
        Returns:
            dict: 过滤统计信息
        """
        total_files = len(file_list)
        included_files = self.filter_files(file_list, project_root)
        excluded_count = total_files - len(included_files)
        
        return {
            'total_files': total_files,
            'included_files': len(included_files),
            'excluded_files': excluded_count,
            'inclusion_rate': len(included_files) / total_files if total_files > 0 else 0
        }
    
    def add_exclude_rule(self, rule_type, pattern):
        """添加排除规则
        
        Args:
            rule_type: 规则类型 ('dir', 'file', 'path')
            pattern: 模式字符串
        """
        if rule_type == 'dir':
            self.exclude_dirs.add(pattern)
        elif rule_type == 'file':
            self.exclude_files.add(pattern)
        elif rule_type == 'path':
            self.exclude_paths.add(pattern)
        else:
            raise FileDiscoveryError(f"未知的规则类型: {rule_type}")
        
        print(f"➕ 添加排除规则 ({rule_type}): {pattern}")
    
    def remove_exclude_rule(self, rule_type, pattern):
        """移除排除规则
        
        Args:
            rule_type: 规则类型 ('dir', 'file', 'path')
            pattern: 模式字符串
        """
        if rule_type == 'dir':
            self.exclude_dirs.discard(pattern)
        elif rule_type == 'file':
            self.exclude_files.discard(pattern)
        elif rule_type == 'path':
            self.exclude_paths.discard(pattern)
        else:
            raise FileDiscoveryError(f"未知的规则类型: {rule_type}")
        
        print(f"➖ 移除排除规则 ({rule_type}): {pattern}")
