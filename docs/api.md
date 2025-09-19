# API 文档

## 🔌 主要接口

### 框架入口

#### `deepenc.initialize(module_config=None)`

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
import deepenc

# 手动配置
module_config = {
    'src.main': 'encrypted/python/src/main.py.encrypted'
}
system = deepenc.initialize(module_config)
```

#### `deepenc.auto_initialize()`

自动初始化系统，尝试从构建目录自动加载配置。

**返回:**
- `EncryptionSystem`: 加密系统实例

**说明:**
- 自动查找配置文件：`config/encryption_config.json`、`build/config/encryption_config.json`
- 如果找到配置，使用配置初始化；否则使用默认配置

#### `deepenc.quick_start()`

快速启动系统，如果自动初始化失败则使用默认配置。

**返回:**
- `EncryptionSystem`: 加密系统实例

**说明:**
- 尝试自动初始化
- 如果失败，使用默认配置初始化
- 适合开发和测试环境

#### `deepenc.get_system()`

获取当前的加密系统实例。

**返回:**
- `EncryptionSystem` 或 `None`: 系统实例

#### `deepenc.shutdown()`

关闭加密系统，清理所有资源。

#### `deepenc.is_initialized()`

检查系统是否已初始化。

**返回:**
- `bool`: 是否已初始化

## 🏗️ 构建 API

### ProjectBuilder

#### `ProjectBuilder(project_root=None, build_dir=None)`

项目构建器，用于自动构建加密项目。

**参数:**
- `project_root` (str, 可选): 项目根目录，默认当前目录
- `build_dir` (str, 可选): 构建输出目录，默认 `project_root/build`

#### `build_project(clean=True)`

构建加密项目。

**参数:**
- `clean` (bool): 是否清理构建目录，默认 True

**返回:**
- `dict`: 构建报告

**示例:**
```python
from deepenc.builders import ProjectBuilder

builder = ProjectBuilder('/path/to/project')
report = builder.build_project()

print(f"构建状态: {report['build_info']['success']}")
print(f"加密模块数: {report['encryption']['encrypted_python_modules']}")
```

#### `scan_project()`

扫描项目文件，不执行构建。

**返回:**
- `dict`: 扫描报告

#### `clean_build()`

清理构建目录。

## 🔍 发现 API

### FileScanner

#### `FileScanner(project_root=None, filter_rules=None)`

文件扫描器，用于发现项目中的 Python 和 ONNX 文件。

**参数:**
- `project_root` (str, 可选): 项目根目录
- `filter_rules` (dict, 可选): 自定义过滤规则

#### `discover_python_files()`

发现项目中的 Python 文件。

**返回:**
- `List[Path]`: Python 文件路径列表

#### `discover_onnx_files()`

发现项目中的 ONNX 模型文件。

**返回:**
- `List[Path]`: ONNX 文件路径列表

#### `discover_all_files()`

发现所有相关文件。

**返回:**
- `dict`: 包含 Python 和 ONNX 文件的字典

### FileFilter

#### `FileFilter(rules=None)`

文件过滤器，用于控制哪些文件被包含或排除。

**参数:**
- `rules` (dict, 可选): 过滤规则
  ```python
  {
      'exclude_dirs': ['tests', 'docs'],
      'exclude_files': ['*.pyc', '__pycache__'],
      'include_files': ['important.py']
  }
  ```

## 🔐 核心 API

### EncryptionSystem

#### `EncryptionSystem()`

加密系统主类，统一管理加密模块和模型。

#### `initialize(module_config=None)`

初始化加密系统。

**参数:**
- `module_config` (dict, 可选): 模块配置

**返回:**
- `bool`: 初始化是否成功

#### `get_status()`

获取系统状态信息。

**返回:**
- `dict`: 状态信息字典

#### `clear_caches()`

清理所有缓存。

#### `shutdown()`

关闭系统，清理资源。

### AESCrypto

#### `AESCrypto()`

AES 加密引擎。

#### `encrypt_file(input_path, output_path, key=None)`

加密文件。

**参数:**
- `input_path` (str): 输入文件路径
- `output_path` (str): 输出文件路径
- `key` (bytes, 可选): 加密密钥

#### `decrypt_file(input_path, key=None)`

解密文件到内存。

**参数:**
- `input_path` (str): 输入文件路径
- `key` (bytes, 可选): 解密密钥

**返回:**
- `bytes`: 解密后的数据

### AuthManager

#### `AuthManager()`

授权管理器。

#### `get_key()`

获取加密密钥。

**返回:**
- `bytes`: 加密密钥

#### `verify_license(license_path)`

验证许可证文件。

**参数:**
- `license_path` (str): 许可证文件路径

**返回:**
- `bool`: 验证是否成功

## 📊 错误处理

### 异常类

#### `EncryptionError`

加密相关错误的基类。

#### `AuthenticationError`

认证和授权错误。

#### `DecryptionError`

解密错误。

#### `LoaderError`

加载器错误。

#### `BuildError`

构建错误。

## 🔧 工具函数

### 文件系统工具

#### `ensure_dir(path)`

确保目录存在，如果不存在则创建。

**参数:**
- `path` (str): 目录路径

#### `safe_copy(src, dst)`

安全复制文件。

**参数:**
- `src` (str): 源文件路径
- `dst` (str): 目标文件路径

### 日志工具

#### `setup_logging(level='INFO')`

设置日志配置。

**参数:**
- `level` (str): 日志级别

## 📝 使用示例

### 基本用法

```python
import deepenc

# 自动初始化
system = deepenc.auto_initialize()

# 正常导入和使用
from src import main
main.run()
```

### 高级用法

```python
import deepenc
from deepenc.builders import ProjectBuilder

# 构建项目
builder = ProjectBuilder('/path/to/project')
report = builder.build_project()

# 手动初始化
module_config = {
    'src.main': 'build/encrypted/python/src/main.py.encrypted'
}
system = deepenc.initialize(module_config)

# 使用加密模块
from src import main
```

### 错误处理

```python
import deepenc
from deepenc.core import EncryptionError

try:
    system = deepenc.auto_initialize()
except EncryptionError as e:
    print(f"加密系统启动失败: {e}")
    # 降级处理
    pass
```
