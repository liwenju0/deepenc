#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


# 读取README文件
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()


# 读取requirements文件
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [
            line.strip() for line in fh if line.strip() and not line.startswith("#")
        ]


setup(
    name="deepenc",
    version="1.0.0",
    author="liwenju0",
    author_email="liwenjudetiankong@126.com",
    maintainer="liwenju0",
    maintainer_email="liwenjudetiankong@126.com",
    description="Python 项目加密分发框架 - 一个简洁、强大的 Python 项目加密分发框架",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/liwenju0/deepenc",
    project_urls={
        "Homepage": "https://github.com/liwenju0/deepenc",
        "Documentation": "https://deepenc.readthedocs.io/",
        "Repository": "https://github.com/liwenju0/deepenc.git",
        "Bug Tracker": "https://github.com/liwenju0/deepenc/issues",
        "Release Notes": "https://github.com/liwenju0/deepenc/releases",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
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
    keywords=["encryption", "distribution", "python", "security", "onnx"],
    include_package_data=True,
    package_data={
        "deepenc.core": ["*.so", "*.pyd", "*.dll", "*.dylib"],
    },
    exclude_package_data={
        "*": ["*.pyc", "*.pyo", "*.pyd", "__pycache__", "*.dll", "*.dylib"],
    },
)
