# 最佳实践指南

## 🎯 开发最佳实践

### 1. 项目结构建议

```
your_project/
├── src/                    # 核心源码目录
│   ├── __init__.py
│   ├── main.py            # 主模块（推荐作为入口点）
│   ├── grpc_main.py       # gRPC服务（默认入口点）
│   ├── models/            # 模型相关代码
│   └── utils/             # 工具函数
├── model/                 # ONNX 模型目录
│   ├── eros/
│   ├── mars/
│   └── nsfw_det/
├── conf/                  # 配置文件目录
├── tests/                 # 测试代码（不会被加密）
├── docs/                  # 文档（不会被加密）
├── requirements.txt       # 依赖文件
└── setup.py              # 安装脚本
```

### 2. 代码组织建议

#### 保持模块独立性

```python
# ✅ 好的做法：模块功能独立
# src/detector.py
class Detector:
    def __init__(self):
        self.model_path = 'model/detector.onnx'
    
    def detect(self, image):
        # 独立的检测逻辑
        pass

# ✅ 好的做法：清晰的接口
# src/main.py
from .detector import Detector
from .classifier import Classifier

def main():
    detector = Detector()
    classifier = Classifier()
    # 主逻辑
```

#### 避免循环导入

```python
# ❌ 避免这样做
# a.py
from b import func_b

# b.py  
from a import func_a  # 循环导入

# ✅ 推荐做法
# common.py
def shared_function():
    pass

# a.py
from common import shared_function

# b.py
from common import shared_function
```

### 3. 加密策略建议

#### 选择性加密

```python
# 核心业务逻辑 - 建议加密
src/
├── detector.py          # ✅ 加密
├── classifier.py        # ✅ 加密
├── nsfw_censor.py      # ✅ 加密

# 通用工具 - 可以不加密  
utils/
├── file_utils.py       # ⚠️ 可选
├── image_utils.py      # ⚠️ 可选

# 配置和测试 - 不建议加密
tests/                  # ❌ 不加密
config/                 # ❌ 不加密
docs/                   # ❌ 不加密
```

#### 模型文件管理

```python
# ✅ 推荐的模型组织方式
model/
├── eros/
│   ├── eros.onnx           # 原始模型
│   ├── eros.onnx.encrypt   # 加密模型
│   └── config.pbtxt        # 配置文件
├── mars/
│   ├── mars.onnx
│   ├── mars.onnx.encrypt
│   └── config.pbtxt
```

## 🔐 安全最佳实践

### 1. 密钥管理

#### 生产环境

```bash
# ✅ 使用硬件授权
export AUTH_MODE="PROD"

# ✅ 或者使用安全的许可证文件
echo "secure-license-content" > /data/appdatas/inference/license.dat
chmod 600 /data/appdatas/inference/license.dat
```

#### 开发环境

```bash
# ✅ 使用环境变量
export ENCRYPTION_KEY="dev-key-16chars"
export AUTH_MODE="DEV"

# ✅ 或者使用本地许可证文件
echo "dev-license-content" > ./license.dat
```

#### 密钥轮换

```python
# 定期更新密钥
def rotate_encryption_key():
    # 1. 生成新密钥
    new_key = generate_new_key()
    
    # 2. 重新加密所有文件
    builder = ProjectBuilder()
    builder.rebuild_with_new_key(new_key)
    
    # 3. 更新配置
    update_key_config(new_key)
```

### 2. 文件权限

```bash
# 设置适当的文件权限
chmod 600 license.dat              # 许可证文件只有所有者可读写
chmod 644 *.py.encrypted          # 加密文件只读
chmod 755 build/run.py            # 启动脚本可执行
```

### 3. 安全清理

```python
# 构建后自动清理敏感文件
def secure_cleanup():
    # 删除原始源码文件
    for py_file in source_files:
        os.remove(py_file)
    
    # 删除原始模型文件
    for onnx_file in model_files:
        os.remove(onnx_file)
    
    # 清理构建缓存
    shutil.rmtree('__pycache__', ignore_errors=True)
```

## ⚡ 性能最佳实践

### 1. 缓存策略

