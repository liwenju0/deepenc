# DeepEnc - Python 项目加密分发框架

一个简洁、强大的 Python 项目加密分发框架，遵循 **Linux 内核设计理念**，具有企业级安全性和性能。

## 🎯 设计理念

- **简洁性**: 遵循 Unix 哲学，每个组件只做一件事，做好一件事
- **透明性**: 开发者完全无感知的加密/解密过程
- **自动化**: 零配置，自动发现和处理所有文件
- **可靠性**: 优雅的错误处理和降级机制
- **模块化**: 清晰的模块边界，易于维护和扩展
- **安全性**: 确保关键文件（如 `src/grpc_main.py`）不被加密
- **企业级**: 支持硬件授权和许可证管理

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
pip install deepenc

# 设置开发环境
make dev-setup

# 或者手动设置授权
mkdir -p /data/appdatas/inference
echo "your-16-char-key" > /data/appdatas/inference/license.dat
export AUTH_MODE="DEV"

# 设置zip包密码（可选）
export UNZIP_CODE="your_custom_password"
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
system = deepenc.auto_initialize()

# 现在可以正常导入，系统会自动处理加密/解密
import onnxruntime as ort
from src import grpc_main, utils

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

## 🧠 工作原理

### 核心架构

DeepEnc 采用**透明代理**的设计模式，通过 Python 的导入钩子（Import Hooks）机制实现完全透明的加密模块加载。

```
用户代码导入 → 智能加载器拦截 → 判断是否加密 → 解密/直接加载 → 返回模块对象
```

#### 系统架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户应用层                                │
├─────────────────────────────────────────────────────────────────┤
│  from src import utils  │  import onnxruntime as ort           │
│  session = ort.InferenceSession('model.onnx')                  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DeepEnc 智能加载层                           │
├─────────────────────────────────────────────────────────────────┤
│  SmartModuleLoader    │    SmartONNXLoader                     │
│  ├─ find_spec()       │    ├─ load_model()                     │
│  ├─ exec_module()     │    ├─ _load_encrypted_model()          │
│  └─ 缓存管理          │    └─ 生命周期管理                     │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      核心加密引擎                               │
├─────────────────────────────────────────────────────────────────┤
│  AuthManager          │    AESCrypto                           │
│  ├─ 硬件授权          │    ├─ AES-CFB 加密                     │
│  ├─ 许可证验证        │    ├─ 部分加密优化                      │
│  └─ 密钥管理          │    └─ 性能优化                        │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      文件系统层                                 │
├─────────────────────────────────────────────────────────────────┤
│  加密文件 (.encrypted)  │  内存缓存          │  许可证文件      │
│  ├─ Python 模块        │  ├─ 解密后的代码    │  ├─ license.dat  │
│  └─ ONNX 模型          │  └─ 推理会话缓存    │  └─ 硬件授权     │
└─────────────────────────────────────────────────────────────────┘
```

### Module Loader 工作原理

#### 1. 导入拦截机制

```python
# 用户代码
from src import utils  # 普通导入

# 系统内部处理流程：
# 1. SmartModuleLoader.find_spec() 拦截导入请求
# 2. 检查模块是否在加密列表中
# 3. 如果是加密模块，返回自定义的 ModuleSpec
# 4. 如果不是，返回 None（让系统正常处理）
```

#### 2. 智能解密流程

```python
class SmartModuleLoader:
    def find_spec(self, fullname, path, target=None):
        """查找模块规范 - 决定如何处理模块导入"""
        if fullname in self.encrypted_modules:
            # 加密模块：返回自定义规范
            return ModuleSpec(
                name=fullname,
                loader=self,  # 使用自定义加载器
                origin=self.encrypted_modules[fullname]
            )
        return None  # 非加密模块：让系统正常处理
    
    def create_module(self, spec):
        """创建模块对象"""
        return None  # 使用默认模块创建
    
    def exec_module(self, module):
        """执行模块代码 - 核心解密逻辑"""
        module_name = module.__name__
        
        # 1. 检查缓存
        if module_name in self._cache:
            decrypted_content = self._cache[module_name]
        else:
            # 2. 获取加密文件路径
            encrypted_file = self.encrypted_modules.get(module_name)
            
            # 3. 解密文件内容
            decrypted_content = self._decrypt_module(encrypted_file)
            
            # 4. 缓存解密后的内容
            self._cache[module_name] = decrypted_content
        
        # 5. 执行解密后的代码
        exec(decrypted_content, module.__dict__)
```

#### 3. 缓存机制

```python
# 内存缓存：避免重复解密
self._cache = {
    'src.utils': 'def hello():\n    print("Hello World")',
    'src.main': 'def main():\n    print("Main function")'
}
```

### ONNX Loader 工作原理

#### 1. 模型加载拦截

```python
# 用户代码
import onnxruntime as ort
session = ort.InferenceSession('model.onnx')  # 普通加载

