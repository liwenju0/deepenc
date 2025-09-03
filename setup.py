#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装脚本

支持传统的 setuptools 安装方式。
建议优先使用 pyproject.toml。
"""

from setuptools import setup, find_packages
import os

# 读取 README 文件
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# 读取 requirements.txt
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="deepenc",
    version="1.0.0",
    author="AI Assistant",
    author_email="ai@example.com",
    description="Python 项目加密分发框架 - 一个简洁、强大的 Python 项目加密分发框架，具有 Linux 架构审美",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-repo/deepenc",
    project_urls={
        "Bug Tracker": "https://github.com/your-repo/deepenc/issues",
        "Documentation": "https://deepenc.readthedocs.io/",
        "Source Code": "https://github.com/your-repo/deepenc",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security :: Cryptography",
        "Topic :: System :: Distributed Computing",
    ],
    package_dir={"": "."},
    packages=find_packages(where=".", exclude=["tests*", "test_*", "examples*", "docs*", ".git*", ".cursor*", "build*", "dist*", "*.egg-info*"]),
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "deepenc=deepenc.cli.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="encryption, distribution, python, security, onnx",
    license="MIT",
)