```python
# ✅ 启用智能缓存
system = encrypt.bootstrap()

# 预加载关键模块
critical_modules = ['src.main', 'src.detector']
for module in critical_modules:
    __import__(module)  # 触发解密和缓存

# 定期清理缓存
import threading
def cache_cleanup():
    while True:
        time.sleep(3600)  # 每小时清理一次
        system.clear_caches()

threading.Thread(target=cache_cleanup, daemon=True).start()
```

### 2. 内存管理

```python
# ✅ 监控内存使用
import psutil

def monitor_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    
    print(f"内存使用: {memory_info.rss / 1024 / 1024:.2f} MB")
    
    # 如果内存使用过高，清理缓存
    if memory_info.rss > 500 * 1024 * 1024:  # 500MB
        encrypt.get_system().clear_caches()
```

### 3. 启动优化

```python
# ✅ 延迟初始化
class LazyInitializer:
    def __init__(self):
        self._system = None
    
    @property
    def system(self):
        if self._system is None:
            self._system = encrypt.bootstrap()
        return self._system

# 全局延迟初始化
lazy_encrypt = LazyInitializer()

def get_model():
    # 只有在实际使用时才初始化
    return lazy_encrypt.system.load_model('model.onnx')
```

### 4. 入口点文件管理

```python
# ✅ 推荐做法：清晰的入口点结构
# src/main.py - 主入口点
def main():
    """应用程序主入口点"""
    # 初始化加密系统
    import deepenc
    deepenc.bootstrap()
    
    # 导入业务模块
    from .grpc_main import start_server
    from .models import load_models
    
    # 启动服务
    start_server()

if __name__ == '__main__':
    main()

# ✅ 推荐做法：分离服务入口点
# src/grpc_main.py - gRPC服务入口点
def start_server():
    """启动gRPC服务"""
    # gRPC服务逻辑
    pass

# ✅ 推荐做法：CLI入口点
# src/cli.py - 命令行工具入口点
def cli_main():
    """命令行工具主入口点"""
    # CLI逻辑
    pass
```

#### 入口点文件最佳实践

1. **命名规范**: 使用描述性名称，如 `main.py`, `app.py`, `server.py`
2. **功能分离**: 不同功能使用不同的入口点文件
3. **依赖管理**: 确保入口点文件不依赖其他未加密的模块
4. **权限设置**: 构建后的入口点文件自动具有执行权限

```bash
# 构建时指定入口点
python -m deepenc build --entry-point src/main.py

# 构建后的目录结构
build/
├── main.py                    # 入口点文件（未加密）
├── conf/                      # 配置文件目录
├── config/                    # 加密配置
└── encrypted/                 # 加密文件
```

## 🚀 部署最佳实践

### 1. 容器化部署

```dockerfile
# Dockerfile
FROM python:3.8-slim

# 安装依赖
COPY requirements.txt .
RUN pip install -r requirements.txt

# 复制加密项目
COPY build/ /app/
WORKDIR /app

# 设置环境变量
ENV AUTH_MODE=PROD
ENV ENCRYPTION_KEY=your-production-key

# 启动应用
CMD ["python", "run.py"]
```

### 2. 环境隔离

```bash
# 生产环境
export AUTH_MODE="PROD"
export ENCRYPTION_KEY="prod-key-32-characters-long"

# 测试环境  
export AUTH_MODE="TEST"
export ENCRYPTION_KEY="test-key-32-characters-long"

# 开发环境
export AUTH_MODE="DEV"
export ENCRYPTION_KEY="dev-key-16-chars"
```

### 3. 健康检查

```python
# health_check.py
import encrypt

def health_check():
    """健康检查"""
    try:
        # 检查系统状态
        system = encrypt.get_system()
        if not system:
            return False, "系统未初始化"
        
        status = system.get_status()
        if not status['initialized']:
            return False, "系统初始化失败"
        
        # 检查关键组件
        if not status['module_loader_installed']:
            return False, "模块加载器未安装"
        
        # 尝试导入关键模块
        try:
            import src.main
            return True, "系统正常"
        except ImportError as e:
            return False, f"关键模块导入失败: {e}"
        
    except Exception as e:
        return False, f"健康检查失败: {e}"

if __name__ == '__main__':
    is_healthy, message = health_check()
    print(f"健康状态: {'✅ 正常' if is_healthy else '❌ 异常'}")
    print(f"详细信息: {message}")
    exit(0 if is_healthy else 1)
```