# 系统内部处理：
# 1. SmartONNXLoader 拦截 onnxruntime.InferenceSession
# 2. 检查模型文件是否加密
# 3. 如果是加密模型，直接在内存中解密
# 4. 使用内存中的二进制数据创建 InferenceSession
```

#### 2. 智能解密流程

```python
class SmartONNXLoader:
    def load_model(self, model_path, **kwargs):
        """智能加载模型"""
        if self._is_encrypted_model(model_path):
            # 加密模型：直接在内存中解密
            return self._load_encrypted_model(model_path, **kwargs)
        else:
            # 普通模型：直接加载
            return self._original_inference_session(model_path, **kwargs)
    
    def _load_encrypted_model(self, encrypted_path, **kwargs):
        """加载加密模型 - 内存中直接解密"""
        # 1. 检查缓存
        cache_key = f"{encrypted_path}:{hash(str(sorted(kwargs.items())))}"
        if cache_key in self._model_cache:
            return self._model_cache[cache_key]
        
        # 2. 获取解密密钥
        key = self.auth_manager.get_key()
        
        # 3. 解密模型到内存（不写临时文件）
        decrypted_model = self.crypto.decrypt_file(encrypted_path, key)
        
        # 4. 直接从内存中的二进制数据创建推理会话
        session = self._original_inference_session(decrypted_model, **kwargs)
        
        # 5. 缓存会话
        self._model_cache[cache_key] = session
        
        return session
```

#### 3. 生命周期管理

```python
# 内存缓存管理
import atexit

class ONNXLoaderManager:
    def __init__(self):
        atexit.register(self.cleanup_all)  # 程序退出时自动清理
    
    def cleanup_all(self):
        """清理所有缓存"""
        self._model_cache.clear()  # 清理内存中的模型缓存
        print("🧹 模型缓存已清理")
```

### 安全机制

#### 1. 授权验证

```python
class AuthManager:
    def get_key(self):
        """获取解密密钥"""
        if self.auth_mode == "DEV":
            # 开发模式：从许可证文件读取
            return self._load_license_key()
        elif self.auth_mode == "PROD":
            # 生产模式：硬件授权验证
            return self._hardware_auth_key()
        else:
            raise AuthenticationError("无效的授权模式")
```

#### 2. 加密算法

```python
class AESCrypto:
    def encrypt(self, data, key):
        """AES-CFB 加密"""
        cipher = AES.new(key, AES.MODE_CFB)
        return cipher.encrypt(data)
    
    def decrypt(self, encrypted_data, key):
        """AES-CFB 解密"""
        cipher = AES.new(key, AES.MODE_CFB)
        return cipher.decrypt(encrypted_data)
```

### 性能优化

#### 1. 智能缓存策略

- **内存缓存**: 直接缓存解密后的代码字符串和推理会话
- **智能缓存**: 避免重复解密，提升性能
- **自动清理**: 程序退出时自动清理缓存

#### 2. 部分加密

```python
# 大文件只加密前10MB，提升性能
if file_size > 10 * 1024 * 1024:  # 10MB
    # 只加密前10MB
    encrypted_data = encrypt(data[:10*1024*1024])
    # 剩余部分保持原样
    return encrypted_data + data[10*1024*1024:]
```

#### 3. 错误处理

```python
class SmartModuleLoader:
    def exec_module(self, module):
        try:
            # 解密和加载逻辑
            pass
        except Exception as e:
            raise LoaderError(f"执行模块失败 {module_name}: {e}")
```

### 实际工作流程示例

#### Python 模块加载流程

```python
# 1. 用户代码
from src import utils

# 2. 系统拦截 (SmartModuleLoader.find_spec)
# 检查 'src.utils' 是否在加密列表中
# 如果在：返回自定义 ModuleSpec
# 如果不在：返回 None（系统正常处理）

# 3. 模块创建 (SmartModuleLoader.create_module)
# 返回 None，使用默认模块创建

# 4. 代码执行 (SmartModuleLoader.exec_module)
# 读取加密文件：encrypted/python/src/utils.py.encrypted
# 解密数据：AES-CFB 解密
# 执行代码：exec(decrypted_content, module.__dict__)

# 5. 缓存结果
# 将解密后的代码字符串缓存到内存中
```

#### ONNX 模型加载流程

```python
# 1. 用户代码
import onnxruntime as ort
session = ort.InferenceSession('model.onnx')

# 2. 系统拦截 (SmartONNXLoader.load_model)
# 检查 'model.onnx' 是否为加密文件
# 如果是：直接在内存中解密
# 如果不是：直接使用原文件

# 3. 解密过程
# 读取加密文件：model.onnx.encrypted
# 解密数据：AES-CFB 解密到内存
# 缓存会话：避免重复解密

# 4. 模型加载
# 使用内存中的二进制数据创建 InferenceSession
# 返回正常的 ONNX 会话对象

# 5. 生命周期管理
# 程序退出时自动清理内存缓存
```

#### 性能优化策略

```python
# Python模块：内存缓存解密后的代码字符串
module_cache = {
    'src.utils': 'def hello():\n    print("Hello World")'
}

# ONNX模型：内存缓存推理会话
model_cache = {
    'model.onnx.encrypted': <InferenceSession_object>
}

