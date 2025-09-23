#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能模块加载器

实现智能的 Python 模块导入，自动处理加密/非加密模块。
遵循 Linux 内核的模块加载机制设计。
"""

import importlib.abc
import importlib.machinery
import os
import sys

from ..core.auth import AuthManager
from ..core.crypto import AESCrypto
from ..core.errors import DecryptionError, LoaderError


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

    def register_encrypted_module(self, module_name, encrypted_file_path):
        """注册加密模块

        Args:
            module_name: 模块名称 (如 'src.grpc_main')
            encrypted_file_path: 加密文件路径
        """
        self.encrypted_modules[module_name] = encrypted_file_path
        print(f"🔐 {module_name}")

    def find_spec(self, fullname, path, target=None):
        """查找模块规范

        借鉴 Python 标准库实现，优先处理加密模块，
        找不到时回退到普通模块导入。

        Args:
            fullname: 完整模块名
            path: 搜索路径（相对导入时已解析）
            target: 目标模块

        Returns:
            ModuleSpec: 模块规范，如果不处理则返回 None
        """
        try:
            # 1. 检查是否是已知的加密模块
            if fullname in self.encrypted_modules:
                encrypted_path = self.encrypted_modules[fullname]
                return importlib.machinery.ModuleSpec(
                    fullname, self, origin=encrypted_path
                )

            # 2. 借鉴标准库：优先使用 path 参数，回退到 sys.path
            if path is not None:
                search_paths = path
                # 如果 path 是空列表，直接返回 None（没有搜索路径）
                if not search_paths:
                    return None
            else:
                search_paths = sys.path
            
            # 3. 自动发现加密版本（使用正确的搜索路径）
            encrypted_path = self._discover_encrypted_version(fullname, search_paths)
            if encrypted_path:
                print(f"🔐 {fullname} -> {os.path.basename(encrypted_path)}")
                # 自动注册发现的加密模块
                self.register_encrypted_module(fullname, encrypted_path)
                return importlib.machinery.ModuleSpec(
                    fullname, self, origin=encrypted_path
                )

            # 4. 没有找到加密版本，交给其他导入器处理
            return None

        except Exception as e:
            print(f"⚠️ {fullname}: {e}")
            return None

    def create_module(self, spec):
        """创建模块对象
        
        借鉴标准库实现，返回 None 让系统创建默认模块对象。
        
        Args:
            spec: 模块规范
            
        Returns:
            None: 让系统创建默认模块对象
        """
        # 返回 None 让系统使用默认的模块创建逻辑
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
                # 设置重要的模块属性
                self._setup_module_attributes(module, module_name)
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

            # 设置重要的模块属性
            self._setup_module_attributes(module, module_name, encrypted_file)

            # 执行解密后的代码
            exec(decrypted_content, module.__dict__)
            print(f"✅ {module_name}")

            return module

        except Exception as e:
            raise LoaderError(f"执行模块失败 {module_name}: {e}")

    def _setup_module_attributes(self, module, module_name, encrypted_file_path=None):
        """设置模块的重要属性

        确保加密模块具有与普通模块相同的属性。

        Args:
            module: 模块对象
            module_name: 模块名称
            encrypted_file_path: 加密文件路径
        """
        # 设置 __file__ 属性
        if encrypted_file_path:
            module.__file__ = encrypted_file_path
        else:
            # 如果没有文件路径，设置一个合理的默认值
            module.__file__ = f"<encrypted:{module_name}>"

        # 设置 __name__ 属性
        module.__name__ = module_name

        # 设置 __package__ 属性
        if "." in module_name:
            module.__package__ = ".".join(module_name.split(".")[:-1])
        else:
            module.__package__ = ""

        # 设置 __spec__ 属性
        try:
            module.__spec__ = importlib.machinery.ModuleSpec(
                module_name, self, origin=module.__file__
            )
        except Exception:
            # 如果创建 ModuleSpec 失败，保持原有的 __spec__
            pass

        # 设置 __cached__ 属性
        if encrypted_file_path:
            module.__cached__ = encrypted_file_path
        else:
            module.__cached__ = None

        # 设置其他重要的模块属性
        module.__loader__ = self
        module.__path__ = None  # 对于非包模块

        # 如果是包模块，设置 __path__
        # 检查文件名是否为 __init__ 文件来判断是否为包
        if (encrypted_file_path and 
            os.path.basename(encrypted_file_path).startswith('__init__')):
            try:
                package_path = os.path.dirname(encrypted_file_path)
                if os.path.isdir(package_path):
                    module.__path__ = [package_path]
            except Exception:
                pass

    def _discover_encrypted_version(self, module_name, search_paths):
        """自动发现加密版本

        借鉴标准库实现，在指定搜索路径中查找加密模块。

        Args:
            module_name: 模块名称
            search_paths: 搜索路径列表

        Returns:
            str: 加密文件路径，未找到返回 None
        """
        # 借鉴 FileFinder 的实现：提取模块的尾部名称
        tail_module = module_name.rpartition('.')[2]
        
        # 遍历搜索路径
        for search_path in search_paths:
            if not isinstance(search_path, str):
                continue
                
            # 检查各种可能的加密文件扩展名
            encrypted_extensions = [".encrypted", ".py.encrypted", ".enc"]
            
            for ext in encrypted_extensions:
                # 借鉴标准库 FileFinder：只使用 tail_module，不使用完整路径
                
                # 1. 先检查包形式 (__init__ 文件)
                base_path = os.path.join(search_path, tail_module)
                if os.path.isdir(base_path):
                    init_encrypted = os.path.join(base_path, '__init__' + ext)
                    if os.path.isfile(init_encrypted):
                        return init_encrypted
                
                # 2. 再检查单文件形式
                module_file_path = os.path.join(search_path, tail_module + ext)
                if os.path.isfile(module_file_path):
                    return module_file_path

        return None



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
            decrypted_data = self.crypto.decrypt_file(
                encrypted_file_path, encryption_key
            )

            # 转换为字符串
            return decrypted_data.decode("utf-8")

        except Exception as e:
            raise DecryptionError(f"解密模块失败 {encrypted_file_path}: {e}")

    def get_cache_info(self):
        """获取缓存信息

        Returns:
            dict: 缓存统计信息
        """
        return {
            "cached_modules": len(self._cache),
            "registered_modules": len(self.encrypted_modules),
            "cache_keys": list(self._cache.keys()),
            "registered_keys": list(self.encrypted_modules.keys()),
            "search_paths": [os.path.abspath(p) for p in sys.path if p and os.path.exists(p)],
        }

    def clear_cache(self):
        """清理缓存"""
        self._cache.clear()
        print("🧹 缓存已清理")

    def unregister_module(self, module_name):
        """取消注册模块

        Args:
            module_name: 要取消注册的模块名
        """
        if module_name in self.encrypted_modules:
            del self.encrypted_modules[module_name]
            print(f"❌ {module_name}")

        if module_name in self._cache:
            del self._cache[module_name]
            # 静默清理缓存


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

            print("🚀 加载器已安装")

            return self.loader

        except Exception as e:
            raise LoaderError(f"安装模块加载器失败: {e}")

    def uninstall_loader(self):
        """卸载智能模块加载器"""
        try:
            if self.loader and self.loader in sys.meta_path:
                sys.meta_path.remove(self.loader)
                print("❌ 加载器已卸载")

            if self._original_meta_path:
                sys.meta_path = self._original_meta_path.copy()
                # 静默恢复原始导入系统

            self.loader = None

        except Exception as e:
            print(f"⚠️ 卸载失败: {e}")

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
