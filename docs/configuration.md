# 配置参考文档

## 📋 配置概览

DeepEnc 框架支持多种配置方式，按优先级排序：

1. **许可证文件** - 最高优先级，适合开发和生产环境
2. **硬件授权** - 中等优先级，适合生产环境
3. **代码配置** - 最低优先级，适合自定义场景
4. **默认配置** - 兜底配置，确保系统正常运行

## 🔧 环境变量配置

### 核心配置

| 变量名 | 描述 | 默认值 | 示例 |
|--------|------|--------|------|
| `AUTH_MODE` | 授权模式 | `DEV` | `AUTH_MODE="PROD"` |
| `DEEPENC_DEBUG` | 调试模式 | `False` | `DEEPENC_DEBUG="1"` |

### 路径配置

| 变量名 | 描述 | 默认值 | 示例 |
|--------|------|--------|------|
| `DEEPENC_CONFIG_DIR` | 配置目录 | `./config` | `DEEPENC_CONFIG_DIR="/etc/deepenc"` |
| `DEEPENC_BUILD_DIR` | 构建目录 | `./build` | `DEEPENC_BUILD_DIR="/opt/build"` |
| `DEEPENC_LICENSE_PATH` | 许可证文件路径 | 无 | `DEEPENC_LICENSE_PATH="/data/appdatas/inference/license.dat"` |

### 性能配置

| 变量名 | 描述 | 默认值 | 示例 |
|--------|------|--------|------|
| `DEEPENC_CACHE_SIZE` | 缓存大小 (MB) | `100` | `DEEPENC_CACHE_SIZE="200"` |
| `DEEPENC_TEMP_DIR` | 临时目录 | `/tmp` | `DEEPENC_TEMP_DIR="/var/tmp"` |
| `DEEPENC_MAX_WORKERS` | 最大工作线程数 | `4` | `DEEPENC_MAX_WORKERS="8"` |

### 安全配置

| 变量名 | 描述 | 默认值 | 示例 |
|--------|------|--------|------|
| `DEEPENC_KEY_ROTATION` | 密钥轮换间隔 (小时) | `24` | `DEEPENC_KEY_ROTATION="12"` |
| `DEEPENC_AUDIT_LOG` | 审计日志路径 | 无 | `DEEPENC_AUDIT_LOG="/var/log/deepenc/audit.log"` |
| `DEEPENC_SECURE_MODE` | 安全模式 | `False` | `DEEPENC_SECURE_MODE="1"` |

## 📄 许可证文件配置

### 许可证文件位置

框架按以下顺序查找许可证文件：

1. **设备特定许可证**: `/data/appdatas/inference/{device_id}.license`
2. **默认许可证**: `/data/appdatas/inference/license.dat`
3. **自定义路径**: 通过环境变量 `DEEPENC_LICENSE_PATH` 指定

### 许可证文件格式

#### 开发模式 (AUTH_MODE=DEV)

```bash
# 许可证文件内容直接为加密密钥
echo "1234567890123456" > /data/appdatas/inference/license.dat
export AUTH_MODE="DEV"
```

#### 生产模式 (AUTH_MODE=PROD)

```bash
# 许可证文件内容为加密数据，需要通过硬件授权解密
echo "encrypted-license-content" > /data/appdatas/inference/license.dat
export AUTH_MODE="PROD"
```

### 许可证文件权限

```bash
# 设置安全的文件权限
chmod 600 /data/appdatas/inference/license.dat
chown root:root /data/appdatas/inference/license.dat
```

## 📄 配置文件配置

### 配置文件格式

DeepEnc 支持多种配置文件格式：

#### JSON 格式 (推荐)