## 🔧 调试最佳实践

### 1. 调试模式

```python
# 启用调试模式
import os
os.environ['ENCRYPT_DEBUG'] = '1'

import encrypt
import logging

# 设置详细日志
logging.basicConfig(level=logging.DEBUG)

system = encrypt.bootstrap()
```

### 2. 问题诊断

```python
def diagnose_system():
    """系统诊断"""
    print("🔍 系统诊断")
    
    # 检查环境
    print(f"Python 版本: {sys.version}")
    print(f"工作目录: {os.getcwd()}")
    
    # 检查依赖
    try:
        import onnxruntime
        print(f"✅ onnxruntime: {onnxruntime.__version__}")
    except ImportError:
        print("❌ onnxruntime 未安装")
    
    try:
        from Crypto.Cipher import AES
        print("✅ PyCrypto 可用")
    except ImportError:
        print("❌ PyCrypto 未安装")
    
    # 检查加密系统
    system = encrypt.get_system()
    if system:
        status = system.get_status()
        print(f"✅ 加密系统状态: {status}")
    else:
        print("❌ 加密系统未初始化")
```

### 3. 性能分析

```python
import cProfile
import pstats

def profile_encryption():
    """性能分析"""
    
    def test_function():
        system = encrypt.bootstrap()
        # 执行一些操作
        for i in range(10):
            try:
                import src.main
            except ImportError:
                pass
    
    # 运行性能分析
    cProfile.run('test_function()', 'profile_stats')
    
    # 显示结果
    stats = pstats.Stats('profile_stats')
    stats.sort_stats('cumulative')
    stats.print_stats(10)
```

## 📋 维护最佳实践

### 1. 版本管理

```python
# 版本兼容性检查
def check_compatibility():
    import encrypt
    
    required_version = "1.0.0"
    current_version = encrypt.__version__
    
    if current_version != required_version:
        print(f"⚠️ 版本不匹配: 需要 {required_version}, 当前 {current_version}")
```

### 2. 配置管理

```yaml
# config.yaml
encryption:
  algorithm: "AES-CFB"
  key_length: 16
  partial_encryption: true
  
discovery:
  auto_scan: true
  exclude_patterns:
    - "test*"
    - "*.tmp"
  
performance:
  cache_size: 100MB
  temp_cleanup: true
```

### 3. 监控和告警

```python
# 监控关键指标
def setup_monitoring():
    import time
    import threading
    
    def monitor_loop():
        while True:
            system = encrypt.get_system()
            if system:
                status = system.get_status()
                
                # 检查异常状态
                if not status['initialized']:
                    send_alert("加密系统未初始化")
                
                # 检查缓存使用
                cache_info = status.get('module_cache_info', {})
                if cache_info.get('cached_modules', 0) > 100:
                    send_alert("模块缓存过多")
            
            time.sleep(60)  # 每分钟检查一次
    
    # 启动监控线程
    monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
    monitor_thread.start()

def send_alert(message):
    """发送告警"""
    print(f"🚨 告警: {message}")
    # 这里可以集成实际的告警系统
```

## 🔄 CI/CD 集成

### 1. 构建脚本

```bash
#!/bin/bash
# build.sh

set -e

echo "🔨 开始构建加密项目..."

# 检查环境
python --version
python -c "import encrypt; print(f'框架版本: {encrypt.__version__}')"

# 设置构建环境
export AUTH_MODE="PROD"
export ENCRYPTION_KEY="${CI_ENCRYPTION_KEY}"

# 构建项目
python -m encrypt build --project . --verbose

# 验证构建结果
python -m encrypt verify

echo "✅ 构建完成"
```

### 2. 测试脚本

```bash
#!/bin/bash
# test.sh

set -e

echo "🧪 开始测试..."

# 单元测试
python -m pytest tests/ -v

# 集成测试
cd build
python run.py --test-mode

# 性能测试
python -m encrypt profile

echo "✅ 测试完成"
```

