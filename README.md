# Python 项目加密分发框架

一个简洁、强大的 Python 项目加密分发框架，具有 Linux 架构审美。

## 🎯 设计理念

- **简洁性**: 遵循 Unix 哲学，每个组件只做一件事，做好一件事
- **透明性**: 开发者完全无感知的加密/解密过程
- **自动化**: 零配置，自动发现和处理所有文件
- **可靠性**: 优雅的错误处理和降级机制
- **模块化**: 清晰的模块边界，易于维护和扩展

## 🏗️ 架构概览

```
encrypt/
├── core/                    # 核心加密引擎
│   ├── __init__.py
│   ├── crypto.py           # AES 加密实现
│   ├── auth.py             # 授权和密钥管理
│   └── errors.py           # 异常定义
├── discovery/               # 文件发现系统
│   ├── __init__.py
│   ├── scanner.py          # 文件扫描器
│   └── filters.py          # 过滤规则
├── loaders/                 # 动态加载系统
│   ├── __init__.py
│   ├── module_loader.py    # Python 模块加载器
│   └── onnx_loader.py      # ONNX 模型加载器
├── builders/                # 构建系统
│   ├── __init__.py
│   ├── project_builder.py  # 项目构建器
│   └── packager.py         # 打包器
├── cli/                     # 命令行工具
│   ├── __init__.py
│   ├── commands.py         # CLI 命令
│   └── main.py             # 入口点
├── utils/                   # 工具函数
│   ├── __init__.py
│   ├── fs.py               # 文件系统工具
│   └── logger.py           # 日志系统
├── __init__.py             # 框架入口
├── bootstrap.py            # 系统启动器
└── config.py               # 配置管理
```

## 🚀 快速开始

### 1. 设置环境

```bash
# 安装依赖
pip install pycrypto onnxruntime

# 设置加密密钥（开发环境）
export ENCRYPTION_KEY="1234567890123456"  # 16字符密钥
```

### 2. 构建加密项目

```bash
# 在项目根目录执行
cd /data/aliyun_code/nsfwimagecensor
python -m encrypt build

# 查看构建结果
ls -la build/
```

### 3. 运行加密项目

```bash
# 进入构建目录
cd build

# 运行项目（自动启动加密系统）
python run.py
```

### 4. 开发者无感知使用

```python
# 在您的项目中，只需要一行初始化
import encrypt
encrypt.bootstrap()

# 现在可以正常导入，系统会自动处理加密/解密
import onnxruntime as ort
from src import grpc_main, nsfw_image_censor

# 系统自动判断并处理加密文件
session = ort.InferenceSession('model/eros/eros.onnx')  # 自动解密（如果已加密）
grpc_main.start_server()                                # 自动解密导入（如果已加密）
```

### 5. 测试框架

```bash
# 测试框架功能
cd encrypt
python test_framework.py

# 运行示例
python examples/basic_usage.py
python examples/advanced_usage.py
```

## 📋 功能特性

- ✅ **自动文件发现**: 零配置自动发现所有 Python 和 ONNX 文件
- ✅ **智能加密**: 自动判断文件类型并选择合适的加密方式
- ✅ **透明解密**: 运行时自动解密，开发者完全无感知
- ✅ **智能降级**: 加密文件不存在时自动使用普通文件
- ✅ **内存安全**: 解密内容只存在于内存中，不落盘
- ✅ **性能优化**: 智能缓存，避免重复解密
- ✅ **授权管理**: 集成硬件授权和环境变量密钥管理
- ✅ **CLI 工具**: 完善的命令行工具
- ✅ **错误处理**: 优雅的错误处理和回滚机制

## 🔧 高级配置

详细配置选项请参考 [配置文档](docs/configuration.md)

## 📖 API 文档

详细 API 文档请参考 [API 文档](docs/api.md)

## 🤝 贡献指南

详细贡献指南请参考 [贡献文档](docs/contributing.md)

## 📄 许可证

MIT License
