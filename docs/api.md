# API 文档

## 🔌 主要接口

### 框架入口

#### `encrypt.bootstrap(module_config=None)`

启动加密系统的主要入口点。

**参数:**
- `module_config` (dict, 可选): 模块配置字典
  ```python
  {
      'module_name': 'encrypted_file_path',
      'src.main': 'encrypted/python/src/main.py.encrypted'
  }
  ```

**返回:**
- `EncryptionSystem`: 加密系统实例

**示例:**
```python
import encrypt

# 自动初始化
system = encrypt.bootstrap()

# 手动配置
module_config = {
    'src.main': 'encrypted/python/src/main.py.encrypted'
}
system = encrypt.bootstrap(module_config)
```

#### `encrypt.initialize(module_config=None)`

`bootstrap()` 的别名，提供更明确的语义。

#### `encrypt.get_system()`

获取当前的加密系统实例。

**返回:**
- `EncryptionSystem` 或 `None`: 系统实例

#### `encrypt.shutdown()`

关闭加密系统，清理所有资源。

## 🏗️ 构建 API

### ProjectBuilder

#### `ProjectBuilder(project_root=None, build_dir=None, entry_point=None)`

项目构建器，用于自动构建加密项目。

**参数:**
- `project_root` (str, 可选): 项目根目录，默认当前目录
- `build_dir` (str, 可选): 构建输出目录，默认 `project_root/build`
- `entry_point` (str, 可选): 项目入口点文件，默认 `src/grpc_main.py`

#### `build_project(auto_discover=True, clean=True)`

构建加密项目。

**参数:**
- `auto_discover` (bool): 是否自动发现文件，默认 True
- `clean` (bool): 是否清理构建目录，默认 True

**返回:**
- `dict`: 构建报告

**示例:**
```python
from encrypt.builders import ProjectBuilder

builder = ProjectBuilder('/path/to/project')
report = builder.build_project()

print(f"构建状态: {report['build_info']['success']}")
print(f"加密模块数: {report['encryption']['encrypted_python_modules']}")
```

## 🔍 发现 API

### FileScanner

#### `FileScanner(project_root=None, filter_rules=None)`

文件扫描器，用于发现项目中的 Python 和 ONNX 文件。

**参数:**
- `project_root` (str, 可选): 项目根目录
- `filter_rules` (dict, 可选): 自定义过滤规则

#### `discover_python_files()`

发现所有 Python 文件。

**返回:**
- `list`: Python 文件信息列表

#### `discover_onnx_files()`

发现所有 ONNX 文件。

**返回:**
- `list`: ONNX 文件信息列表

#### `discover_all_files()`

发现所有相关文件。

**返回:**
- `dict`: 包含所有文件信息的字典

**示例:**
```python
from encrypt.discovery import FileScanner

scanner = FileScanner('/path/to/project')
result = scanner.discover_all_files()

print(f"Python 文件: {len(result['python_files'])}")
print(f"ONNX 文件: {len(result['onnx_files'])}")
```

### FileFilter

#### `FileFilter(custom_rules=None)`

文件过滤器，用于过滤不需要处理的文件。

**参数:**
- `custom_rules` (dict, 可选): 自定义过滤规则
  ```python
  {
      'exclude_dirs': ['test_dir'],
      'exclude_files': ['config.py'],
      'include_files': ['important.py']
  }
  ```

#### `should_include_file(file_path, project_root=None)`

判断文件是否应该包含。

**参数:**
- `file_path` (str): 文件路径
- `project_root` (str, 可选): 项目根目录

**返回:**
- `bool`: 是否应该包含

## 🔐 加密 API

### AESCrypto

#### `AESCrypto(enc_len=None)`

AES 加密器。

**参数:**
- `enc_len` (int, 可选): 加密长度，默认 10MB

#### `encrypt(data, key)`

加密数据。

**参数:**
- `data` (bytes): 要加密的数据
- `key` (str): 加密密钥

**返回:**
- `bytes`: 加密后的数据

#### `decrypt(encrypted_data, key)`

解密数据。

**参数:**
- `encrypted_data` (bytes): 加密的数据
- `key` (str): 解密密钥

**返回:**
- `bytes`: 解密后的数据

#### `encrypt_file(input_path, output_path, key)`

加密文件。

#### `decrypt_file(encrypted_path, key)`

解密文件到内存。

**示例:**
```python
from encrypt.core import AESCrypto

crypto = AESCrypto()

# 加密数据
data = b"Hello, World!"
key = "1234567890123456"  # 16字符密钥
encrypted = crypto.encrypt(data, key)

# 解密数据
decrypted = crypto.decrypt(encrypted, key)
assert data == decrypted
```