### 3. 部署脚本

```bash
#!/bin/bash
# deploy.sh

set -e

echo "🚀 开始部署..."

# 检查构建结果
if [ ! -f "build/run.py" ]; then
    echo "❌ 构建文件不存在"
    exit 1
fi

# 部署到目标环境
rsync -av build/ production_server:/app/

# 重启服务
ssh production_server "systemctl restart your-app"

echo "✅ 部署完成"
```

## 🛡️ 安全最佳实践

### 1. 密钥安全

```bash
# ✅ 使用安全的密钥存储
# 不要在代码中硬编码密钥
# 不要在日志中输出密钥
# 定期轮换密钥

# 使用密钥管理服务
export ENCRYPTION_KEY=$(vault kv get -field=key secret/app/encryption)
```

### 2. 访问控制

```python
# 限制文件访问权限
def secure_file_permissions():
    import stat
    
    # 加密文件只有所有者可读
    for encrypted_file in encrypted_files:
        os.chmod(encrypted_file, stat.S_IRUSR)
    
    # 临时目录限制访问
    temp_dir = '/tmp/encrypt_temp'
    os.makedirs(temp_dir, mode=0o700, exist_ok=True)
```

### 3. 审计日志

```python
# 记录关键操作
import logging

audit_logger = logging.getLogger('encrypt.audit')

def log_operation(operation, details):
    audit_logger.info(f"操作: {operation}, 详情: {details}")

# 使用示例
log_operation("模块解密", {"module": "src.main", "user": "admin"})
log_operation("模型加载", {"model": "eros.onnx", "session_id": "12345"})
```

## 📊 监控最佳实践

### 1. 关键指标

```python
# 定义关键性能指标 (KPI)
KPI_METRICS = {
    'startup_time': 5.0,        # 启动时间 < 5秒
    'decrypt_time': 0.1,        # 解密时间 < 100ms
    'memory_usage': 200,        # 内存使用 < 200MB
    'cache_hit_rate': 0.9,      # 缓存命中率 > 90%
}

def check_kpis():
    system = encrypt.get_system()
    stats = system.get_performance_stats()
    
    for metric, threshold in KPI_METRICS.items():
        current_value = stats.get(metric, 0)
        if current_value > threshold:
            print(f"⚠️ KPI 告警: {metric} = {current_value} > {threshold}")
```

### 2. 健康检查

```python
def comprehensive_health_check():
    """全面健康检查"""
    checks = []
    
    # 检查系统初始化
    system = encrypt.get_system()
    checks.append(("系统初始化", system is not None))
    
    # 检查授权状态
    if system:
        status = system.get_status()
        checks.append(("授权有效", status.get('authorization_valid', False)))
        checks.append(("模块加载器", status.get('module_loader_installed', False)))
        checks.append(("ONNX加载器", status.get('onnx_loader_installed', False)))
    
    # 检查关键文件
    checks.append(("配置文件", os.path.exists('config/encryption_config.json')))
    checks.append(("启动脚本", os.path.exists('run.py')))
    
    # 输出结果
    all_passed = True
    for check_name, passed in checks:
        status_icon = "✅" if passed else "❌"
        print(f"{status_icon} {check_name}")
        if not passed:
            all_passed = False
    
    return all_passed
```

## 🔄 故障恢复

### 1. 自动恢复

```python
def auto_recovery():
    """自动故障恢复"""
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            system = encrypt.bootstrap()
            return system
        except Exception as e:
            print(f"⚠️ 启动失败 (尝试 {attempt + 1}/{max_retries}): {e}")
            
            if attempt < max_retries - 1:
                # 清理和重试
                encrypt.shutdown()
                time.sleep(1)
            else:
                raise
```

### 2. 降级策略

```python
def fallback_strategy():
    """降级策略"""
    try:
        # 尝试完整初始化
        system = encrypt.bootstrap()
    except AuthenticationError:
        print("⚠️ 授权失败，使用只读模式")
        system = encrypt.bootstrap_readonly()
    except Exception as e:
        print(f"⚠️ 初始化失败，使用安全模式: {e}")
        system = encrypt.bootstrap_safe_mode()
    
    return system
```
