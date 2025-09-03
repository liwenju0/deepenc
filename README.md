# DeepEnc - Python 项目加密分发框架

一个简洁、强大的 Python 项目加密分发框架，遵循 **Linux 内核设计理念**，具有企业级安全性和性能。

## 🎯 设计理念

- **简洁性**: 遵循 Unix 哲学，每个组件只做一件事，做好一件事
- **透明性**: 开发者完全无感知的加密/解密过程
- **自动化**: 零配置，自动发现和处理所有文件
- **可靠性**: 优雅的错误处理和降级机制
- **模块化**: 清晰的模块边界，易于维护和扩展
- **安全性**: 确保关键文件（如 `src/grpc_main.py`）不被加密

## 🏗️ 架构概览

```
deepenc/
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
│   ├── project_builder.py  # 项目构建器（重构版）
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
cd /path/to/your/project
python -m deepenc build

# 指定自定义入口文件
python -m deepenc build --entry-point src/main.py

# 指定项目和入口文件
python -m deepenc build --project /path/to/project --entry-point src/app.py

# 查看构建结果
ls -la build/
```

### 3. 运行加密项目

```bash
# 进入构建目录
cd build

# 直接运行您的应用（启动方式由您决定）
python src/grpc_main.py  # 默认入口文件
# 或者
python main.py            # 自定义入口文件
```

### 4. 开发者无感知使用

```python
# 在您的项目中，只需要一行初始化
import deepenc
deepenc.bootstrap()

# 现在可以正常导入，系统会自动处理加密/解密
import onnxruntime as ort
from src import grpc_main, nsfw_image_censor

# 系统自动判断并处理加密文件
session = ort.InferenceSession('model/eros/eros.onnx')  # 自动解密（如果已加密）
grpc_main.start_server()                                # 自动解密导入（如果已加密）
```

## 🔒 安全特性

### 关键文件保护

- **入口点文件保护**: 指定的入口文件不会被加密，保持原始状态
- **智能文件过滤**: 自动识别并排除关键文件（如 `src/grpc_main.py`）
- **配置文件保护**: 配置文件自动包含到构建目录，确保项目完整性

框架自动保护以下文件不被加密：
- `src/grpc_main.py` - **gRPC主服务文件（重点保护）**
- `*.pyc` - Python字节码文件
- `__pycache__` - Python缓存目录
- `.git` - Git版本控制目录
- `build` - 构建输出目录
- `dist` - 分发目录
- `*.egg-info` - Python包信息

### 加密策略

- **选择性加密**: 只加密核心业务逻辑，保护关键服务文件
- **内存安全**: 解密内容只存在于内存中，不落盘
- **智能降级**: 加密文件不存在时自动使用普通文件

## 📋 功能特性

- ✅ **自动文件发现**: 零配置自动发现所有 Python 和 ONNX 文件
- ✅ **智能加密**: 自动判断文件类型并选择合适的加密方式
- ✅ **透明解密**: 运行时自动解密，开发者完全无感知
- ✅ **关键文件保护**: 自动排除 `src/grpc_main.py` 等关键文件
- ✅ **智能降级**: 加密文件不存在时自动使用普通文件
- ✅ **内存安全**: 解密内容只存在于内存中，不落盘
- ✅ **性能优化**: 智能缓存，避免重复解密
- ✅ **授权管理**: 集成硬件授权和环境变量密钥管理
- ✅ **CLI 工具**: 完善的命令行工具
- ✅ **错误处理**: 优雅的错误处理和回滚机制

## 🆕 最新功能特性 (v1.0.0)

### 入口点文件支持

- **自定义入口文件**: 支持指定项目入口Python文件，默认为 `src/grpc_main.py`
- **智能加密策略**: 入口文件不会被加密，保持原始状态便于调试和维护
- **CLI参数支持**: 新增 `--entry-point` 参数，支持绝对路径和相对路径

```bash
# 使用默认入口文件
python -m deepenc build

# 指定自定义入口文件
python -m deepenc build --entry-point src/main.py

# 指定项目和入口文件
python -m deepenc build --project /path/to/project --entry-point src/app.py
```

### 配置文件自动包含