### AuthManager

#### `AuthManager()`

授权管理器。

#### `get_key()`

获取当前的加密密钥。

**返回:**
- `str`: 加密密钥

#### `verify_authorization()`

验证授权状态。

**返回:**
- `bool`: 授权是否有效

#### `get_auth_info()`

获取授权信息。

**返回:**
- `dict`: 授权信息

**示例:**
```python
from encrypt.core import AuthManager

auth = AuthManager()
key = auth.get_key()
info = auth.get_auth_info()

print(f"密钥来源: {info['key_source']}")
print(f"授权状态: {info['authorization_valid']}")
```

## 🚀 加载器 API

### SmartModuleLoader

#### `register_encrypted_module(module_name, encrypted_file_path)`

注册加密模块。

**参数:**
- `module_name` (str): 模块名称
- `encrypted_file_path` (str): 加密文件路径

#### `get_cache_info()`

获取缓存信息。

**返回:**
- `dict`: 缓存统计信息

#### `clear_cache()`

清理缓存。

### SmartONNXLoader

#### `load_model(model_path, **kwargs)`

智能加载 ONNX 模型。

**参数:**
- `model_path` (str): 模型文件路径
- `**kwargs`: 传递给 `onnxruntime.InferenceSession` 的参数

**返回:**
- `onnxruntime.InferenceSession`: 推理会话

#### `cleanup_all()`

清理所有临时文件。

## 🎛️ 系统控制 API

### EncryptionSystem

#### `get_status()`

获取系统状态。

**返回:**
- `dict`: 系统状态信息

#### `clear_caches()`

清理所有缓存。

#### `shutdown()`

关闭系统。

**示例:**
```python
import encrypt

# 启动系统
system = encrypt.bootstrap()

# 获取状态
status = system.get_status()
print(f"系统已初始化: {status['initialized']}")

# 清理缓存
system.clear_caches()

# 关闭系统
system.shutdown()
```

## 🛠️ 工具函数

### 便利函数

#### `encrypt.quick_start()`

快速启动，自动检测配置。

#### `encrypt.auto_initialize()`

自动初始化，从构建目录加载配置。

#### `encrypt.is_initialized()`

检查系统是否已初始化。

**示例:**
```python
import encrypt

# 快速启动
system = encrypt.quick_start()

# 检查状态
if encrypt.is_initialized():
    print("系统已就绪")
```

## ❌ 异常处理

### 异常层次结构

```python
Exception
├── EncryptionError
│   └── DecryptionError
├── AuthenticationError
│   ├── LicenseError
│   └── KeyError
├── FileDiscoveryError
├── BuildError
└── LoaderError
```

### 异常处理最佳实践

```python
import encrypt
from encrypt.core import EncryptionError, AuthenticationError

try:
    system = encrypt.bootstrap()
except AuthenticationError as e:
    print(f"授权失败: {e}")
    # 处理授权问题
except EncryptionError as e:
    print(f"加密错误: {e}")
    # 处理加密问题
except Exception as e:
    print(f"未知错误: {e}")
    # 处理其他问题
```

## 🔧 配置 API

### 环境变量

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `AUTH_MODE` | 授权模式 | `DEV` |
| `ENCRYPTION_KEY` | 加密密钥 | 无 |
| `AUTH_CODE` | 授权码 | 无 |
| `ENCRYPT_DEBUG` | 调试模式 | `False` |

### 配置文件

框架支持 JSON 格式的配置文件：

```json
{
    "version": "1.0.0",
    "module_mapping": {
        "src.main": "encrypted/python/src/main.py.encrypted"
    },
    "model_mapping": {
        "eros": "encrypted/models/eros.onnx.encrypt"
    },
    "auth_info": {
        "auth_mode": "DEV",
        "key_source": "environment"
    }
}
```

## 📈 性能指标

### 关键指标

- **启动时间**: 系统初始化时间 < 100ms
- **解密时间**: 单个模块解密时间 < 50ms
- **内存占用**: 缓存内存占用 < 100MB
- **缓存命中率**: > 90%

### 性能监控

```python
# 获取性能统计
system = encrypt.get_system()
if system:
    perf_stats = system.get_performance_stats()
    print(f"解密操作数: {perf_stats.get('decrypt_count', 0)}")
    print(f"缓存命中率: {perf_stats.get('cache_hit_rate', 0):.2%}")
```
