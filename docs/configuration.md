# 配置参考文档

## 📋 配置概览

DeepEnc 框架支持多种配置方式，按优先级排序：

1. **许可证文件** - 最高优先级，适合开发和生产环境
2. **硬件授权** - 中等优先级，适合生产环境
3. **环境变量** - 中等优先级，适合容器化部署
4. **代码配置** - 最低优先级，适合自定义场景
5. **默认配置** - 兜底配置，确保系统正常运行

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
        "fallback_to_dev": false
    },
    "performance": {
        "cache_size_mb": 200,
        "max_workers": 8,
        "temp_dir": "/var/tmp"
    },
    "security": {
        "audit_log": "/var/log/deepenc/audit.log",
        "key_rotation_hours": 12,
        "secure_mode": true
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
  fallback_to_dev: false

performance:
  cache_size_mb: 200
  max_workers: 8
  temp_dir: "/var/tmp"

security:
  audit_log: "/var/log/deepenc/audit.log"
  key_rotation_hours: 12
  secure_mode: true
```

### 配置文件位置

框架按以下顺序查找配置文件：

1. **环境变量指定**: `DEEPENC_CONFIG_DIR/config.json`
2. **构建目录**: `build/config/encryption_config.json`
3. **项目根目录**: `config/encryption_config.json`
4. **默认位置**: `./config/encryption_config.json`

## 🔐 加密配置

### 加密算法配置

```json
{
    "encryption": {
        "algorithm": "AES-CFB",
        "key_length": 256,
        "iv_mode": "random",
        "padding": "PKCS7"
    }
}
```

**支持的算法:**
- **AES-CFB**: 推荐，性能好，安全性高
- **AES-CBC**: 兼容性好，性能中等
- **AES-GCM**: 最高安全性，性能较低

**密钥长度:**
- **128位**: 兼容性好，安全性中等
- **256位**: 推荐，安全性高，性能好

### 部分加密配置

```json
{
    "encryption": {
        "partial_encryption": true,
        "max_encrypt_size": 10485760,
        "encrypt_ratio": 0.3,
        "smart_selection": true
    }
}
```

**配置说明:**
- **partial_encryption**: 是否启用部分加密
- **max_encrypt_size**: 最大加密文件大小 (字节)
- **encrypt_ratio**: 加密比例 (0.1-1.0)
- **smart_selection**: 是否启用智能选择加密段

## 🚀 性能配置

### 缓存配置

```json
{
    "performance": {
        "cache": {
            "enabled": true,
            "max_size_mb": 200,
            "ttl_seconds": 3600,
            "cleanup_interval": 300
        }
    }
}
```

**缓存策略:**
- **LRU**: 最近最少使用淘汰策略
- **TTL**: 基于时间的过期策略
- **智能清理**: 自动清理过期和低频访问的缓存

### 并发配置

```json
{
    "performance": {
        "concurrency": {
            "max_workers": 8,
            "thread_pool_size": 16,
            "queue_size": 100
        }
    }
}
```

**并发控制:**
- **max_workers**: 最大工作线程数
- **thread_pool_size**: 线程池大小
- **queue_size**: 任务队列大小

## 🛡️ 安全配置

### 授权配置

```json
{
    "auth": {
        "mode": "PROD",
        "key_source": "hardware",
        "fallback_to_dev": false,
        "hardware_auth": {
            "enabled": true,
            "timeout_seconds": 30,
            "retry_count": 3
        }
    }
}
```

**授权模式:**
- **DEV**: 开发模式，使用许可证文件
- **PROD**: 生产模式，使用硬件授权
- **HYBRID**: 混合模式，优先硬件授权，降级到许可证文件

### 审计配置

```json
{
    "security": {
        "audit": {
            "enabled": true,
            "log_path": "/var/log/deepenc/audit.log",
            "log_level": "INFO",
            "max_file_size": 10485760,
            "backup_count": 5
        }
    }
}
```

**审计功能:**
- **操作记录**: 记录所有加密/解密操作
- **访问日志**: 记录模块访问和加载
- **错误追踪**: 记录所有错误和异常

## 🔧 构建配置

### 项目构建配置

```json
{
    "build": {
        "project_root": "/path/to/project",
        "build_dir": "/path/to/build",
        "entry_point": "src/main.py",
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
    }
}
```

**构建选项:**
- **project_root**: 项目根目录
- **build_dir**: 构建输出目录
- **entry_point**: 项目入口文件
- **exclude_patterns**: 排除的文件模式
- **include_patterns**: 包含的文件模式

### 文件过滤配置

```json
{
    "build": {
        "file_filter": {
            "exclude_dirs": [
                "tests",
                "docs",
                "examples",
                "__pycache__"
            ],
            "exclude_files": [
                "*.pyc",
                "*.pyo",
                "*.log",
                "config.py"
            ],
            "include_files": [
                "src/main.py",
                "src/core.py"
            ]
        }
    }
}
```

## 📊 监控配置

### 系统监控配置

```json
{
    "monitoring": {
        "enabled": true,
        "metrics": {
            "cpu_usage": true,
            "memory_usage": true,
            "disk_usage": true,
            "network_io": false
        },
        "health_check": {
            "enabled": true,
            "interval_seconds": 30,
            "timeout_seconds": 10
        }
    }
}
```

**监控指标:**
- **系统指标**: CPU、内存、磁盘使用率
- **应用指标**: 模块加载数、缓存命中率
- **性能指标**: 响应时间、吞吐量

### 日志配置

```json
{
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "handlers": {
            "console": {
                "enabled": true,
                "level": "INFO"
            },
            "file": {
                "enabled": true,
                "level": "DEBUG",
                "path": "/var/log/deepenc/deepenc.log",
                "max_size_mb": 100,
                "backup_count": 5
            }
        }
    }
}
```

## 🔄 动态配置

### 配置热更新

```python
import deepenc
import json