```json
{
    "version": "1.0.0",
    "encryption": {
        "algorithm": "AES-CFB",
        "key_length": 256,
        "partial_encryption": true,
        "max_encrypt_size": 10485760
    },
    "auth": {
        "mode": "PROD",
        "key_source": "hardware",
        "license_path": "/data/appdatas/inference/license.dat",
        "hardware_auth_timeout": 10
    },
    "discovery": {
        "auto_scan": true,
        "exclude_patterns": [
            "tests/**",
            "docs/**",
            "*.pyc",
            "__pycache__"
        ],
        "include_patterns": [
            "src/**/*.py",
            "model/**/*.onnx"
        ]
    },
    "build": {
        "project_root": ".",
        "build_dir": "./build",
        "entry_point": "src/main.py",
        "clean_before_build": true,
        "preserve_structure": true
    },
    "runtime": {
        "cache_size_mb": 100,
        "temp_dir": "/tmp",
        "max_workers": 4,
        "auto_cleanup": true,
        "cleanup_interval": 3600
    },
    "security": {
        "secure_mode": false,
        "audit_logging": true,
        "audit_log_path": "/var/log/deepenc/audit.log",
        "key_rotation_hours": 24
    },
    "logging": {
        "level": "INFO",
        "format": "structured",
        "file_path": "/var/log/deepenc/deepenc.log",
        "max_file_size_mb": 100,
        "backup_count": 5
    }
}
```

#### YAML 格式

```yaml
version: "1.0.0"

encryption:
  algorithm: "AES-CFB"
  key_length: 256
  partial_encryption: true
  max_encrypt_size: 10485760

auth:
  mode: "PROD"
  key_source: "hardware"
  license_path: "/data/appdatas/inference/license.dat"
  hardware_auth_timeout: 10

discovery:
  auto_scan: true
  exclude_patterns:
    - "tests/**"
    - "docs/**"
    - "*.pyc"
    - "__pycache__"
  include_patterns:
    - "src/**/*.py"
    - "model/**/*.onnx"

build:
  project_root: "."
  build_dir: "./build"
  entry_point: "src/main.py"
  clean_before_build: true
  preserve_structure: true

runtime:
  cache_size_mb: 100
  temp_dir: "/tmp"
  max_workers: 4
  auto_cleanup: true
  cleanup_interval: 3600

security:
  secure_mode: false
  audit_logging: true
  audit_log_path: "/var/log/deepenc/audit.log"
  key_rotation_hours: 24

logging:
  level: "INFO"
  format: "structured"
  file_path: "/var/log/deepenc/deepenc.log"
  max_file_size_mb: 100
  backup_count: 5
```

#### TOML 格式

```toml
version = "1.0.0"

[encryption]
algorithm = "AES-CFB"
key_length = 256
partial_encryption = true
max_encrypt_size = 10485760

[auth]
mode = "PROD"
key_source = "hardware"
license_path = "/data/appdatas/inference/license.dat"
hardware_auth_timeout = 10

[discovery]
auto_scan = true
exclude_patterns = [
    "tests/**",
    "docs/**",
    "*.pyc",
    "__pycache__"
]
include_patterns = [
    "src/**/*.py",
    "model/**/*.onnx"
]

[build]
project_root = "."
build_dir = "./build"
entry_point = "src/main.py"
clean_before_build = true
preserve_structure = true

[runtime]
cache_size_mb = 100
temp_dir = "/tmp"
max_workers = 4
auto_cleanup = true
cleanup_interval = 3600

[security]
secure_mode = false
audit_logging = true
audit_log_path = "/var/log/deepenc/audit.log"
key_rotation_hours = 24

[logging]
level = "INFO"
format = "structured"
file_path = "/var/log/deepenc/deepenc.log"
max_file_size_mb = 100
backup_count = 5
```

### 配置文件位置

框架按以下顺序查找配置文件：

1. **当前工作目录**: `./deepenc.toml`, `./deepenc.yaml`, `./deepenc.json`
2. **配置目录**: `./config/deepenc.toml`, `./config/deepenc.yaml`, `./config/deepenc.json`
3. **构建目录**: `./build/config/deepenc.toml`, `./build/config/deepenc.yaml`, `./build/config/deepenc.json`
4. **用户目录**: `~/.deepenc/deepenc.toml`, `~/.deepenc/deepenc.yaml`, `~/.deepenc/deepenc.json`
5. **系统目录**: `/etc/deepenc/deepenc.toml`, `/etc/deepenc/deepenc.yaml`, `/etc/deepenc/deepenc.json`

