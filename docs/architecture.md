# 架构设计文档

## 🏗️ 系统架构概览

DeepEnc 框架采用分层架构设计，遵循 Linux 内核的设计理念：

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

## 🎯 设计原则

### 1. 简洁性 (Simplicity)
- **单一职责**: 每个组件只做一件事，做好一件事
- **最小接口**: 提供最少的必要接口
- **清晰边界**: 模块间边界明确，职责清晰

### 2. 透明性 (Transparency)
- **开发者无感知**: 加密/解密过程对开发者透明
- **错误可见**: 错误信息清晰明确，便于调试
- **状态可查**: 系统状态和运行信息可查询

### 3. 自动化 (Automation)
- **零配置**: 开箱即用，无需复杂配置
- **智能发现**: 自动发现项目结构和文件
- **自动降级**: 授权失败时自动降级到开发模式

### 4. 可靠性 (Reliability)
- **优雅降级**: 关键功能失败时提供替代方案
- **资源管理**: 自动管理内存、缓存等资源
- **错误恢复**: 从错误状态中自动恢复

## 🔧 核心组件

### 1. 系统启动器 (Bootstrap System)

系统启动器是框架的核心入口，提供多种启动方式：

```python
# 自动初始化 - 推荐用于开发环境
system = deepenc.auto_initialize()

# 快速启动 - 智能降级启动
system = deepenc.quick_start()

# 手动配置 - 精确控制启动过程
system = deepenc.initialize(module_config)
```

**设计特点:**
- **智能降级**: 自动选择最适合的启动方式
- **配置发现**: 自动查找和加载配置文件
- **状态管理**: 完整的系统生命周期管理

### 2. 加密引擎 (Encryption Engine)

基于 AES-CFB 模式的加密引擎，支持部分加密：

```python
class AESCrypto:
    def __init__(self):
        self.algorithm = "AES-CFB"
        self.key_length = 256
    
    def encrypt_file(self, input_path: str, output_path: str, key: bytes):
        """加密文件，支持部分加密"""
        pass
```

**核心特性:**
- **部分加密**: 只加密文件的关键部分，保持性能
- **流式处理**: 支持大文件的高效加密
- **密钥管理**: 安全的密钥生成和存储

### 3. 智能加载器 (Smart Loaders)

#### Python 模块加载器

```python
class SmartModuleLoader(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    """智能模块加载器
    
    自动处理加密和非加密的 Python 模块导入。
    实现了完全透明的加密模块加载机制。
    """
    
    def exec_module(self, module):
        """执行模块，自动设置 __file__ 等属性"""
        # 检查缓存
        if module.__name__ in self._cache:
            decrypted_content = self._cache[module.__name__]
        else:
            # 解密模块
            decrypted_content = self._decrypt_module(encrypted_file)
            # 缓存解密后的内容
            self._cache[module.__name__] = decrypted_content
        
        # 设置模块属性
        self._setup_module_attributes(module, module.__name__)
        # 执行解密后的代码
        exec(decrypted_content, module.__dict__)
```

**关键特性:**
- **属性完整性**: 自动设置 `__file__`、`__package__` 等属性
- **透明加载**: 开发者无需了解加密细节
- **智能降级**: 自动降级到普通导入

#### ONNX 模型加载器

```python
class SmartONNXLoader:
    """智能 ONNX 模型加载器
    
    自动处理加密和非加密的 ONNX 模型。
    与 onnxruntime 完全兼容。
    """
    
    def load_model(self, model_path: str):
        """加载模型，自动处理加密/解密"""
        pass
```

### 4. 文件发现系统 (Discovery System)

```python
class FileScanner:
    """文件扫描器
    
    智能发现项目中的 Python 和 ONNX 文件。
    支持自定义过滤规则。
    """
    
    def discover_python_files(self):
        """发现 Python 文件"""
        pass
    
    def discover_onnx_files(self):
        """发现 ONNX 模型文件"""
        pass
```

**发现策略:**
- **递归扫描**: 自动扫描项目目录结构
- **智能过滤**: 排除测试、文档等非核心文件
- **类型识别**: 自动识别文件类型和用途

## 🔄 数据流

### 1. 项目构建流程

```
项目源码 → 文件扫描 → 智能过滤 → 加密处理 → 构建输出
    ↓           ↓         ↓         ↓         ↓
  Python    发现文件   排除测试    AES加密   加密文件
  模块       ONNX模型   文档      部分加密   配置文件
```

### 2. 运行时加载流程

```
导入请求 → 模块查找 → 加密检测 → 解密加载 → 属性设置 → 模块可用
    ↓         ↓         ↓         ↓         ↓         ↓
  import   路径解析   模块名    文件检查   内存解密   设置属性   正常使用
  语句      模块名    加密状态   代码执行   __file__   导入成功
```

## 🛡️ 安全架构

### 1. 多层安全防护

- **文件级加密**: 源码和模型文件加密存储
- **运行时保护**: 内存中的代码解密后立即使用
- **密钥管理**: 硬件授权 + 软件许可证双重保护
- **访问控制**: 基于授权的模块访问控制

### 2. 授权机制

```python
class AuthManager:
    """授权管理器
    
    支持多种授权方式，确保系统安全。
    """
    
    def get_key(self) -> bytes:
        """获取加密密钥"""
        # 1. 尝试硬件授权
        if self._try_hardware_auth():
            return self._get_hardware_key()
        
        # 2. 尝试许可证文件
        if self._try_license_file():
            return self._get_license_key()
        
        # 3. 降级到开发模式
        return self._get_dev_key()
```

## 📊 性能优化

### 1. 部分加密策略

- **智能选择**: 只加密关键代码段
- **缓存优化**: 解密结果智能缓存
- **并行处理**: 多文件并行加密/解密

### 2. 内存管理

- **延迟加载**: 模块按需加载
- **缓存清理**: 自动清理过期缓存
- **资源回收**: 及时释放解密后的资源

## 🔍 监控和调试

### 1. 系统状态监控

```python
def get_system_status():
    """获取系统状态信息"""
    return {
        'initialized': deepenc.is_initialized(),
        'loaded_modules': len(module_cache),
        'memory_usage': get_memory_usage(),
        'cache_stats': get_cache_statistics()
    }
```

### 2. 调试支持

- **详细日志**: 完整的操作日志记录
- **错误追踪**: 详细的错误信息和堆栈
- **性能分析**: 关键操作的性能指标

---

**DeepEnc 架构团队** - 构建安全、高效、易用的加密框架 🏗️