- **智能发现**: 自动发现并复制项目中的配置文件
- **支持格式**: `.conf`, `.ini`, `.yaml`, `.yml`, `.json`, `.toml`, `.cfg`
- **目录结构**: 配置文件被复制到构建目录的 `conf/` 子目录中

### 构建目录结构优化

```
build/
├── main.py                    # 入口文件（未加密）
├── conf/                      # 配置文件目录
│   ├── app.conf
│   └── settings.yaml
├── config/                    # 加密配置
│   └── encryption_config.json
└── encrypted/                 # 加密文件
    ├── python/                # Python加密文件
    └── models/                # ONNX模型加密文件
```

## 🔧 安装指南

### 系统要求

- **Python**: 3.7+
- **操作系统**: Linux (推荐), macOS, Windows
- **内存**: 最少 512MB
- **磁盘空间**: 最少 100MB

### 依赖安装

#### 必需依赖

```bash
# 安装核心依赖
pip install pycrypto

# 如果需要 ONNX 支持
pip install onnxruntime

# 或者安装 GPU 版本
pip install onnxruntime-gpu
```

#### 可选依赖

```bash
# 性能监控
pip install psutil

# YAML 配置支持
pip install pyyaml

# 进度条显示
pip install tqdm
```

### 快速安装

#### 方式1: 直接使用

```bash
# 1. 进入您的项目目录
cd /path/to/your/project

# 2. 复制 deepenc 框架
cp -r /path/to/deepenc ./

# 3. 设置环境变量
export ENCRYPTION_KEY="your-16-char-key1"

# 4. 构建项目
python -m deepenc build

# 5. 运行项目（启动方式由您决定）
cd build && python src/grpc_main.py
```

#### 方式2: 作为子模块

```bash
# 1. 添加为 Git 子模块
git submodule add https://github.com/your-repo/deepenc.git deepenc

# 2. 初始化子模块
git submodule update --init --recursive

# 3. 按照方式1的步骤3-5执行
```

## 🔑 密钥配置

### 开发环境

```bash
# 使用环境变量（推荐）
export ENCRYPTION_KEY="dev-key-16chars"
export AUTH_MODE="DEV"

# 或者创建许可证文件
echo "dev-license-content-16chars" > license.dat
```

### 生产环境

#### 方式1: 硬件授权（最安全）

```bash
# 启用硬件授权模式
export AUTH_MODE="PROD"

# 确保硬件授权库可用
# 框架会自动查找以下路径：
# - /usr/local/lib/libhexie_auth.so
# - /usr/lib/libhexie_auth.so
# - ./libhexie_auth.so
```

#### 方式2: 许可证文件

```bash
# 创建生产许可证文件
echo "production-license-content" > /data/appdatas/inference/license.dat
chmod 600 /data/appdatas/inference/license.dat
```

#### 方式3: 环境变量

```bash
# 设置生产密钥
export ENCRYPTION_KEY="prod-key-32-characters-long"
export AUTH_MODE="PROD"
```

## 🏗️ 重构后的架构设计

### 核心改进

基于 **Linus Torvalds 的设计理念**，我们对 `ProjectBuilder` 进行了全面重构：

#### 1. **单一职责原则**
- 将原来的巨型类分解为多个专门组件
- 每个类只负责一个特定功能，职责清晰明确

#### 2. **模块化设计**
- `BuildEnvironment`: 构建环境管理
- `FileProcessor`: 文件处理抽象基类
- `PythonProcessor`: Python文件加密
- `ONNXProcessor`: ONNX模型加密
- `ConfigGenerator`: 配置文件生成

#### 3. **策略模式**
- 使用抽象基类 `FileProcessor` 支持不同类型的文件处理
- 遵循开闭原则，新增文件类型只需继承此类

#### 4. **组合优于继承**
- `ProjectBuilder` 作为主协调器，组合各个功能组件
- 通过依赖注入管理组件生命周期

### 架构组件

```
ProjectBuilder (主协调器)
├── BuildEnvironment (构建环境管理)
├── FileProcessor (文件处理抽象)
│   ├── PythonProcessor (Python文件加密)
│   └── ONNXProcessor (ONNX模型加密)
├── ConfigGenerator (配置文件生成)
└── FileScanner (文件发现)
```

## 🔧 高级配置

### 自定义文件过滤

