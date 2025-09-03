#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异常定义

定义框架中使用的所有异常类型。
遵循 Python 异常层次结构的最佳实践。
"""


class EncryptionError(Exception):
    """加密相关异常的基类"""
    pass


class DecryptionError(EncryptionError):
    """解密失败异常"""
    pass


class AuthenticationError(Exception):
    """认证相关异常的基类"""
    pass


class LicenseError(AuthenticationError):
    """许可证相关异常"""
    pass


class KeyError(AuthenticationError):
    """密钥相关异常"""
    pass


class FileDiscoveryError(Exception):
    """文件发现异常"""
    pass


class BuildError(Exception):
    """构建异常"""
    pass


class LoaderError(Exception):
    """加载器异常"""
    pass
