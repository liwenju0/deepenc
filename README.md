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

#### 方式1: 自动初始化（推荐）

```python
# 在您的项目中，只需要一行初始化
import deepenc

# 自动初始化 - 系统会自动查找配置文件
deepenc.auto_initialize()

# 现在可以正常导入，系统会自动处理加密/解密
import onnxruntime as ort
from src import grpc_main, nsfw_image_censor

# 系统自动判断并处理加密文件
```

#### 方式2: 手动配置

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

## 🔧 核心功能

### 🚀 智能启动系统

- **自动初始化**: `deepenc.auto_initialize()` - 自动发现配置文件
- **快速启动**: `deepenc.quick_start()` - 智能降级启动
- **手动配置**: `deepenc.initialize()` - 精确控制配置
- **生命周期管理**: 完整的启动、运行、关闭流程

### 🏗️ 简化构建流程

- **一键构建**: `python -m deepenc build` - 自动发现和加密
- **智能过滤**: 自动排除测试、文档等非核心文件
- **入口点保护**: 确保入口文件不被加密
- **灵活配置**: 支持自定义过滤规则和构建选项

### 🔐 企业级安全

- **多级授权**: 硬件授权 → 许可证文件 → 环境变量
- **AES 加密**: 使用 AES-CFB 模式，平衡安全性和性能
- **部分加密**: 大文件只加密前 10MB，大幅提升性能
- **安全降级**: 授权失败时优雅降级，不影响系统运行

### 📊 性能优化

- **智能缓存**: 解密内容智能缓存，提高访问速度
- **内存管理**: 大文件使用临时文件，优化内存使用
- **并发处理**: 支持多线程并发解密
- **资源清理**: 自动清理临时文件和缓存

## 📋 命令行工具

### 构建命令

```bash
# 构建项目
python -m deepenc build

# 指定入口点
python -m deepenc build --entry-point src/main.py

# 指定项目路径
python -m deepenc build --project /path/to/project

# 详细输出
python -m deepenc build --verbose
```

### 管理命令

```bash
# 扫描项目文件
python -m deepenc scan

# 查看系统状态
python -m deepenc status

# 清理构建目录
python -m deepenc clean

# 验证构建结果
python -m deepenc verify
```

## 🔌 API 接口

### 基本接口

```python
import deepenc

# 自动初始化（推荐）
system = deepenc.auto_initialize()

# 手动初始化
system = deepenc.initialize(module_config)

# 快速启动
system = deepenc.quick_start()

# 检查状态
if deepenc.is_initialized():
    print("系统已启动")

# 关闭系统
deepenc.shutdown()
```

### 构建接口

```python
from deepenc.builders import ProjectBuilder

# 创建构建器
builder = ProjectBuilder('/path/to/project')

# 构建项目
report = builder.build_project()

# 扫描项目
scan_report = builder.scan_project()
```

### 发现接口

```python
from deepenc.discovery import FileScanner, FileFilter

# 创建扫描器
scanner = FileScanner('/path/to/project')

# 自定义过滤规则
filter_rules = {
    'exclude_dirs': ['tests', 'docs'],
    'exclude_files': ['*.pyc', '__pycache__']
}

# 应用过滤器
scanner.file_filter = FileFilter(filter_rules)

# 发现文件
python_files = scanner.discover_python_files()
onnx_files = scanner.discover_onnx_files()
```

## 📚 文档

- [快速开始指南](docs/quickstart.md) - 5分钟上手
- [API 文档](docs/api.md) - 完整的接口参考
- [架构设计](docs/architecture.md) - 系统架构详解
- [最佳实践](docs/best_practices.md) - 开发和使用建议
- [配置参考](docs/configuration.md) - 配置选项详解

## 🎯 使用场景

### 1. 软件分发

- **商业软件**: 保护核心算法和业务逻辑
- **开源项目**: 保护专有模块和模型
- **SaaS 服务**: 保护客户端代码和配置

### 2. 模型保护

- **AI 模型**: 保护训练好的 ONNX 模型
- **算法实现**: 保护核心算法代码
- **配置文件**: 保护敏感配置信息

### 3. 企业部署

- **内部系统**: 保护企业内部工具和脚本
- **客户部署**: 保护交付给客户的代码
- **云服务**: 保护云端的业务逻辑

## 🚀 部署示例

### Docker 部署

```dockerfile
FROM python:3.9-slim

# 安装依赖
RUN pip install deepenc onnxruntime

# 复制加密项目
COPY build/ /app/
WORKDIR /app

# 设置环境变量
ENV ENCRYPTION_KEY=your-production-key

# 启动应用
CMD ["python", "main.py"]
```

### Kubernetes 部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deepenc-app
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: deepenc-app
        image: your-registry/deepenc-app:latest
        env:
        - name: ENCRYPTION_KEY
          valueFrom:
            secretKeyRef:
              name: deepenc-secret
              key: encryption-key
```

## 🔧 开发环境

### 安装开发依赖

```bash
# 克隆仓库
git clone https://github.com/your-repo/deepenc.git
cd deepenc

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
python -m pytest tests/
```

### 项目结构

```
deepenc/
├── deepenc/              # 核心代码
├── tests/                # 测试代码
├── docs/                 # 文档
├── examples/             # 示例代码
├── setup.py             # 安装脚本
├── pyproject.toml       # 项目配置
└── README.md            # 项目说明
```

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 贡献方式

1. **报告问题**: 在 GitHub Issues 中报告 bug 或提出建议
2. **提交代码**: Fork 项目并提交 Pull Request
3. **改进文档**: 帮助完善文档和示例
4. **分享经验**: 在 Discussions 中分享使用经验

### 开发规范

- 遵循 PEP 8 代码风格
- 添加适当的测试用例
- 更新相关文档
- 使用清晰的提交信息

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和用户！

## 📞 联系我们

- **GitHub**: [https://github.com/your-repo/deepenc](https://github.com/your-repo/deepenc)
- **文档**: [https://deepenc.readthedocs.io/](https://deepenc.readthedocs.io/)
- **问题反馈**: [GitHub Issues](https://github.com/your-repo/deepenc/issues)
- **讨论交流**: [GitHub Discussions](https://github.com/your-repo/deepenc/discussions)

---

**DeepEnc** - 让 Python 项目加密分发变得简单而强大 🚀