```python
from deepenc.builders import ProjectBuilder
from deepenc.discovery import FileFilter

# 创建自定义过滤器
custom_rules = {
    'exclude_dirs': ['my_test_dir'],
    'exclude_files': ['config.py'],
    'include_files': ['important.py']  # 强制包含
}

# 使用自定义规则构建
builder = ProjectBuilder()
builder.scanner.file_filter = FileFilter(custom_rules)
build_report = builder.build_project()
```

### 手动初始化系统

```python
import deepenc

# 手动配置模块映射
module_config = {
    'src.main': 'encrypted/python/src/main.py.encrypted',
    'src.utils': 'encrypted/python/src/utils.py.encrypted'
}

# 初始化系统
system = deepenc.initialize(module_config)

# 现在可以正常导入加密模块
from src import main, utils
```

## 📚 使用示例

### 基本使用

```python
#!/usr/bin/env python3
import deepenc

def main():
    # 启动加密系统
    system = deepenc.bootstrap()
    
    # 正常导入模块（系统会自动处理加密/解密）
    from src import grpc_main, nsfw_image_censor
    
    # 启动gRPC服务
    grpc_main.start_server()

if __name__ == '__main__':
    main()
```

### 高级使用

```python
#!/usr/bin/env python3
import deepenc
from deepenc.builders import ProjectBuilder

def build_and_run():
    # 1. 构建项目
    builder = ProjectBuilder()
    report = builder.build_project()
    
    print(f"构建完成: {report['encryption']['encrypted_python_modules']} 个模块")
    
    # 2. 启动系统
    system = deepenc.bootstrap()
    
    # 3. 运行应用
    from src import grpc_main
    grpc_main.start_server()

if __name__ == '__main__':
    build_and_run()
```

## 🚀 部署指南

### Docker 部署

#### Dockerfile 示例

```dockerfile
FROM python:3.8-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install -r requirements.txt

# 复制加密项目
COPY build/ /app/
WORKDIR /app

# 设置环境变量
ENV AUTH_MODE=PROD
ENV ENCRYPTION_KEY=your-production-key

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import deepenc; print('OK')" || exit 1

# 启动应用（启动方式由您决定）
CMD ["python", "src/grpc_main.py"]
```

#### docker-compose.yml 示例

```yaml
version: '3.8'

services:
  encrypted-app:
    build: .
    environment:
      - AUTH_MODE=PROD
      - ENCRYPTION_KEY=${ENCRYPTION_KEY}
    volumes:
      - ./data:/data
      - ./logs:/app/logs
    ports:
      - "8080:8080"
    restart: unless-stopped
```

### 生产环境部署

```bash
#!/bin/bash
# deploy.sh

set -e

echo "🚀 开始部署..."

# 检查构建结果
if [ ! -f "build/src/grpc_main.py" ]; then
    echo "❌ 关键文件不存在"
    exit 1
fi

# 部署到目标环境
rsync -av build/ production_server:/app/

# 重启服务
ssh production_server "systemctl restart your-app"

echo "✅ 部署完成"
```

## 🛠️ 故障排除

### 常见问题

#### 1. 加密密钥错误

```
❌ 授权系统初始化失败: 无法获取有效的加密密钥
```

**解决方案:**
- 检查环境变量 `ENCRYPTION_KEY` 是否设置
- 确保密钥长度为 16、24 或 32 字符
- 检查许可证文件是否存在且可读

#### 2. 关键文件被加密

```
❌ src/grpc_main.py 被意外加密
```

**解决方案:**
- 框架已自动保护关键文件，检查排除规则
- 确保 `src/grpc_main.py` 在排除列表中
- 重新构建项目

#### 3. 模块导入失败

```
❌ 执行模块失败 src.main: 解密模块失败
```

**解决方案:**
- 检查加密文件是否存在
- 验证密钥是否正确
- 确保文件权限正确

### 调试模式

```bash
# 启用详细输出
python -m deepenc build --verbose

# 或者在代码中
import deepenc
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 系统诊断

```bash
# 诊断系统状态
python -m deepenc status

# 检查文件完整性
python -m deepenc verify

