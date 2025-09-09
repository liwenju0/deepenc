#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志系统

提供统一的日志功能。
"""

import logging
import sys
from pathlib import Path


def setup_logger(name="encrypt", level=logging.INFO, log_file=None):
    """设置日志系统

    Args:
        name: 日志器名称
        level: 日志级别
        log_file: 日志文件路径，None 表示只输出到控制台

    Returns:
        logging.Logger: 日志器实例
    """
    logger = logging.getLogger(name)

    # 避免重复添加处理器
    if logger.handlers:
        return logger

    logger.setLevel(level)

    # 创建格式器
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 文件处理器
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