# 加载配置
with open('config.json', 'r') as f:
    config = json.load(f)

# 初始化系统
system = deepenc.initialize(config)

# 动态更新配置
def update_config(new_config):
    """动态更新配置"""
    system.update_config(new_config)
    print("配置已更新")

# 示例：更新缓存大小
new_cache_config = {
    "performance": {
        "cache": {
            "max_size_mb": 300
        }
    }
}
update_config(new_cache_config)
```

### 配置验证

```python
from deepenc.config import ConfigValidator

def validate_config(config):
    """验证配置有效性"""
    validator = ConfigValidator()
    
    try:
        validator.validate(config)
        print("✅ 配置验证通过")
        return True
    except Exception as e:
        print(f"❌ 配置验证失败: {e}")
        return False

# 验证配置
if validate_config(config):
    system = deepenc.initialize(config)
else:
    print("使用默认配置")
    system = deepenc.auto_initialize()
```

## 📱 容器化配置

### Docker 环境配置

```dockerfile
# 设置环境变量
ENV AUTH_MODE=PROD
ENV DEEPENC_DEBUG=0
ENV DEEPENC_CACHE_SIZE=200
ENV DEEPENC_MAX_WORKERS=8

# 创建配置目录
RUN mkdir -p /etc/deepenc

# 复制配置文件
COPY config/ /etc/deepenc/
ENV DEEPENC_CONFIG_DIR=/etc/deepenc
```

### Kubernetes 配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: deepenc-config
data:
  encryption_config.json: |
    {
      "version": "1.0.0",
      "encryption": {
        "algorithm": "AES-CFB",
        "key_length": 256
      }
    }
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deepenc-app
spec:
  template:
    spec:
      containers:
      - name: deepenc-app
        env:
        - name: DEEPENC_CONFIG_DIR
          value: "/etc/deepenc"
        volumeMounts:
        - name: config-volume
          mountPath: /etc/deepenc
      volumes:
      - name: config-volume
        configMap:
          name: deepenc-config
```

## 🚨 故障排除配置

### 调试配置

```json
{
    "debug": {
        "enabled": true,
        "log_level": "DEBUG",
        "trace_calls": true,
        "profile_performance": true,
        "memory_tracking": true
    }
}
```

**调试功能:**
- **详细日志**: 记录所有操作细节
- **调用追踪**: 追踪函数调用链
- **性能分析**: 分析关键操作性能
- **内存跟踪**: 监控内存使用情况

### 错误处理配置

```json
{
    "error_handling": {
        "retry_on_failure": true,
        "max_retry_count": 3,
        "retry_delay_seconds": 1,
        "fallback_strategy": "graceful",
        "error_reporting": {
            "enabled": true,
            "include_stack_trace": true,
            "log_to_file": true
        }
    }
}
```

## 📚 配置最佳实践

### 1. 环境分离

```bash
# 开发环境
export AUTH_MODE="DEV"
export DEEPENC_DEBUG="1"
export DEEPENC_CACHE_SIZE="50"

# 测试环境
export AUTH_MODE="DEV"
export DEEPENC_DEBUG="0"
export DEEPENC_CACHE_SIZE="100"

# 生产环境
export AUTH_MODE="PROD"
export DEEPENC_DEBUG="0"
export DEEPENC_CACHE_SIZE="200"
export DEEPENC_SECURE_MODE="1"
```

### 2. 配置管理

```bash
# 使用配置文件管理
mkdir -p config/{dev,test,prod}

# 开发环境配置
cp config/dev/encryption_config.json config/

# 测试环境配置
cp config/test/encryption_config.json config/

# 生产环境配置
cp config/prod/encryption_config.json config/
```

### 3. 配置验证

```python
# 启动前验证配置
import deepenc
from deepenc.config import validate_config

def safe_startup():
    """安全的系统启动"""
    try:
        # 验证配置
        if validate_config(config):
            system = deepenc.initialize(config)
        else:
            system = deepenc.auto_initialize()
        
        print("系统启动成功")
        return system
        
    except Exception as e:
        print(f"系统启动失败: {e}")
        return None
```

---

**DeepEnc 配置团队** - 提供灵活、安全的配置管理 ⚙️
