#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行工具

提供完善的 CLI 接口。
"""

from cli.commands import EncryptCLI
from cli.main import main

__all__ = [
    'EncryptCLI',
    'main'
]
