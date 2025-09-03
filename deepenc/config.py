#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理

统一的配置管理系统。
"""

import os
import json
from pathlib import Path


class Config:
    """配置管理类"""
    
    # 默认配置
    DEFAULT_CONFIG = {
        'encryption': {
            'algorithm': 'AES-CFB',
            'key_length': 16,
            'partial_encryption': True,
            'enc_len': 1024 * 1024 * 10  # 10MB
        },
        'discovery': {
            'auto_scan': True,
            'exclude_dirs': [
                '.git', '__pycache__', 'build', 'dist', 'venv', 'env',
                'tests', 'test', 'docs', 'doc', 'examples', 'scripts'
            ],
            'exclude_files': [
                '__init__.py', 'setup.py', 'requirements.txt',
                '*.pyc', '*.pyo', '*.log', '*.tmp'
            ]
        },
        'performance': {
            'cache_enabled': True,
            'cache_size_mb': 100,
            'temp_cleanup': True
        },
        'logging': {
            'level': 'INFO',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    }
    
    def __init__(self, config_file=None):
        """初始化配置
        
        Args:
            config_file: 配置文件路径
        """
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_file:
            self.load_from_file(config_file)
        
        # 从环境变量覆盖配置
        self.load_from_env()
    
    def load_from_file(self, config_file):
        """从文件加载配置
        
        Args:
            config_file: 配置文件路径
        """
        try:
            config_path = Path(config_file)
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                
                # 深度合并配置
                self._deep_merge(self.config, file_config)
                print(f"✅ 加载配置文件: {config_file}")
            
        except Exception as e:
            print(f"⚠️ 加载配置文件失败: {e}")
    
    def load_from_env(self):
        """从环境变量加载配置"""
        env_mappings = {
            'ENCRYPT_CACHE_SIZE': ('performance', 'cache_size_mb'),
            'ENCRYPT_LOG_LEVEL': ('logging', 'level'),
            'ENCRYPT_ENC_LEN': ('encryption', 'enc_len'),
        }
        
        for env_var, (section, key) in env_mappings.items():
            value = os.environ.get(env_var)
            if value:
                try:
                    # 尝试转换类型
                    if key in ['cache_size_mb', 'enc_len']:
                        value = int(value)
                    
                    self.config[section][key] = value
                    print(f"✅ 环境变量配置: {env_var} = {value}")
                    
                except ValueError as e:
                    print(f"⚠️ 环境变量格式错误 {env_var}: {e}")
    
    def _deep_merge(self, base_dict, update_dict):
        """深度合并字典
        
        Args:
            base_dict: 基础字典
            update_dict: 更新字典
        """
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_merge(base_dict[key], value)
            else:
                base_dict[key] = value
    
    def get(self, section, key=None, default=None):
        """获取配置值
        
        Args:
            section: 配置段
            key: 配置键，None 表示获取整个段
            default: 默认值
            
        Returns:
            配置值
        """
        if key is None:
            return self.config.get(section, default)
        else:
            return self.config.get(section, {}).get(key, default)
    
    def set(self, section, key, value):
        """设置配置值
        
        Args:
            section: 配置段
            key: 配置键
            value: 配置值
        """
        if section not in self.config:
            self.config[section] = {}
        
        self.config[section][key] = value
    
    def save_to_file(self, config_file):
        """保存配置到文件
        
        Args:
            config_file: 配置文件路径
        """
        try:
            config_path = Path(config_file)
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            print(f"✅ 配置已保存: {config_file}")
            
        except Exception as e:
            print(f"❌ 保存配置失败: {e}")
    
    def to_dict(self):
        """转换为字典
        
        Returns:
            dict: 配置字典
        """
        return self.config.copy()


# 全局配置实例
_global_config = None


def get_config():
    """获取全局配置实例
    
    Returns:
        Config: 配置实例
    """
    global _global_config
    
    if _global_config is None:
        # 查找配置文件
        config_files = [
            'encrypt_config.json',
            'config/encrypt_config.json',
            'config/encryption_config.json'
        ]
        
        config_file = None
        for file_path in config_files:
            if os.path.exists(file_path):
                config_file = file_path
                break
        
        _global_config = Config(config_file)
    
    return _global_config


def reset_config():
    """重置全局配置"""
    global _global_config
    _global_config = None