## 🐍 代码配置

### 基本配置

```python
import deepenc
from deepenc.config import DeepEncConfig

# 创建配置对象
config = DeepEncConfig()

# 设置配置
config.encryption.algorithm = "AES-CFB"
config.encryption.key_length = 256
config.auth.mode = "PROD"
config.discovery.auto_scan = True

# 应用配置
system = deepenc.initialize(config=config)
```

### 高级配置

```python
from deepenc.config import DeepEncConfig
from deepenc.discovery import FileFilter
from deepenc.builders import ProjectBuilder

# 创建自定义过滤器
file_filter = FileFilter({
    'exclude_dirs': ['tests', 'docs'],
    'exclude_files': ['*.pyc', '__pycache__'],
    'include_files': ['src/main.py']
})

# 创建配置
config = DeepEncConfig()
config.discovery.file_filter = file_filter
config.build.entry_point = "src/main.py"
config.runtime.cache_size_mb = 200

# 使用配置构建项目
builder = ProjectBuilder(config=config)
report = builder.build_project()
```

### 配置验证

```python
from deepenc.config import DeepEncConfig, ConfigValidator

# 创建配置
config = DeepEncConfig()
config.encryption.key_length = 128  # 无效值

# 验证配置
validator = ConfigValidator()
try:
    validator.validate(config)
    print("配置有效")
except ValueError as e:
    print(f"配置无效: {e}")
```

## 🔧 配置选项详解

### 加密配置 (encryption)

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `algorithm` | string | `"AES-CFB"` | 加密算法，支持 AES-CFB, AES-CBC |
| `key_length` | int | `256` | 密钥长度，支持 128, 192, 256 |
| `partial_encryption` | bool | `true` | 是否启用部分加密 |
| `max_encrypt_size` | int | `10485760` | 最大加密大小 (字节) |
| `iv_mode` | string | `"fixed"` | IV 模式，支持 fixed, random |
| `padding` | string | `"PKCS7"` | 填充模式 |

### 授权配置 (auth)

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `mode` | string | `"DEV"` | 授权模式，支持 DEV, TEST, PROD |
| `key_source` | string | `"license_file"` | 密钥来源，支持 license_file, hardware |
| `license_path` | string | `/data/appdatas/inference/license.dat` | 许可证文件路径 |
| `hardware_auth_timeout` | int | `10` | 硬件授权超时时间 (秒) |

### 发现配置 (discovery)

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `auto_scan` | bool | `true` | 是否自动扫描 |
| `exclude_patterns` | list | `[]` | 排除模式列表 |
| `include_patterns` | list | `[]` | 包含模式列表 |
| `scan_depth` | int | `10` | 扫描深度 |
| `follow_symlinks` | bool | `false` | 是否跟随符号链接 |
| `file_types` | list | `["py", "onnx"]` | 支持的文件类型 |

### 构建配置 (build)

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `project_root` | string | `"."` | 项目根目录 |
| `build_dir` | string | `"./build"` | 构建输出目录 |
| `entry_point` | string | `"src/grpc_main.py"` | 入口点文件 |
| `clean_before_build` | bool | `true` | 构建前是否清理 |
| `preserve_structure` | bool | `true` | 是否保持目录结构 |
| `compress_output` | bool | `false` | 是否压缩输出 |
| `generate_checksums` | bool | `true` | 是否生成校验和 |

### 运行时配置 (runtime)

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `cache_size_mb` | int | `100` | 缓存大小 (MB) |
| `temp_dir` | string | `"/tmp"` | 临时目录 |
| `max_workers` | int | `4` | 最大工作线程数 |
| `auto_cleanup` | bool | `true` | 是否自动清理 |
| `cleanup_interval` | int | `3600` | 清理间隔 (秒) |
| `memory_limit_mb` | int | `512` | 内存限制 (MB) |
| `enable_profiling` | bool | `false` | 是否启用性能分析 |