# 性能分析
python -m deepenc profile
```

## 📊 性能特性

### 关键指标

- **启动时间**: 系统初始化时间 < 100ms
- **解密时间**: 单个模块解密时间 < 50ms
- **内存占用**: 缓存内存占用 < 100MB
- **缓存命中率**: > 90%

### 性能监控

```python
# 获取性能统计
system = deepenc.get_system()
if system:
    perf_stats = system.get_performance_stats()
    print(f"解密操作数: {perf_stats.get('decrypt_count', 0)}")
    print(f"缓存命中率: {perf_stats.get('cache_hit_rate', 0):.2%}")
```

## 🔐 安全最佳实践

### 1. 密钥管理

```bash
# ✅ 生产环境：使用硬件授权
export AUTH_MODE="PROD"

# ✅ 开发环境：使用环境变量
export ENCRYPTION_KEY="dev-key-16chars"
export AUTH_MODE="DEV"
```

### 2. 文件权限

```bash
# 设置适当的文件权限
chmod 600 license.dat              # 许可证文件只有所有者可读写
chmod 644 *.py.encrypted          # 加密文件只读
chmod 755 src/grpc_main.py        # 关键服务文件可执行
```

### 3. 安全清理

```python
# 构建后自动清理敏感文件
def secure_cleanup():
    # 删除原始源码文件（保留关键文件）
    for py_file in source_files:
        if 'grpc_main.py' not in str(py_file):
            os.remove(py_file)
```

## 🧪 测试指南

### 运行测试

```bash
# 测试框架功能
cd deepenc
python test_framework.py

# 运行示例
python examples/basic_usage.py
python examples/advanced_usage.py
```

### 验证构建

```bash
# 验证构建结果
python -m deepenc verify

# 检查关键文件保护
ls -la build/src/grpc_main.py  # 应该存在且未加密
```

## 📚 完整文档

- **[快速开始](docs/quickstart.md)** - 5分钟上手指南
- **[API 文档](docs/api.md)** - 完整的API参考
- **[架构设计](docs/architecture.md)** - 系统架构详解
- **[最佳实践](docs/best_practices.md)** - 开发和生产最佳实践

## 🤝 贡献指南

我们欢迎社区贡献！请查看 [贡献指南](docs/contributing.md) 了解如何参与项目开发。

## 🆘 获取帮助

如果遇到问题，请：

1. **查看日志**: 启用详细日志输出
   ```bash
   python -m deepenc build --verbose
   ```

2. **运行诊断**: 使用内置诊断工具
   ```bash
   python -m deepenc status
   ```

3. **检查示例**: 运行示例代码
   ```bash
   python deepenc/examples/basic_usage.py
   ```

4. **查看文档**: 阅读详细文档
   - [快速开始](docs/quickstart.md)
   - [API 文档](docs/api.md)
   - [架构设计](docs/architecture.md)
   - [最佳实践](docs/best_practices.md)

## 🔄 更新日志

### v1.0.0 (2025-09-03)

#### 🆕 新功能
- **入口点文件支持**: 允许用户指定项目入口Python文件，默认为 `src/grpc_main.py`
- **配置文件自动包含**: 自动发现并复制项目中的配置文件到构建目录
- **构建目录结构优化**: 重新设计构建输出目录结构，更加清晰和实用

#### 🔧 改进
- **CLI增强**: 新增 `--entry-point` 参数，支持自定义入口文件
- **智能文件过滤**: 改进文件排除逻辑，确保入口文件不被加密
- **构建报告优化**: 增强构建报告内容，提供更详细的构建信息

#### 🐛 修复
- **参数传递错误**: 修复 `ProjectBuilder` 构造函数参数不匹配问题
- **格式化错误**: 修复构建摘要中的格式化字符串错误
- **向后兼容性**: 确保现有项目配置和CLI命令的兼容性

#### 📁 构建目录结构
```
build/
├── main.py                    # 入口文件（未加密）
├── conf/                      # 配置文件目录
├── config/                    # 加密配置
│   └── encryption_config.json
└── encrypted/                 # 加密文件
    ├── python/                # Python加密文件
    └── models/                # ONNX模型加密文件
```

查看 [CHANGELOG.md](CHANGELOG.md) 了解完整的版本更新信息。

## 📄 许可证

MIT License

---

**DeepEnc** - 让 Python 项目加密变得简单而安全 🚀
