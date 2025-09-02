# 安装指南

## 🔧 系统要求

- **Python**: 3.7+
- **操作系统**: Linux (推荐), macOS, Windows
- **内存**: 最少 512MB
- **磁盘空间**: 最少 100MB

## 📦 依赖安装

### 必需依赖

```bash
# 安装核心依赖
pip install pycrypto

# 如果需要 ONNX 支持
pip install onnxruntime

# 或者安装 GPU 版本
pip install onnxruntime-gpu
```

### 可选依赖

```bash
# 性能监控
pip install psutil

# YAML 配置支持
pip install pyyaml

# 进度条显示
pip install tqdm
```

## 🚀 快速安装

### 方式1: 直接使用

```bash
# 1. 进入您的项目目录
cd /path/to/your/project

# 2. 复制 encrypt 框架
cp -r /path/to/encrypt ./

# 3. 设置环境变量
export ENCRYPTION_KEY="your-16-char-key1"

# 4. 构建项目
python -m encrypt build

# 5. 运行项目
cd build && python run.py
```

### 方式2: 作为子模块

```bash
# 1. 添加为 Git 子模块
git submodule add https://github.com/your-repo/encrypt.git encrypt

# 2. 初始化子模块
git submodule update --init --recursive

# 3. 按照方式1的步骤3-5执行
```

## 🔐 密钥配置

### 开发环境

```bash
# 使用环境变量（推荐）
export ENCRYPTION_KEY="dev-key-16chars"
export AUTH_MODE="DEV"

# 或者创建许可证文件
echo "dev-license-content-16chars" > license.dat
```

### 生产环境

#### 方式1: 硬件授权（最安全）

```bash
# 启用硬件授权模式
export AUTH_MODE="PROD"

# 确保硬件授权库可用
# 框架会自动查找以下路径：
# - /usr/local/lib/libhexie_auth.so
# - /usr/lib/libhexie_auth.so
# - ./libhexie_auth.so
```

#### 方式2: 许可证文件

```bash
# 创建生产许可证文件
echo "production-license-content" > /data/appdatas/inference/license.dat
chmod 600 /data/appdatas/inference/license.dat
```

#### 方式3: 环境变量

```bash
# 设置生产密钥
export ENCRYPTION_KEY="prod-key-32-characters-long"
export AUTH_MODE="PROD"
```

## 🐳 Docker 部署

### Dockerfile 示例

```dockerfile
FROM python:3.8-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install -r requirements.txt

# 复制加密项目
COPY build/ /app/
WORKDIR /app

# 设置环境变量
ENV AUTH_MODE=PROD
ENV ENCRYPTION_KEY=your-production-key

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import encrypt; print('OK')" || exit 1

# 启动应用
CMD ["python", "run.py"]
```

### docker-compose.yml 示例

```yaml
version: '3.8'

services:
  encrypted-app:
    build: .
    environment:
      - AUTH_MODE=PROD
      - ENCRYPTION_KEY=${ENCRYPTION_KEY}
    volumes:
      - ./data:/data
      - ./logs:/app/logs
    ports:
      - "8080:8080"
    restart: unless-stopped
    
  # 如果使用 Triton 推理服务器
  triton-server:
    image: nvcr.io/nvidia/tritonserver:latest
    volumes:
      - ./build/encrypted/models:/models
    ports:
      - "8000:8000"
      - "8001:8001"
      - "8002:8002"
    command: tritonserver --model-repository=/models
```

## 🔧 故障排除

### 常见安装问题

#### 1. PyCrypto 安装失败

```bash
# Ubuntu/Debian
sudo apt-get install python3-dev libffi-dev

# CentOS/RHEL
sudo yum install python3-devel libffi-devel

# 重新安装
pip install --upgrade pycrypto
```

#### 2. ONNX Runtime 安装问题

```bash
# 如果默认版本有问题，尝试指定版本
pip install onnxruntime==1.12.0

# 或者使用 CPU 版本
pip uninstall onnxruntime-gpu
pip install onnxruntime
```

#### 3. 权限问题

```bash
# 检查文件权限
ls -la encrypt/
chmod +x encrypt/cli/main.py

# 检查目录权限
chmod 755 encrypt/
```

### 环境验证

```bash
# 验证安装
python -c "
import encrypt
print(f'框架版本: {encrypt.__version__}')

from encrypt.core import AESCrypto, AuthManager
crypto = AESCrypto()
auth = AuthManager()
print('✅ 核心组件正常')

try:
    import onnxruntime
    print(f'✅ ONNX Runtime: {onnxruntime.__version__}')
except ImportError:
    print('⚠️ ONNX Runtime 未安装')
"
```

## 📋 验证清单

安装完成后，请检查以下项目：

- [ ] Python 版本 >= 3.7
- [ ] PyCrypto 已安装
- [ ] ONNX Runtime 已安装（如果需要）
- [ ] 环境变量已设置
- [ ] 框架测试通过
- [ ] 示例代码可以运行
- [ ] 构建命令可以执行

### 完整验证脚本

```bash
#!/bin/bash
# verify_install.sh

echo "🔍 验证安装..."

# 检查 Python 版本
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "Python 版本: $python_version"

# 检查依赖
python3 -c "
try:
    from Crypto.Cipher import AES
    print('✅ PyCrypto 可用')
except ImportError:
    print('❌ PyCrypto 未安装')

try:
    import onnxruntime
    print('✅ ONNX Runtime 可用')
except ImportError:
    print('⚠️ ONNX Runtime 未安装')
"

# 检查环境变量
if [ -n "$ENCRYPTION_KEY" ]; then
    echo "✅ 加密密钥已设置"
else
    echo "⚠️ 加密密钥未设置"
fi

# 测试框架
echo "🧪 测试框架..."
cd encrypt
python test_framework.py

echo "✅ 安装验证完成"
```

## 🆘 获取帮助

如果遇到问题，请：

1. **查看日志**: 启用详细日志输出
   ```bash
   python -m encrypt build --verbose
   ```

2. **运行诊断**: 使用内置诊断工具
   ```bash
   python -m encrypt status
   ```

3. **检查示例**: 运行示例代码
   ```bash
   python encrypt/examples/basic_usage.py
   ```

4. **查看文档**: 阅读详细文档
   - [快速开始](docs/quickstart.md)
   - [API 文档](docs/api.md)
   - [架构设计](docs/architecture.md)
   - [最佳实践](docs/best_practices.md)