### 安全配置 (security)

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `secure_mode` | bool | `false` | 是否启用安全模式 |
| `audit_logging` | bool | `true` | 是否启用审计日志 |
| `audit_log_path` | string | 无 | 审计日志路径 |
| `key_rotation_hours` | int | `24` | 密钥轮换间隔 (小时) |
| `secure_temp_files` | bool | `true` | 是否使用安全临时文件 |
| `file_permissions` | string | `"600"` | 文件权限模式 |

### 日志配置 (logging)

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `level` | string | `"INFO"` | 日志级别 |
| `format` | string | `"structured"` | 日志格式，支持 simple, structured, json |
| `file_path` | string | 无 | 日志文件路径 |
| `max_file_size_mb` | int | `100` | 最大文件大小 (MB) |
| `backup_count` | int | `5` | 备份文件数量 |
| `console_output` | bool | `true` | 是否输出到控制台 |
| `syslog` | bool | `false` | 是否输出到系统日志 |

## 🔄 配置热更新

### 启用热更新

```python
from deepenc.config import ConfigManager

# 创建配置管理器
config_manager = ConfigManager()

# 启用热更新
config_manager.enable_hot_reload()

# 监听配置文件变化
@config_manager.on_config_change
def handle_config_change(new_config):
    print(f"配置已更新: {new_config.version}")
    
    # 应用新配置
    if deepenc.is_initialized():
        system = deepenc.get_system()
        system.update_config(new_config)
```

### 配置变更通知

```python
import asyncio
from deepenc.config import ConfigWatcher

async def watch_config():
    """监听配置变化"""
    watcher = ConfigWatcher()
    
    async for config_change in watcher.watch():
        print(f"检测到配置变化: {config_change.file_path}")
        
        # 重新加载配置
        new_config = config_change.load_config()
        
        # 应用新配置
        await apply_config(new_config)

# 启动配置监听
asyncio.run(watch_config())
```

## 🧪 配置测试

### 配置验证测试

```python
import pytest
from deepenc.config import DeepEncConfig, ConfigValidator

class TestConfig:
    
    def test_valid_config(self):
        """测试有效配置"""
        config = DeepEncConfig()
        config.encryption.algorithm = "AES-CFB"
        config.encryption.key_length = 256
        
        validator = ConfigValidator()
        assert validator.validate(config) is True
    
    def test_invalid_key_length(self):
        """测试无效密钥长度"""
        config = DeepEncConfig()
        config.encryption.key_length = 64  # 无效值
        
        validator = ConfigValidator()
        with pytest.raises(ValueError):
            validator.validate(config)
    
    def test_missing_required_fields(self):
        """测试缺少必需字段"""
        config = DeepEncConfig()
        # 不设置必需字段
        
        validator = ConfigValidator()
        with pytest.raises(ValueError):
            validator.validate(config)
```

### 配置加载测试

```python
import tempfile
import json
from pathlib import Path
from deepenc.config import ConfigLoader

class TestConfigLoading:
    
    def test_load_json_config(self):
        """测试加载 JSON 配置"""
        # 创建临时配置文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            config_data = {
                "version": "1.0.0",
                "encryption": {
                    "algorithm": "AES-CFB",
                    "key_length": 256
                }
            }
            json.dump(config_data, f)
            config_path = f.name
        
        try:
            # 加载配置
            loader = ConfigLoader()
            config = loader.load_from_file(config_path)
            
            assert config.version == "1.0.0"
            assert config.encryption.algorithm == "AES-CFB"
            assert config.encryption.key_length == 256
            
        finally:
            # 清理临时文件
            Path(config_path).unlink()
    
    def test_load_yaml_config(self):
        """测试加载 YAML 配置"""
        # 类似 JSON 测试，但使用 YAML 格式
        pass
    
    def test_load_toml_config(self):
        """测试加载 TOML 配置"""
        # 类似 JSON 测试，但使用 TOML 格式
        pass
```

## 🔍 配置调试

### 启用配置调试

