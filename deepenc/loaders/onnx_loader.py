#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能 ONNX 加载器

实现智能的 ONNX 模型加载，自动处理加密/非加密模型。
遵循 Linux 内核的设备驱动模型设计。
"""

import os
import tempfile
import atexit
from pathlib import Path
from ..core.crypto import AESCrypto
from ..core.auth import AuthManager
from ..core.errors import LoaderError, DecryptionError

try:
    import onnxruntime as ort
except ImportError:
    print("⚠️ onnxruntime 未安装，ONNX 加载器功能将不可用")
    ort = None


class SmartONNXLoader:
    """智能 ONNX 加载器
    
    自动处理加密和非加密的 ONNX 模型加载。
    实现了完全透明的加密模型加载机制。
    """
    
    def __init__(self):
        """初始化 ONNX 加载器"""
        if ort is None:
            raise LoaderError("onnxruntime 未安装，无法使用 ONNX 加载器")
        
        self.crypto = AESCrypto()
        self.auth_manager = AuthManager()
        self._temp_files = set()
        self._model_cache = {}  # 模型会话缓存
        self._original_inference_session = ort.InferenceSession
        
        # 注册退出时清理
        atexit.register(self.cleanup_all)
    
    def load_model(self, model_path, **kwargs):
        """智能加载模型
        
        自动判断模型是否加密，选择合适的加载方式。
        
        Args:
            model_path: 模型文件路径
            **kwargs: 传递给 InferenceSession 的参数
            
        Returns:
            onnxruntime.InferenceSession: 推理会话
        """
        try:
            # 1. 检查是否是已知的加密模型
            if self._is_known_encrypted_model(model_path):
                return self._load_encrypted_model(model_path, **kwargs)
            
            # 2. 自动发现加密版本
            encrypted_path = self._discover_encrypted_version(model_path)
            if encrypted_path:
                print(f"🔍 自动发现加密模型: {model_path} -> {encrypted_path}")
                return self._load_encrypted_model(encrypted_path, **kwargs)
            
            # 3. 降级到普通加载
            print(f"📦 使用普通加载: {model_path}")
            return self._original_inference_session(model_path, **kwargs)
            
        except Exception as e:
            raise LoaderError(f"加载模型失败 {model_path}: {e}")
    
    def _is_known_encrypted_model(self, model_path):
        """检查是否是已知的加密模型
        
        Args:
            model_path: 模型路径
            
        Returns:
            bool: 是否是加密模型
        """
        return (model_path.endswith('.encrypt') or 
                '.encrypt' in model_path or
                model_path.endswith('.enc') or
                model_path in self._model_cache)
    
    def _discover_encrypted_version(self, model_path):
        """自动发现加密版本
        
        Args:
            model_path: 原始模型路径
            
        Returns:
            str: 加密模型路径，未找到返回 None
        """
        model_path_obj = Path(model_path)
        
        # 检查同目录下的各种加密版本
        possible_encrypted_paths = [
            # 标准加密扩展名
            model_path_obj.with_suffix('.onnx.encrypt'),
            model_path_obj.with_suffix('.encrypt'),
            model_path_obj.with_suffix('.enc'),
            
            # 同名加密文件
            model_path_obj.parent / f"{model_path_obj.stem}.encrypt",
            model_path_obj.parent / f"{model_path_obj.stem}.onnx.encrypt",
            model_path_obj.parent / f"{model_path_obj.stem}.enc",
            
            # 加密目录中的文件
            model_path_obj.parent / 'encrypted' / model_path_obj.name,
            model_path_obj.parent / 'encrypted' / f"{model_path_obj.name}.encrypt",
        ]
        
        for encrypted_path in possible_encrypted_paths:
            if encrypted_path.exists():
                return str(encrypted_path)
        
        return None
    
    def _load_encrypted_model(self, encrypted_path, **kwargs):
        """加载加密模型
        
        Args:
            encrypted_path: 加密模型路径
            **kwargs: 传递给 InferenceSession 的参数
            
        Returns:
            onnxruntime.InferenceSession: 推理会话
        """
        try:
            # 检查缓存
            cache_key = f"{encrypted_path}:{hash(str(sorted(kwargs.items())))}"
            if cache_key in self._model_cache:
                print(f"📋 使用缓存的模型会话: {encrypted_path}")
                return self._model_cache[cache_key]
            
            # 获取加密密钥
            encryption_key = self.auth_manager.get_key()
            
            # 解密模型到内存
            decrypted_model = self.crypto.decrypt_file(encrypted_path, encryption_key)
            
            # 创建临时文件
            tmp_file = tempfile.NamedTemporaryFile(
                delete=False, 
                suffix='.onnx',
                prefix='decrypted_model_'
            )
            tmp_file.write(decrypted_model)
            tmp_file.close()
            
            self._temp_files.add(tmp_file.name)
            
            # 创建推理会话
            session = self._original_inference_session(tmp_file.name, **kwargs)
            
            # 缓存会话
            self._model_cache[cache_key] = session
            
            # 将清理方法附加到会话
            session._encrypted_temp_file = tmp_file.name
            session._cleanup = lambda: self._cleanup_file(tmp_file.name)
            
            print(f"✅ 成功加载加密模型: {encrypted_path}")
            return session
            
        except Exception as e:
            raise LoaderError(f"加载加密模型失败 {encrypted_path}: {e}")
    
    def _cleanup_file(self, tmp_file):
        """清理单个临时文件
        
        Args:
            tmp_file: 临时文件路径
        """
        if tmp_file in self._temp_files:
            try:
                os.unlink(tmp_file)
                self._temp_files.remove(tmp_file)
                print(f"🧹 清理临时文件: {os.path.basename(tmp_file)}")
            except Exception as e:
                print(f"⚠️ 清理临时文件失败 {tmp_file}: {e}")
    
    def cleanup_all(self):
        """清理所有临时文件"""
        temp_count = len(self._temp_files)
        for tmp_file in list(self._temp_files):
            self._cleanup_file(tmp_file)
        
        if temp_count > 0:
            print(f"🧹 清理了 {temp_count} 个临时文件")
    
    def get_cache_info(self):
        """获取缓存信息
        
        Returns:
            dict: 缓存统计信息
        """
        return {
            'cached_models': len(self._model_cache),
            'temp_files': len(self._temp_files),
            'cache_keys': list(self._model_cache.keys()),
            'temp_file_paths': list(self._temp_files)
        }
    
    def clear_cache(self):
        """清理模型缓存"""
        self._model_cache.clear()
        print("🧹 模型缓存已清理")


class ONNXLoaderManager:
    """ONNX 加载器管理器
    
    管理智能 ONNX 加载器的生命周期。
    """
    
    def __init__(self):
        self.loader = None
        self._is_patched = False
    
    def install_loader(self):
        """安装智能 ONNX 加载器"""
        try:
            if ort is None:
                print("⚠️ onnxruntime 未安装，跳过 ONNX 加载器安装")
                return None
            
            self.loader = SmartONNXLoader()
            
            # 替换 InferenceSession
            ort.InferenceSession = self.loader.load_model
            self._is_patched = True
            
            print("🚀 智能 ONNX 加载器已安装")
            print("🎯 系统将自动处理加密/非加密模型")
            
            return self.loader
            
        except Exception as e:
            raise LoaderError(f"安装 ONNX 加载器失败: {e}")
    
    def uninstall_loader(self):
        """卸载智能 ONNX 加载器"""
        try:
            if self.loader and self._is_patched:
                ort.InferenceSession = self.loader._original_inference_session
                self._is_patched = False
                print("❌ 智能 ONNX 加载器已卸载")
            
            if self.loader:
                self.loader.cleanup_all()
                self.loader = None
            
        except Exception as e:
            print(f"⚠️ 卸载 ONNX 加载器时发生错误: {e}")
    
    def get_loader(self):
        """获取加载器实例
        
        Returns:
            SmartONNXLoader: 加载器实例
        """
        return self.loader
    
    def is_installed(self):
        """检查加载器是否已安装
        
        Returns:
            bool: 是否已安装
        """
        return self.loader is not None and self._is_patched
