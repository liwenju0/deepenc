#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 项目加密分发框架

一个简洁、强大的 Python 项目加密分发框架，具有 Linux 架构审美。

设计理念:
- 简洁性: 遵循 Unix 哲学，每个组件只做一件事，做好一件事
- 透明性: 开发者完全无感知的加密/解密过程
- 自动化: 零配置，自动发现和处理所有文件
- 可靠性: 优雅的错误处理和降级机制
- 模块化: 清晰的模块边界，易于维护和扩展

Usage:
    import encrypt
    encrypt.bootstrap()  # 启动加密系统
    
    # 现在可以正常导入，系统会自动处理加密/解密
    from your_module import your_function

Author: AI Assistant
Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "AI Assistant"
__license__ = "MIT"

# 导出主要接口
from .bootstrap import bootstrap, initialize
from .core import EncryptionError, AuthenticationError
from .builders.project_builder import ProjectBuilder

# 设置默认的日志级别
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = [
    'bootstrap',
    'initialize', 
    'ProjectBuilder',
    'EncryptionError',
    'AuthenticationError',
    '__version__'
]