```bash
# 设置环境变量
export DEEPENC_DEBUG="1"
export DEEPENC_CONFIG_DEBUG="1"

# 或者在代码中
import os
os.environ['DEEPENC_DEBUG'] = '1'
os.environ['DEEPENC_CONFIG_DEBUG'] = '1'
```

### 配置诊断

```python
from deepenc.config import ConfigDiagnostics

# 运行配置诊断
diagnostics = ConfigDiagnostics()
report = diagnostics.run()

print("配置诊断报告:")
print(f"配置文件数量: {report['config_files_found']}")
print(f"配置加载状态: {report['load_status']}")
print(f"配置验证结果: {report['validation_result']}")
print(f"许可证文件状态: {report['license_status']}")

if report['issues']:
    print("\n发现的问题:")
    for issue in report['issues']:
        print(f"- {issue['type']}: {issue['message']}")
```

### 配置比较

```python
from deepenc.config import ConfigComparator

# 比较两个配置
config1 = DeepEncConfig()
config1.encryption.algorithm = "AES-CFB"

config2 = DeepEncConfig()
config2.encryption.algorithm = "AES-CBC"

# 比较配置差异
comparator = ConfigComparator()
diff = comparator.compare(config1, config2)

print("配置差异:")
for change in diff.changes:
    print(f"- {change.path}: {change.old_value} -> {change.new_value}")
```

## 📚 配置最佳实践

### 1. 环境分离

```bash
# 开发环境
export AUTH_MODE="DEV"
export DEEPENC_CONFIG_DIR="./config/dev"

# 测试环境
export AUTH_MODE="TEST"
export DEEPENC_CONFIG_DIR="./config/test"

# 生产环境
export AUTH_MODE="PROD"
export DEEPENC_CONFIG_DIR="/etc/deepenc/prod"
```

### 2. 配置模板

```python
# 创建配置模板
def create_config_template(environment):
    """创建环境特定的配置模板"""
    base_config = {
        "version": "1.0.0",
        "encryption": {
            "algorithm": "AES-CFB",
            "key_length": 256
        }
    }
    
    if environment == "development":
        base_config.update({
            "auth": {"mode": "DEV"},
            "logging": {"level": "DEBUG"}
        })
    elif environment == "production":
        base_config.update({
            "auth": {"mode": "PROD"},
            "logging": {"level": "WARNING"},
            "security": {"secure_mode": True}
        })
    
    return base_config
```

### 3. 配置验证

```python
# 生产环境配置验证
def validate_production_config(config):
    """验证生产环境配置"""
    errors = []
    
    # 检查安全设置
    if not config.security.secure_mode:
        errors.append("生产环境必须启用安全模式")
    
    if config.auth.mode != "PROD":
        errors.append("生产环境必须使用 PROD 授权模式")
    
    # 检查日志设置
    if config.logging.level == "DEBUG":
        errors.append("生产环境不应使用 DEBUG 日志级别")
    
    if errors:
        raise ValueError(f"配置验证失败: {'; '.join(errors)}")
```

### 4. 配置备份

```python
import shutil
from datetime import datetime

def backup_config(config_path):
    """备份配置文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{config_path}.backup_{timestamp}"
    
    shutil.copy2(config_path, backup_path)
    print(f"配置已备份到: {backup_path}")
    
    return backup_path
```

## 🔮 未来配置特性

### 1. 计划中的功能

- **配置版本管理**: 支持配置的版本控制和回滚
- **配置模板系统**: 提供预定义的配置模板
- **配置加密**: 支持敏感配置的加密存储
- **配置同步**: 支持多节点配置同步

### 2. 扩展接口

```python
# 自定义配置提供者
class CustomConfigProvider:
    def load_config(self):
        """加载配置"""
        pass
    
    def save_config(self, config):
        """保存配置"""
        pass
    
    def watch_changes(self):
        """监听配置变化"""
        pass

# 注册自定义提供者
from deepenc.config import ConfigRegistry
registry = ConfigRegistry()
registry.register_provider('custom', CustomConfigProvider())
```
