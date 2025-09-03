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
├── eros/               # 按功能分组
│   ├── eros.onnx
│   └── config.json
├── mars/               # 按功能分组
│   ├── mars.onnx
│   └── config.json
└── shared/             # 共享模型
    └── common.onnx
```

## 🚀 系统初始化最佳实践

### 1. 自动初始化（推荐）

```python
# ✅ 推荐做法：自动初始化
import deepenc

# 系统会自动查找配置文件
system = deepenc.auto_initialize()

# 如果自动初始化失败，使用快速启动
if not system:
    system = deepenc.quick_start()

# 现在可以正常导入
from src import main
```

**优势:**
- 零配置，开箱即用
- 自动发现配置文件
- 智能降级机制
- 适合开发和测试环境

### 2. 手动配置（生产环境）

```python
# ✅ 生产环境：手动配置
import deepenc

# 明确的模块映射
module_config = {
    'src.main': 'encrypted/python/src/main.py.encrypted',
    'src.detector': 'encrypted/python/src/detector.py.encrypted',
    'src.classifier': 'encrypted/python/src/classifier.py.encrypted'
}

# 初始化系统
system = deepenc.initialize(module_config)

# 验证系统状态
if not deepenc.is_initialized():
    raise RuntimeError("加密系统初始化失败")
```

**优势:**
- 配置明确，便于管理
- 性能可预测
- 便于调试和监控
- 适合生产环境

### 3. 生命周期管理

```python
# ✅ 完整的生命周期管理
import deepenc
import atexit

def cleanup():
    """清理资源"""
    if deepenc.is_initialized():
        deepenc.shutdown()

# 注册清理函数
atexit.register(cleanup)

try:
    # 启动系统
    system = deepenc.bootstrap()
    
    # 使用系统
    from src import main
    main.run()
    
finally:
    # 确保清理
    cleanup()
```

## 🔧 构建最佳实践

### 1. 构建流程优化

```bash
# ✅ 推荐的构建流程
# 1. 清理环境
python -m deepenc clean

# 2. 扫描项目
python -m deepenc scan --format json

# 3. 构建项目
python -m deepenc build --entry-point src/main.py

# 4. 验证构建结果
python -m deepenc verify
```

### 2. 自定义过滤规则

```python
# ✅ 自定义过滤规则
from deepenc.builders import ProjectBuilder
from deepenc.discovery import FileFilter

# 创建过滤器
filter_rules = {
    'exclude_dirs': [
        'tests',           # 测试目录
        'docs',            # 文档目录
        'examples',        # 示例目录
        '__pycache__',     # Python缓存
        '.git'             # Git目录
    ],
    'exclude_files': [
        '*.pyc',           # Python字节码
        '*.pyo',           # Python优化字节码
        '*.log',           # 日志文件
        'config.py',       # 配置文件
        'setup.py'         # 安装脚本
    ],
    'include_files': [
        'src/main.py',     # 强制包含
        'src/core.py'      # 强制包含
    ]
}

# 应用过滤器
builder = ProjectBuilder()
builder.scanner.file_filter = FileFilter(filter_rules)
```

### 3. 构建配置管理

```python
# ✅ 构建配置管理
import json
from pathlib import Path

# 构建配置
build_config = {
    'project_root': '/path/to/project',
    'build_dir': '/path/to/build',
    'entry_point': 'src/main.py',
    'exclude_patterns': [
        'tests/**',
        'docs/**',
        '*.pyc'
    ],
    'encryption_settings': {
        'algorithm': 'AES-CFB',
        'key_length': 256,
        'partial_encryption': True,
        'max_encrypt_size': 10 * 1024 * 1024  # 10MB
    }
}

# 保存配置
config_path = Path('build_config.json')
with open(config_path, 'w') as f:
    json.dump(build_config, f, indent=2)
```

## 🔐 安全最佳实践

### 1. 密钥管理

```python
# ✅ 安全的密钥管理
import os
from pathlib import Path

# 环境变量方式（开发环境）
os.environ['ENCRYPTION_KEY'] = 'your-16-char-key'

# 许可证文件方式（生产环境）
license_path = Path('/data/appdatas/inference/license.dat')
if license_path.exists():
    with open(license_path, 'r') as f:
        license_content = f.read().strip()
    os.environ['AUTH_CODE'] = license_content

