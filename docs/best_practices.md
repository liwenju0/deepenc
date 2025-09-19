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
├── eros/               # 按功能分类
│   ├── model.onnx
│   └── config.json
├── mars/
│   ├── model.onnx
│   └── config.json
└── shared/             # 共享模型
    └── common.onnx
```

## 🚀 部署最佳实践

### 1. 环境配置

#### 开发环境

```bash
# 设置开发模式
export AUTH_MODE="DEV"

# 创建许可证文件
mkdir -p /data/appdatas/inference
echo "your-16-char-key" > /data/appdatas/inference/license.dat
```

#### 生产环境

```bash
# 设置生产模式
export AUTH_MODE="PROD"

# 使用硬件授权
export HARDWARE_AUTH="1"
```

### 2. Docker 部署

```dockerfile
# 多阶段构建
FROM python:3.9-slim as builder

# 构建阶段
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python -m deepenc build

# 运行阶段
FROM python:3.9-slim

WORKDIR /app
COPY --from=builder /build/build/ .

# 设置环境变量
ENV AUTH_MODE=PROD

# 创建非 root 用户
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

CMD ["python", "main.py"]
```

### 3. Kubernetes 部署

```yaml
# 部署配置
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deepenc-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: deepenc-app
  template:
    spec:
      containers:
      - name: deepenc-app
        image: your-registry/deepenc-app:latest
        env:
        - name: AUTH_MODE
          value: "PROD"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        volumeMounts:
        - name: license-volume
          mountPath: /data/appdatas/inference
          readOnly: true
      volumes:
      - name: license-volume
        secret:
          secretName: deepenc-license
---
# 许可证密钥
apiVersion: v1
kind: Secret
metadata:
  name: deepenc-license
type: Opaque
data:
  license.dat: <base64-encoded-license>
```

## ⚡ 性能优化最佳实践

### 1. 缓存策略

```python
# 启用智能缓存
import deepenc

# 设置缓存大小
os.environ['ENCRYPT_CACHE_SIZE'] = '200'  # 200MB

# 初始化系统
system = deepenc.auto_initialize()

# 清理缓存（定期执行）
system.clear_caches()
```

### 2. 并发处理

```python
# 设置工作线程数（如果支持）
# os.environ['ENCRYPT_MAX_WORKERS'] = '8'

# 使用线程池处理多个文件
import concurrent.futures

def process_files(file_list):
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(process_single_file, f) for f in file_list]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    return results
```

### 3. 内存管理

```python
# 监控内存使用
import psutil
import gc

def monitor_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    
    if memory_info.rss > 500 * 1024 * 1024:  # 500MB
        print("内存使用过高，清理缓存...")
        gc.collect()
        system.clear_caches()
```

## 🛡️ 安全最佳实践

### 1. 密钥管理

```bash
# 设置安全的文件权限
chmod 600 /data/appdatas/inference/license.dat
chown root:root /data/appdatas/inference/license.dat
```

### 2. 网络安全

```python
# 限制网络访问
import socket

def restrict_network_access():
    # 只允许本地访问
    if not socket.gethostname().startswith('localhost'):
        raise SecurityError("只允许本地访问")
```

## 🔍 监控和调试最佳实践

### 1. 系统监控

```python
# 系统健康检查
def health_check():
    try:
        # 检查系统状态
        status = deepenc.get_system().get_status()
        
        # 检查关键指标
        if status['memory_usage'] > 80:  # 80%
            return False, "内存使用过高"
        
        if status['loaded_modules'] == 0:
            return False, "没有加载的模块"
        
        return True, "系统正常"
        
    except Exception as e:
        return False, f"健康检查失败: {e}"
```

### 2. 日志管理

```python
# 结构化日志
import logging
import json

class StructuredLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
    
    def log_operation(self, operation, details):
        log_entry = {
            'timestamp': time.time(),
            'operation': operation,
            'details': details,
            'level': 'INFO'
        }
        self.logger.info(json.dumps(log_entry))
```

### 3. 性能分析

```python
# 性能监控装饰器
import time
from functools import wraps

def performance_monitor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        if execution_time > 1.0:  # 超过1秒记录警告
            logging.warning(f"函数 {func.__name__} 执行时间过长: {execution_time:.2f}s")
        
        return result
    return wrapper

# 使用示例
@performance_monitor
def slow_function():
    time.sleep(2)
```

## 🚨 故障排除最佳实践

### 1. 常见问题诊断

```bash
# 1. 检查系统状态
python -m deepenc status

# 2. 检查许可证
ls -la /data/appdatas/inference/
cat /data/appdatas/inference/license.dat

# 3. 检查构建结果
ls -la build/encrypted/
```

### 2. 调试模式

```python
# 启用详细调试
import logging
logging.basicConfig(level=logging.DEBUG)

# 获取详细状态
system = deepenc.get_system()
if system:
    print(json.dumps(system.get_status(), indent=2))
```

### 3. 性能问题排查

```python
# 内存泄漏检测
import tracemalloc

def detect_memory_leak():
    tracemalloc.start()
    
    # 执行操作
    for i in range(100):
        process_files(large_file_list)
    
    # 检查内存使用
    current, peak = tracemalloc.get_traced_memory()
    print(f"当前内存使用: {current / 1024 / 1024:.1f} MB")
    print(f"峰值内存使用: {peak / 1024 / 1024:.1f} MB")
    
    tracemalloc.stop()
```

## 📊 测试最佳实践

### 1. 单元测试

```python
# tests/test_detector.py
import unittest
from unittest.mock import patch
from src.detector import Detector

class TestDetector(unittest.TestCase):
    def setUp(self):
        self.detector = Detector()
    
    @patch('src.detector.ort.InferenceSession')
    def test_detector_initialization(self, mock_session):
        # 测试检测器初始化
        self.assertIsNotNone(self.detector)
        mock_session.assert_called_once()
    
    def test_detector_detection(self):
        # 测试检测功能
        result = self.detector.detect(test_image)
        self.assertIsInstance(result, dict)
```

### 2. 集成测试

```python
# tests/test_integration.py
class TestIntegration(unittest.TestCase):
    def setUp(self):
        # 初始化加密系统
        self.system = deepenc.auto_initialize()
    
    def test_end_to_end_workflow(self):
        # 测试完整工作流程
        from src import main
        
        # 执行主流程
        result = main.run()
        self.assertTrue(result['success'])
    
    def tearDown(self):
        # 清理资源
        deepenc.shutdown()
```

## 🔄 持续集成最佳实践

### 1. CI/CD 流水线

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/ -v
    
    - name: Build project
      run: |
        python -m deepenc build
    
    - name: Verify build
      run: |
        python -m deepenc verify
```

### 2. 自动化测试

```bash
#!/bin/bash
# scripts/run_tests.sh

echo "🧪 运行单元测试..."
python -m pytest tests/unit/ -v

echo "🔗 运行集成测试..."
python -m pytest tests/integration/ -v

echo "🏗️ 构建项目..."
python -m deepenc build

echo "✅ 验证构建结果..."
python -m deepenc verify

echo "🎉 所有测试通过！"
```

## 📚 总结

遵循这些最佳实践可以确保：

1. **代码质量**: 清晰的模块结构和接口设计
2. **性能优化**: 合理的缓存策略和并发处理
3. **安全可靠**: 完善的密钥管理
4. **易于维护**: 全面的测试覆盖和监控体系
5. **生产就绪**: 容器化部署和自动化运维

---

**DeepEnc 最佳实践团队** - 助力构建高质量加密应用 🚀
