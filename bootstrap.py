#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统启动器

统一的系统启动和初始化入口。
遵循 Linux 内核的启动流程设计。
"""

import sys
import os
from pathlib import Path
from loaders.module_loader import ModuleLoaderManager
from loaders.onnx_loader import ONNXLoaderManager
from core.errors import LoaderError, AuthenticationError


class EncryptionSystem:
    """加密系统
    
    统一管理加密模块和模型的加载。
    """
    
    def __init__(self):
        """初始化加密系统"""
        self.module_manager = ModuleLoaderManager()
        self.onnx_manager = ONNXLoaderManager()
        self._is_initialized = False
        self._initialization_error = None
    
    def initialize(self, module_config=None):
        """初始化加密系统
        
        Args:
            module_config: 模块配置字典
                {
                    'module_name': 'encrypted_file_path',
                    ...
                }
        
        Returns:
            bool: 初始化是否成功
        """
        if self._is_initialized:
            print("⚠️ 加密系统已经初始化")
            return True
        
        try:
            print("🚀 正在启动加密系统...")
            
            # 1. 初始化 ONNX 加载器
            self._initialize_onnx_loader()
            
            # 2. 初始化模块加载器
            self._initialize_module_loader(module_config)
            
            self._is_initialized = True
            self._print_startup_info()
            
            return True
            
        except Exception as e:
            self._initialization_error = e
            print(f"❌ 加密系统启动失败: {e}")
            return False
    
    def _initialize_onnx_loader(self):
        """初始化 ONNX 加载器"""
        try:
            self.onnx_manager.install_loader()
        except Exception as e:
            # ONNX 加载器失败不影响系统启动
            print(f"⚠️ ONNX 加载器初始化失败: {e}")
    
    def _initialize_module_loader(self, module_config):
        """初始化模块加载器
        
        Args:
            module_config: 模块配置
        """
        try:
            self.module_manager.install_loader(module_config)
        except Exception as e:
            raise LoaderError(f"模块加载器初始化失败: {e}")
    
    def _print_startup_info(self):
        """打印启动信息"""
        print("✅ 加密系统启动成功")
        print("")
        print("🎯 系统特性:")
        print("  - 自动识别加密/非加密模块")
        print("  - 自动识别加密/非加密模型")
        print("  - 智能降级到普通导入/加载")
        print("  - 开发者完全无感知")
        print("")
        
        # 显示加载器状态
        module_status = "✅" if self.module_manager.is_installed() else "❌"
        onnx_status = "✅" if self.onnx_manager.is_installed() else "❌"
        
        print("📊 加载器状态:")
        print(f"  {module_status} Python 模块加载器")
        print(f"  {onnx_status} ONNX 模型加载器")
        print("")
    
    def shutdown(self):
        """关闭加密系统"""
        try:
            print("🛑 正在关闭加密系统...")
            
            # 卸载加载器
            self.module_manager.uninstall_loader()
            self.onnx_manager.uninstall_loader()
            
            self._is_initialized = False
            print("✅ 加密系统已关闭")
            
        except Exception as e:
            print(f"⚠️ 关闭加密系统时发生错误: {e}")
    
    def get_status(self):
        """获取系统状态
        
        Returns:
            dict: 系统状态信息
        """
        return {
            'initialized': self._is_initialized,
            'initialization_error': str(self._initialization_error) if self._initialization_error else None,
            'module_loader_installed': self.module_manager.is_installed(),
            'onnx_loader_installed': self.onnx_manager.is_installed(),
            'module_cache_info': self.module_manager.get_loader().get_cache_info() if self.module_manager.get_loader() else {},
            'onnx_cache_info': self.onnx_manager.get_loader().get_cache_info() if self.onnx_manager.get_loader() else {}
        }
    
    def clear_caches(self):
        """清理所有缓存"""
        try:
            if self.module_manager.get_loader():
                self.module_manager.get_loader().clear_cache()
            
            if self.onnx_manager.get_loader():
                self.onnx_manager.get_loader().clear_cache()
            
            print("🧹 所有缓存已清理")
            
        except Exception as e:
            print(f"⚠️ 清理缓存时发生错误: {e}")


# 全局系统实例
_encryption_system = None


def initialize(module_config=None):
    """初始化加密系统
    
    这是框架的主要入口点。
    
    Args:
        module_config: 模块配置字典
        
    Returns:
        EncryptionSystem: 加密系统实例
        
    Raises:
        LoaderError: 初始化失败
    """
    global _encryption_system
    
    if _encryption_system is None:
        _encryption_system = EncryptionSystem()
    
    if not _encryption_system.initialize(module_config):
        raise LoaderError("加密系统初始化失败")
    
    return _encryption_system


def bootstrap(module_config=None):
    """启动加密系统
    
    initialize() 的别名，提供更直观的接口。
    
    Args:
        module_config: 模块配置字典
        
    Returns:
        EncryptionSystem: 加密系统实例
    """
    return initialize(module_config)


def get_system():
    """获取加密系统实例
    
    Returns:
        EncryptionSystem: 系统实例，未初始化则返回 None
    """
    return _encryption_system


def shutdown():
    """关闭加密系统"""
    global _encryption_system
    
    if _encryption_system:
        _encryption_system.shutdown()
        _encryption_system = None


def is_initialized():
    """检查系统是否已初始化
    
    Returns:
        bool: 是否已初始化
    """
    return _encryption_system is not None and _encryption_system._is_initialized


def auto_initialize():
    """自动初始化
    
    尝试从构建目录自动加载配置并初始化系统。
    """
    try:
        # 查找配置文件
        possible_config_paths = [
            Path.cwd() / 'config' / 'encryption_config.json',
            Path.cwd() / 'build' / 'config' / 'encryption_config.json',
            Path(__file__).parent.parent / 'config' / 'encryption_config.json'
        ]
        
        config_data = None
        for config_path in possible_config_paths:
            if config_path.exists():
                import json
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                print(f"📄 加载配置文件: {config_path}")
                break
        
        if config_data:
            module_config = config_data.get('module_mapping', {})
            return initialize(module_config)
        else:
            print("⚠️ 未找到配置文件，使用默认初始化")
            return initialize()
            
    except Exception as e:
        print(f"❌ 自动初始化失败: {e}")
        raise LoaderError(f"自动初始化失败: {e}")


# 便利函数
def quick_start():
    """快速启动
    
    尝试自动初始化，如果失败则使用默认配置。
    """
    try:
        return auto_initialize()
    except Exception:
        print("🔄 自动初始化失败，使用默认配置")
        return initialize()
