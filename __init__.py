#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 项目加密分发框架

这个文件是为了向后兼容性而保留的。
实际的包内容在 deepenc/ 目录中。
"""

# 导入实际的包
from deepenc import *

# 重新导出所有内容
__all__ = deepenc.__all__
