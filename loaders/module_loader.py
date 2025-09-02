#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能模块加载器

实现智能的 Python 模块导入，自动处理加密/非加密模块。
遵循 Linux 内核的模块加载机制设计。
"""

import sys
import importlib.abc
import importlib.machinery
import os
from pathlib import Path
from ..core.crypto import AESCrypto
from ..core.auth import AuthManager
from ..core.errors import LoaderError, DecryptionError


class SmartModuleLoader(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    """智能模块加载器
    
    自动处理加密和非加密的 Python 模块导入。
    实现了完全透明的加密模块加载机制。
    """
    
    def __init__(self):
        """初始化模块加载器"""
        self.crypto = AESCrypto()
        self.auth_manager = AuthManager()
        self.encrypted_modules = {}
        self._cache = {}  # 解密后的代码缓存
        self._project_root = self._find_project_root()
    
    def register_encrypted_module(self, module_name, encrypted_file_path):
        """注册加密模块
        
        Args:
            module_name: 模块名称 (如 'src.grpc_main')
            encrypted_file_path: 加密文件路径
        """
        self.encrypted_modules[module_name] = encrypted_file_path
        print(f"🔐 注册加密模块: {module_name}")
    
    def find_spec(self, fullname, path, target=None):
        """查找模块规范
        
        智能判断模块是否加密，实现自动降级。
        
        Args:
            fullname: 完整模块名
            path: 搜索路径
            target: 目标模块
            
        Returns:
            ModuleSpec: 模块规范，如果不处理则返回 None
        """
        try:
            # 1. 检查是否是已知的加密模块
            if fullname in self.encrypted_modules:
                return importlib.machinery.ModuleSpec(
                    fullname, 
                    self, 
                    origin=f"<encrypted:{fullname}>"
                )
            
            # 2. 自动发现加密版本
            encrypted_path = self._discover_encrypted_version(fullname)
            if encrypted_path:
                # 自动注册发现的加密模块
                self.register_encrypted_module(fullname, encrypted_path)
                return importlib.machinery.ModuleSpec(
                    fullname, 
                    self, 
                    origin=f"<auto_encrypted:{fullname}>"
                )
            
            # 3. 检查是否存在普通版本（降级处理）
            if self._has_normal_version(fullname):
                print(f"📦 降级到普通导入: {fullname}")
                return None  # 让系统使用默认导入器
            
            # 4. 都不存在，交给其他导入器处理
            return None
            
        except Exception as e:
            print(f"⚠️ 查找模块规范失败 {fullname}: {e}")
            return None
    
    def exec_module(self, module):
        """执行模块
        
        解密并执行加密的模块。
        
        Args:
            module: 要执行的模块对象
        """
        module_name = module.__name__
        
        try:
            # 检查缓存
            if module_name in self._cache:
                exec(self._cache[module_name], module.__dict__)
                return module
            
            # 获取加密文件路径
            encrypted_file = self.encrypted_modules.get(module_name)
            if not encrypted_file:
                raise LoaderError(f"模块 {module_name} 未找到加密版本")
            
            # 解密模块
            decrypted_content = self._decrypt_module(encrypted_file)
            
            # 缓存解密后的内容
            self._cache[module_name] = decrypted_content
            
            # 执行解密后的代码
            exec(decrypted_content, module.__dict__)
            print(f"✅ 成功加载加密模块: {module_name}")
            
            return module
            
        except Exception as e:
            raise LoaderError(f"执行模块失败 {module_name}: {e}")
    
    def _discover_encrypted_version(self, module_name):
        """自动发现加密版本
        
        Args:
            module_name: 模块名称
            
        Returns:
            str: 加密文件路径，未找到返回 None
        """
        # 将模块名转换为可能的文件路径
        possible_paths = self._module_name_to_paths(module_name)
        
        for base_path in possible_paths:
            # 检查各种可能的加密文件扩展名
            encrypted_extensions = ['.encrypted', '.py.encrypted', '.enc']
            
            for ext in encrypted_extensions:
                encrypted_path = base_path + ext
                if os.path.exists(encrypted_path):
                    print(f"🔍 自动发现加密模块: {module_name} -> {encrypted_path}")
                    return encrypted_path
        
        return None
    
    def _has_normal_version(self, module_name):
        """检查是否存在普通版本
        
        Args:
            module_name: 模块名称
            
        Returns:
            bool: 是否存在普通版本
        """
        possible_paths = self._module_name_to_paths(module_name)
        
        for base_path in possible_paths:
            # 检查 .py 文件
            py_path = base_path + '.py'
            if os.path.exists(py_path):
                return True
            
            # 检查包目录（包含 __init__.py）
            if os.path.isdir(base_path):
                init_path = os.path.join(base_path, '__init__.py')
                if os.path.exists(init_path):
                    return True
        
        return False
    
    def _module_name_to_paths(self, module_name):
        """将模块名转换为可能的文件路径
        
        Args:
            module_name: 模块名称
            
        Returns:
            list: 可能的文件路径列表
        """
        module_parts = module_name.split('.')
        possible_paths = []
        
        # 方案1: 直接路径
        direct_path = os.path.join(self._project_root, *module_parts)
        possible_paths.append(direct_path)
        
        # 方案2: 添加常见的源码目录前缀
        common_prefixes = ['src', 'lib', 'modules', 'packages']
        for prefix in common_prefixes:
            prefixed_path = os.path.join(self._project_root, prefix, *module_parts)
            possible_paths.append(prefixed_path)
        
        # 方案3: 如果第一个部分不是已知前缀，尝试作为包名
        if module_parts[0] not in common_prefixes:
            package_path = os.path.join(self._project_root, *module_parts)
            if package_path not in possible_paths:
                possible_paths.append(package_path)
        
        return possible_paths
    
    def _find_project_root(self):
        """查找项目根目录
        
        Returns:
            str: 项目根目录路径
        """
        current_dir = Path.cwd()
        
        # 查找包含项目标识文件的目录
        project_markers = ['.git', 'setup.py', 'pyproject.toml', 'requirements.txt']
        
        for parent in [current_dir] + list(current_dir.parents):
            for marker in project_markers:
                if (parent / marker).exists():
                    return str(parent)
        
        # 如果找不到，使用当前目录
        return str(current_dir)
    
    def _decrypt_module(self, encrypted_file_path):
        """解密模块文件
        
        Args:
            encrypted_file_path: 加密文件路径
            
        Returns:
            str: 解密后的 Python 代码
            
        Raises:
            DecryptionError: 解密失败
        """
        try:
            # 获取加密密钥
            encryption_key = self.auth_manager.get_key()
            
            # 解密文件
            decrypted_data = self.crypto.decrypt_file(encrypted_file_path, encryption_key)
            
            # 转换为字符串
            return decrypted_data.decode('utf-8')
            
        except Exception as e:
            raise DecryptionError(f"解密模块失败 {encrypted_file_path}: {e}")
    
    def get_cache_info(self):
        """获取缓存信息
        
        Returns:
            dict: 缓存统计信息
        """
        return {
            'cached_modules': len(self._cache),
            'registered_modules': len(self.encrypted_modules),
            'cache_keys': list(self._cache.keys()),
            'registered_keys': list(self.encrypted_modules.keys())
        }
    
    def clear_cache(self):
        """清理缓存"""
        self._cache.clear()
        print("🧹 模块缓存已清理")
    
    def unregister_module(self, module_name):
        """取消注册模块
        
        Args:
            module_name: 要取消注册的模块名
        """
        if module_name in self.encrypted_modules:
            del self.encrypted_modules[module_name]
            print(f"❌ 取消注册模块: {module_name}")
        
        if module_name in self._cache:
            del self._cache[module_name]
            print(f"🧹 清理模块缓存: {module_name}")


class ModuleLoaderManager:
    """模块加载器管理器
    
    管理智能模块加载器的生命周期。
    """
    
    def __init__(self):
        self.loader = None
        self._original_meta_path = None
    
    def install_loader(self, encrypted_modules=None):
        """安装智能模块加载器
        
        Args:
            encrypted_modules: 预定义的加密模块映射
        """
        try:
            self.loader = SmartModuleLoader()
            
            # 注册预定义的加密模块
            if encrypted_modules:
                for module_name, encrypted_file in encrypted_modules.items():
                    self.loader.register_encrypted_module(module_name, encrypted_file)
            
            # 保存原始的 meta_path
            self._original_meta_path = sys.meta_path.copy()
            
            # 安装加载器（最高优先级）
            sys.meta_path.insert(0, self.loader)
            
            print("🚀 智能模块加载器已安装")
            print("🎯 系统将自动处理加密/非加密模块")
            
            return self.loader
            
        except Exception as e:
            raise LoaderError(f"安装模块加载器失败: {e}")
    
    def uninstall_loader(self):
        """卸载智能模块加载器"""
        try:
            if self.loader and self.loader in sys.meta_path:
                sys.meta_path.remove(self.loader)
                print("❌ 智能模块加载器已卸载")
            
            if self._original_meta_path:
                sys.meta_path = self._original_meta_path.copy()
                print("🔄 已恢复原始导入系统")
            
            self.loader = None
            
        except Exception as e:
            print(f"⚠️ 卸载模块加载器时发生错误: {e}")
    
    def get_loader(self):
        """获取加载器实例
        
        Returns:
            SmartModuleLoader: 加载器实例
        """
        return self.loader
    
    def is_installed(self):
        """检查加载器是否已安装
        
        Returns:
            bool: 是否已安装
        """
        return self.loader is not None and self.loader in sys.meta_path
