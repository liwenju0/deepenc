# 快速开始指南

## 🚀 5 分钟上手

### 1. 构建加密项目

```bash
# 在您的项目根目录执行
cd /path/to/your/project
python -m encrypt build

# 或者指定项目路径
python -m encrypt build --project /path/to/your/project
```

### 2. 运行加密项目

```bash
# 进入构建目录
cd build

# 运行项目
python run.py
```

### 3. 开发者无感知使用

```python
# 在您的 Python 代码中，完全无需修改
import onnxruntime as ort
from src import grpc_main, nsfw_image_censor

# 系统会自动处理加密/解密
session = ort.InferenceSession('model/eros/eros.onnx')  # 自动解密
grpc_main.start_server()                                # 自动解密导入
```

## 🔧 环境准备

### 必需依赖

```bash
pip install pycrypto onnxruntime
```

### 密钥配置

框架支持多种密钥来源（按优先级排序）：

1. **硬件授权许可证**（生产环境推荐）
2. **许可证文件**
3. **环境变量**

#### 方式1: 环境变量（开发推荐）

```bash
export ENCRYPTION_KEY="your-16-char-key1"
# 或者
export AUTH_CODE="your-encryption-key"
```

#### 方式2: 许可证文件

```bash
# 创建许可证文件
echo "your-license-content" > license.dat

# 或者放在系统目录
echo "your-license-content" > /data/appdatas/inference/license.dat
```

#### 方式3: 硬件授权（生产环境）

```bash
# 设置授权模式
export AUTH_MODE="PROD"

# 确保硬件授权库可用
# 框架会自动查找 libhexie_auth.so
```

## 📋 常用命令

### 扫描项目文件

```bash
# 扫描当前项目
python -m encrypt scan

# 扫描指定项目
python -m encrypt scan --project /path/to/project

# JSON 格式输出
python -m encrypt scan --format json
```

### 查看系统状态

```bash
python -m encrypt status
```

### 清理构建目录

```bash
python -m encrypt clean
```

### 验证构建结果

```bash
python -m encrypt verify
```

## 🎯 高级用法

### 自定义过滤规则

```python
from encrypt.builders import ProjectBuilder
from encrypt.discovery import FileFilter

# 创建自定义过滤器
custom_rules = {
    'exclude_dirs': ['my_test_dir'],
    'exclude_files': ['config.py'],
    'include_files': ['important.py']  # 强制包含
}

# 使用自定义规则构建
builder = ProjectBuilder()
builder.scanner.file_filter = FileFilter(custom_rules)
build_report = builder.build_project()
```

### 手动初始化系统

```python
import encrypt

# 手动配置模块映射
module_config = {
    'src.main': 'encrypted/python/src/main.py.encrypted',
    'src.utils': 'encrypted/python/src/utils.py.encrypted'
}

# 初始化系统
system = encrypt.initialize(module_config)

# 现在可以正常导入加密模块
from src import main, utils
```

### 获取系统信息

```python
import encrypt

# 获取系统实例
system = encrypt.get_system()

if system:
    # 获取状态信息
    status = system.get_status()
    print(f"系统状态: {status}")
    
    # 清理缓存
    system.clear_caches()
```

## 🛠️ 故障排除

### 常见问题

#### 1. 加密密钥错误

```
❌ 授权系统初始化失败: 无法获取有效的加密密钥
```

**解决方案:**
- 检查环境变量 `ENCRYPTION_KEY` 是否设置
- 确保密钥长度为 16、24 或 32 字符
- 检查许可证文件是否存在且可读

#### 2. 模块导入失败

```
❌ 执行模块失败 src.main: 解密模块失败
```

**解决方案:**
- 检查加密文件是否存在
- 验证密钥是否正确
- 确保文件权限正确

#### 3. ONNX 模型加载失败

```
❌ 加载模型失败: 解密文件失败
```

**解决方案:**
- 检查 onnxruntime 是否正确安装
- 验证模型文件是否完整
- 检查临时目录权限

### 调试模式

```bash
# 启用详细输出
python -m encrypt build --verbose

# 或者在代码中
import encrypt
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 重置系统

```python
import encrypt

# 关闭系统
encrypt.shutdown()

# 重新初始化
system = encrypt.initialize()
```

## 📚 更多文档

- [API 文档](api.md)
- [架构设计](architecture.md)
- [配置参考](configuration.md)
- [最佳实践](best_practices.md)