# 部分加密：大文件只加密前10MB
if file_size > 10MB:
    encrypted_part = encrypt(data[:10MB])
    return encrypted_part + data[10MB:]
```

### 🏗️ 简化构建流程

- **一键构建**: `python -m deepenc build` - 自动发现和加密
- **智能过滤**: 自动排除测试、文档等非核心文件
- **入口点保护**: 确保入口文件不被加密
- **灵活配置**: 支持自定义过滤规则和构建选项
- **自动打包**: `--genzip` 参数自动生成带密码的zip包

### 🔐 企业级安全

- **多级授权**: 硬件授权 → 许可证文件
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

# 构建完成后生成zip包
python -m deepenc build --genzip

# 结合其他参数使用
python -m deepenc build --project /path/to/project --genzip --verbose
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

### ZIP 包生成

```bash
# 基本用法
python -m deepenc build --genzip

# 环境变量配置密码
export UNZIP_CODE="your_custom_password"
python -m deepenc build --genzip

# 生成的文件格式
# {projectname}.{version}.zip
# 例如: myproject.1.2.3.zip
# 默认密码: deepenc (可通过UNZIP_CODE环境变量修改)
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
- [ZIP 包生成](docs/zip_generation.md) - 自动打包功能详解

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
- **自动化分发**: 构建完成后自动生成带密码的zip包

## 📋 实际使用示例

### 完整工作流程

```bash
# 1. 设置环境
export AUTH_MODE="DEV"
export UNZIP_CODE="my_custom_password"

# 2. 创建项目VERSION文件
echo "1.0.0" > VERSION

# 3. 构建加密项目
python -m deepenc build --genzip --verbose

# 4. 查看构建结果
ls -la build/
ls -la build/dist/

# 5. 运行加密项目
cd build
python src/grpc_main.py
```

### 配置文件示例

项目根目录下的 `VERSION` 文件：
```
1.0.0
```

生成的配置文件 `build/config/encryption_config.json`：
```json
{
  "version": "1.0.0",
  "build_time": "2025-01-XX",
  "project_root": "/path/to/project",
  "entry_point": {
    "module_name": "src.grpc_main",
    "file_path": "/path/to/project/src/grpc_main.py"
  },
  "auth_info": {
    "auth_mode": "DEV",
    "hardware_auth_available": false,
    "key_source": "license_file",
    "authorization_valid": true
  },
  "module_mapping": {
    "src.utils": "encrypted/python/src/utils.py.encrypted"
  }
}
```

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
ENV AUTH_MODE=PROD

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
        - name: AUTH_MODE
          value: "PROD"
        - name: LICENSE_PATH
          value: "/data/appdatas/inference/license.dat"
```

## 🔧 开发环境

### 安装开发依赖

```bash
# 克隆仓库
git clone https://github.com/liwenju0/deepenc.git
cd deepenc

# 安装开发依赖
pip install -e ".[dev]"

# 设置开发环境
make dev-setup

# 运行测试
python -m pytest tests/
```

## 🔐 授权配置

### 开发模式

```bash
# 设置开发模式（无需硬件授权）
export AUTH_MODE="DEV"

# 创建许可证文件
mkdir -p /data/appdatas/inference
echo "your-16-char-key" > /data/appdatas/inference/license.dat
```

### 生产模式

```bash
# 设置生产模式（需要硬件授权）
export AUTH_MODE="PROD"

# 确保硬件授权设备已连接
# 系统会自动检测并验证硬件授权
```

### ZIP包密码配置

```bash
# 设置自定义密码
export UNZIP_CODE="your_custom_password"

# 使用默认密码（deepenc）
# 不设置环境变量即可
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

## 🔧 故障排除

### 常见问题

#### 1. 构建失败
```bash
# 检查项目结构
python -m deepenc scan

# 检查权限
ls -la /data/appdatas/inference/

# 检查授权文件
cat /data/appdatas/inference/license.dat
```

#### 2. ZIP包生成失败
```bash
# 检查VERSION文件
cat VERSION

# 检查环境变量
echo $UNZIP_CODE

# 使用详细模式
python -m deepenc build --genzip --verbose
```

#### 3. 运行时授权失败
```bash
# 检查授权模式
echo $AUTH_MODE

# 检查许可证文件
ls -la /data/appdatas/inference/license.dat

# 重新生成许可证
echo "your-16-char-key" > /data/appdatas/inference/license.dat
```

### 调试技巧

```bash
# 启用详细日志
export ENCRYPT_LOG_LEVEL="DEBUG"

# 检查系统状态
python -m deepenc status

# 验证构建结果
python -m deepenc verify
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

- **GitHub**: [https://github.com/liwenju0/deepenc](https://github.com/liwenju0/deepenc)
- **文档**: [https://deepenc.readthedocs.io/](https://deepenc.readthedocs.io/)
- **问题反馈**: [GitHub Issues](https://github.com/liwenju0/deepenc/issues)
- **讨论交流**: [GitHub Discussions](https://github.com/liwenju0/deepenc/discussions)

---

**DeepEnc** - 让 Python 项目加密分发变得简单而强大 🚀
