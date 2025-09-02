#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
授权和密钥管理

重新实现的授权系统，支持硬件授权和环境变量密钥管理。
遵循 Linux 内核的模块化设计理念。
"""

import os
import ctypes
import ctypes.util
from pathlib import Path
from .errors import AuthenticationError, LicenseError, KeyError


class HardwareAuth:
    """硬件授权实现
    
    完全按照原项目 io_util.py 的实现方式。
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
        """初始化授权库"""
        try:
            # 按照原项目的方式导入 hexie_auth
            from . import hexie_auth
            self.ukey_handler = hexie_auth.Auth(self.timeout)
            print(f"✅ 成功初始化硬件授权: hexie_auth.Auth({self.timeout})")
            
        except Exception as err:
            print(f"Failed to import hexie_auth: {err}. Ukey is not available!")
            self.ukey_handler = None
    
    def read_license_from_ukey(self, device_type='wd'):
        """从硬件设备读取许可证
        
        完全按照原项目的方法调用。
        
        Args:
            device_type: 设备类型，默认 'wd'
            
        Returns:
            str: 许可证字符串，失败返回空字符串
        """
        if not self.ukey_handler:
            return ""
        
        try:
            # 按照原项目的方式调用
            license_str = self.ukey_handler.ReadLicenseFromUkey(device_type)
            print(f"Get license from ukey! {len(license_str)}")
            return license_str
            
        except Exception as err:
            print(f"Failed to read license from ukey! {err}")
            return ""
    
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
    
    统一管理密钥获取，支持硬件授权和环境变量。
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
        
        完全按照原项目 io_util.py 的逻辑：
        1. 如果启用硬件授权，从硬件获取
        2. 否则从许可证文件获取
        3. 最后从环境变量获取
        
        Returns:
            str: 加密密钥
        """
        # 如果启用硬件授权
        if self.hardware_auth:
            key = self._get_key_from_hardware()
            if key:
                return key
        
        # 从许可证文件获取
        key = self._get_key_from_license_file()
        if key:
            return key
        
        # 从环境变量获取
        key = self._get_key_from_environment()
        if key:
            return key
        
        print("❌ 无法获取加密密钥")
        return None
    
    def _get_key_from_hardware(self):
        """从硬件授权获取密钥"""
        try:
            # 读取硬件许可证
            license_str = self.hardware_auth.read_license_from_ukey('wd')
            if not license_str:
                return None
            
            # 根据授权模式处理许可证
            auth_mode = os.environ.get("AUTH_MODE", "DEV")
            
            if auth_mode == 'DEV':
                # 开发模式：直接使用前16位
                return license_str[:16] if len(license_str) >= 16 else None
            else:
                # 生产模式：解密许可证
                decrypted_license = self.hardware_auth.decrypt_license(license_str)
                return decrypted_license[:16] if len(decrypted_license) >= 16 else None
                
        except Exception as e:
            print(f"从硬件获取密钥失败: {e}")
            return None
    
    def _get_key_from_license_file(self):
        """从许可证文件获取密钥"""
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
                return license_str[:16] if len(license_str) >= 16 else None
            
            return None
            
        except Exception as e:
            print(f"从许可证文件获取密钥失败: {e}")
            return None
    
    def _get_key_from_environment(self):
        """从环境变量获取密钥"""
        try:
            # 按照原项目的方式，只检查 AUTH_CODE
            key = os.environ.get('AUTH_CODE')
            if key and len(key) >= 16:
                return key[:32]  # 最多取32位
            
            return None
            
        except Exception as e:
            print(f"从环境变量获取密钥失败: {e}")
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
        
        # 按照原项目的逻辑判断来源
        if self.hardware_auth and os.environ.get("AUTH_MODE", "DEV") != 'DEV':
            return "hardware"
        elif os.path.exists('/data/appdatas/inference/license.dat'):
            return "license_file"
        elif os.environ.get('AUTH_CODE'):
            return "environment"
        else:
            return "unknown"