# 硬件授权方式（最高安全）
os.environ['AUTH_MODE'] = 'PROD'
```

### 2. 文件权限管理

```bash
# ✅ 安全的文件权限
# 构建目录权限
chmod 755 build/
chmod 644 build/config/*.json
chmod 600 build/config/encryption_config.json

# 运行时目录权限
chmod 755 /data/appdatas/inference/
chmod 600 /data/appdatas/inference/license.dat
```

### 3. 网络安全

```python
# ✅ 网络安全配置
# 避免在日志中记录敏感信息
import logging

class SecureFormatter(logging.Formatter):
    def format(self, record):
        # 过滤敏感信息
        if hasattr(record, 'msg'):
            record.msg = self._filter_sensitive(record.msg)
        return super().format(record)
    
    def _filter_sensitive(self, msg):
        # 过滤密钥、路径等敏感信息
        sensitive_patterns = [
            r'ENCRYPTION_KEY=\w+',
            r'/data/appdatas/inference/',
            r'license\.dat'
        ]
        # 实现过滤逻辑
        return msg

# 应用安全格式化器
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 📊 性能优化最佳实践

### 1. 缓存策略

```python
# ✅ 缓存优化
import deepenc

# 启动系统
system = deepenc.bootstrap()

# 预热缓存
def warm_up_cache():
    """预热常用模块的缓存"""
    try:
        from src import detector, classifier
        print("缓存预热完成")
    except ImportError as e:
        print(f"缓存预热失败: {e}")

# 定期清理缓存
import time
def cache_maintenance():
    """定期维护缓存"""
    while True:
        time.sleep(3600)  # 每小时
        if deepenc.is_initialized():
            system = deepenc.get_system()
            system.clear_caches()
            print("缓存已清理")
```

### 2. 内存管理

```python
# ✅ 内存管理
import gc
import psutil

def monitor_memory():
    """监控内存使用"""
    process = psutil.Process()
    memory_info = process.memory_info()
    
    print(f"内存使用: {memory_info.rss / 1024 / 1024:.2f} MB")
    
    # 如果内存使用过高，清理缓存
    if memory_info.rss > 500 * 1024 * 1024:  # 500MB
        if deepenc.is_initialized():
            system = deepenc.get_system()
            system.clear_caches()
            gc.collect()
            print("内存已清理")

# 定期监控
import threading
def start_memory_monitor():
    """启动内存监控"""
    def monitor():
        while True:
            monitor_memory()
            time.sleep(300)  # 每5分钟
    
    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()
```

### 3. 并发处理

```python
# ✅ 并发处理
import concurrent.futures
from deepenc import bootstrap

def process_batch(items):
    """批量处理"""
    # 启动系统
    system = bootstrap()
    
    def process_item(item):
        try:
            from src import processor
            return processor.process(item)
        except Exception as e:
            return f"处理失败: {e}"
    
    # 使用线程池
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_item, item) for item in items]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    return results
```

## 🧪 测试最佳实践

### 1. 单元测试

```python
# ✅ 单元测试
import unittest
from unittest.mock import patch, MagicMock
import deepenc

class TestDeepEnc(unittest.TestCase):
    
    def setUp(self):
        """测试前准备"""
        # 清理之前的系统
        if deepenc.is_initialized():
            deepenc.shutdown()
    
    def tearDown(self):
        """测试后清理"""
        if deepenc.is_initialized():
            deepenc.shutdown()
    
    def test_auto_initialize(self):
        """测试自动初始化"""
        with patch('pathlib.Path.exists', return_value=False):
            system = deepenc.auto_initialize()
            self.assertIsNotNone(system)
    
    def test_manual_initialize(self):
        """测试手动初始化"""
        module_config = {'test.module': 'test/path'}
        system = deepenc.initialize(module_config)
        self.assertIsNotNone(system)
    
    def test_system_lifecycle(self):
        """测试系统生命周期"""
        # 启动
        system = deepenc.bootstrap()
        self.assertTrue(deepenc.is_initialized())
        
        # 关闭
        deepenc.shutdown()
        self.assertFalse(deepenc.is_initialized())

if __name__ == '__main__':
    unittest.main()
```

### 2. 集成测试

```python
# ✅ 集成测试
import tempfile
import shutil
from pathlib import Path
from deepenc.builders import ProjectBuilder

class TestIntegration(unittest.TestCase):
    
    def setUp(self):
        """创建临时测试环境"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.build_dir = self.test_dir / 'build'
        
        # 创建测试项目结构
        self._create_test_project()
    
    def tearDown(self):
        """清理测试环境"""
        shutil.rmtree(self.test_dir)
    
    def _create_test_project(self):
        """创建测试项目"""
        # 创建源码目录
        src_dir = self.test_dir / 'src'
        src_dir.mkdir()
        
        # 创建测试文件
        (src_dir / '__init__.py').write_text('')
        (src_dir / 'main.py').write_text('print("Hello, World!")')
        
        # 创建模型目录
        model_dir = self.test_dir / 'model'
        model_dir.mkdir()
        (model_dir / 'test.onnx').write_text('fake onnx content')
    
    def test_full_build_and_run(self):
        """测试完整的构建和运行流程"""
        # 构建项目
        builder = ProjectBuilder(
            project_root=str(self.test_dir),
            build_dir=str(self.build_dir)
        )
        
        report = builder.build_project()
        self.assertTrue(report['build_info']['success'])
        
        # 验证构建结果
        self.assertTrue((self.build_dir / 'src' / 'main.py').exists())
        self.assertTrue((self.build_dir / 'model' / 'test.onnx.encrypt').exists())
```

### 3. 性能测试

```python
# ✅ 性能测试
import time
import statistics
from deepenc import bootstrap

class TestPerformance(unittest.TestCase):
    
    def test_initialization_performance(self):
        """测试初始化性能"""
        times = []
        
        for _ in range(10):
            start_time = time.time()
            system = bootstrap()
            end_time = time.time()
            
            times.append(end_time - start_time)
            deepenc.shutdown()
        
        avg_time = statistics.mean(times)
        max_time = max(times)
        
        print(f"平均初始化时间: {avg_time:.3f}s")
        print(f"最大初始化时间: {max_time:.3f}s")
        
        # 性能要求：平均时间 < 100ms
        self.assertLess(avg_time, 0.1)
    
    def test_module_import_performance(self):
        """测试模块导入性能"""
        system = bootstrap()
        
        try:
            # 测试导入性能
            import_times = []
            
            for _ in range(100):
                start_time = time.time()
                # 这里应该导入一个测试模块
                end_time = time.time()
                import_times.append(end_time - start_time)
            
            avg_import_time = statistics.mean(import_times)
            print(f"平均导入时间: {avg_import_time:.3f}s")
            
            # 性能要求：平均导入时间 < 50ms
            self.assertLess(avg_import_time, 0.05)
            
        finally:
            deepenc.shutdown()
```

## 🚀 部署最佳实践

### 1. 容器化部署

```dockerfile
# ✅ Dockerfile 最佳实践
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制加密项目
COPY build/ .

# 设置环境变量
ENV PYTHONPATH=/app
ENV ENCRYPTION_KEY=your-production-key

# 创建非 root 用户
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import deepenc; print('OK')" || exit 1

# 启动应用
CMD ["python", "main.py"]
```

### 2. Kubernetes 部署

```yaml
# ✅ Kubernetes 部署配置
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deepenc-app
  labels:
    app: deepenc-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: deepenc-app
  template:
    metadata:
      labels:
        app: deepenc-app
    spec:
      containers:
      - name: deepenc-app
        image: your-registry/deepenc-app:latest
        ports:
        - containerPort: 8080
        env:
        - name: ENCRYPTION_KEY
          valueFrom:
            secretKeyRef:
              name: deepenc-secret
              key: encryption-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Secret
metadata:
  name: deepenc-secret
type: Opaque
data:
  encryption-key: <base64-encoded-key>
```

### 3. 监控和日志

```python
# ✅ 监控和日志配置
import logging
import json
from datetime import datetime
from deepenc import bootstrap

# 配置结构化日志
class StructuredFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # 添加异常信息
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry)

# 配置日志
def setup_logging():
    """配置日志系统"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(StructuredFormatter())
    logger.addHandler(console_handler)
    
    # 文件处理器
    file_handler = logging.FileHandler('deepenc.log')
    file_handler.setFormatter(StructuredFormatter())
    logger.addHandler(file_handler)

# 启动监控
def start_monitoring():
    """启动监控"""
    setup_logging()
    
    # 启动系统
    system = bootstrap()
    
    # 记录启动信息
    logging.info("DeepEnc 系统已启动", extra={
        'system_status': 'running',
        'version': '1.0.0'
    })
    
    return system

if __name__ == '__main__':
    system = start_monitoring()
    # 运行应用
```

## 🔮 未来规划建议

### 1. 短期优化

- **性能优化**: 进一步提升解密性能，目标 < 50ms
- **缓存优化**: 实现智能缓存策略，提高缓存命中率
- **错误处理**: 提供更友好的错误信息和恢复建议

### 2. 中期扩展

- **分布式支持**: 支持 Redis 等分布式缓存
- **云原生**: 支持 Kubernetes、Docker Swarm 等平台
- **配置管理**: 支持配置热更新和版本管理

### 3. 长期愿景

- **AI 增强**: 智能配置推荐和性能优化
- **多语言支持**: 支持 Java、Go 等其他语言
- **生态系统**: 构建完整的加密分发生态系统
