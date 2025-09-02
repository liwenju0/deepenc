#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模块主入口

支持 python -m encrypt 的调用方式。
"""

from .cli.main import main

if __name__ == '__main__':
    exit(main())
