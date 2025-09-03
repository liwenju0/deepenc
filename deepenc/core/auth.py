#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
授权管理器

提供统一的授权验证接口。
遵循 Linux 内核的安全设计原则。
"""

import os
import hashlib
import hmac
from pathlib import Path
from .errors import AuthenticationError


class HardwareAuth:
    """硬件授权实现
    
    完全按照原项目 io_util.py 的实现方式。
    采用动态加载器避免循环导入问题。
    """
    
    def __init__(self, timeout=10):
        """初始化硬件授权
        
        Args:
            timeout: 超时时间（秒）
        """
        self.timeout = timeout
        self.ukey_handler = None
        self._initialize_auth_lib()
    
    def _initialize_auth_lib(self):
        """初始化授权库
        
        采用动态加载器方式，避免循环导入问题。
        """
        try:
            # 使用动态加载器获取 Auth 类
            from .hexie_auth_loader import get_auth_class
            
            AuthClass = get_auth_class()
            if AuthClass:
                # 按照原项目的方式创建 Auth 实例
                self.ukey_handler = AuthClass(self.timeout)
                print(f"✅ 成功初始化硬件授权: hexie_auth.Auth({self.timeout})")
            else:
                print("❌ 无法获取 Auth 类")
                self.ukey_handler = None
                
        except Exception as err:
            import traceback
            print(f"❌ 初始化硬件授权失败: {err}")
            print(f"详细错误信息: {traceback.format_exc()}")
            self.ukey_handler = None

    
    def get_device_id(self):
        """获取设备 ID
        
        完全按照原项目的方法调用。
        
        Returns:
            str: 设备 ID，失败返回空字符串
        """
        if not self.ukey_handler:
            return ""
        
        try:
            # 按照原项目的方式调用
            device_id = self.ukey_handler.GetDeviceID()
            return device_id
            
        except Exception as err:
            print(f"Failed to get device ID: {err}")
            return ""
    
    def decrypt_license(self, encrypted_license):
        """解密许可证
        
        完全按照原项目的方法调用。
        
        Args:
            encrypted_license: 加密的许可证字符串
            
        Returns:
            str: 解密后的许可证内容
        """
        if not self.ukey_handler:
            return encrypted_license
        
        try:
            # 按照原项目的方式调用
            decrypted_license = self.ukey_handler.DecLicense(encrypted_license)
            return decrypted_license
            
        except Exception as err:
            print(f"Failed to decrypt license: {err}")
            return encrypted_license


class AuthManager:
    """授权管理器
    
    统一管理密钥获取，支持硬件授权和许可证文件。
    遵循 Linux 的优先级和降级机制。
    """
    
    def __init__(self):
        """初始化授权管理器"""
        self.hardware_auth = None
        self.encryption_key = None
        self._initialize()
    
    def _initialize(self):
        """初始化授权系统"""
        try:
            # 检查是否启用硬件授权
            auth_mode = os.environ.get("AUTH_MODE", "DEV")
            
            if auth_mode != 'DEV':
                print("🔐 启用硬件授权模式")
                self.hardware_auth = HardwareAuth()
            else:
                print("🔧 使用开发模式")
            
            # 获取加密密钥
            self.encryption_key = self._get_encryption_key()
            
            if self.encryption_key:
                print("✅ 授权系统初始化成功")
            else:
                raise AuthenticationError("无法获取有效的加密密钥")
                
        except Exception as e:
            raise AuthenticationError(f"授权系统初始化失败: {e}")
    
    def _get_encryption_key(self):
        """获取加密密钥
        
        从许可证文件获取密钥，支持开发和生产两种模式。
        
        Returns:
            str: 加密密钥
        """
        # 从许可证文件获取
        key = self._get_key_from_license_file()
        if key:
            return key
        
        print("❌ 无法获取加密密钥")
        return None
    
    
    def _get_key_from_license_file(self):
        """从许可证文件获取密钥
        
        DEV 模式：许可证文件内容即为原始未加密的 key。
        非 DEV 模式：许可证文件内容为加密数据，需要通过 hardware_auth 解密得到 key。
        """
        try:
            # 如果有硬件授权，尝试获取设备特定的许可证文件
            if self.hardware_auth:
                try:
                    device_id = self.hardware_auth.get_device_id()
                    license_file = '/data/appdatas/inference/{}.license'.format(device_id)
                    if not os.path.exists(license_file):
                        license_file = '/data/appdatas/inference/license.dat'
                except:            
                    license_file = '/data/appdatas/inference/license.dat'
            else:
                license_file = '/data/appdatas/inference/license.dat'
            
            # 尝试读取许可证文件
            if os.path.exists(license_file):
                with open(license_file, 'r', encoding='utf-8') as f:
                    license_str = f.read()
                print(f"Read license from {license_file}")

                license_str = license_str.strip()
                auth_mode = os.environ.get("AUTH_MODE", "DEV")

                if auth_mode == 'DEV':
                    # 开发模式：直接使用文件中的原始 key
                    return license_str if license_str else None
                else:
                    # 非开发模式：需要通过硬件授权解密
                    if not self.hardware_auth:
                        print("非 DEV 模式缺少 hardware_auth，无法解密许可证")
                        return None
                    decrypted = self.hardware_auth.decrypt_license(license_str)
                    decrypted = decrypted.strip() if decrypted else ""
                    return decrypted if decrypted else None
            
            return None
            
        except Exception as e:
            print(f"从许可证文件获取密钥失败: {e}")
            return None
    
    def get_key(self):
        """获取当前的加密密钥
        
        Returns:
            str: 加密密钥
            
        Raises:
            AuthenticationError: 无法获取密钥
        """
        if not self.encryption_key:
            raise AuthenticationError("加密密钥未初始化")
        
        return self.encryption_key
    
    def verify_authorization(self):
        """验证授权状态
        
        Returns:
            bool: 授权是否有效
        """
        try:
            key = self.get_key()
            return key is not None and len(key) >= 16
        except Exception:
            return False
    
    def get_auth_info(self):
        """获取授权信息
        
        Returns:
            dict: 授权信息
        """
        return {
            'auth_mode': os.environ.get("AUTH_MODE", "DEV"),
            'hardware_auth_available': self.hardware_auth is not None,
            'key_source': self._get_key_source(),
            'key_length': len(self.encryption_key) if self.encryption_key else 0,
            'authorization_valid': self.verify_authorization()
        }
    
    def _get_key_source(self):
        """获取密钥来源"""
        if not self.encryption_key:
            return "none"
        
        auth_mode = os.environ.get("AUTH_MODE", "DEV")
        if self.hardware_auth and auth_mode != 'DEV':
            return "hardware_decrypted_license"
        elif os.path.exists('/data/appdatas/inference/license.dat'):
            return "license_file"
        else:
            return "unknown"
