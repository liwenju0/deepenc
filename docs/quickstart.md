# 快速开始指南

## 🚀 5分钟上手

### 1. 环境准备

```bash
# 安装依赖
pip install pycrypto onnxruntime

# 设置开发环境
mkdir -p /data/appdatas/inference
echo "your-16-char-key" > /data/appdatas/inference/license.dat
export AUTH_MODE="DEV"
```

### 2. 构建加密项目

```bash
# 在项目根目录执行
cd /path/to/your/project
python -m deepenc build

# 指定自定义入口文件
python -m deepenc build --entry-point src/main.py
```

### 3. 运行加密项目

```bash
# 进入构建目录
cd build

# 运行项目
python src/grpc_main.py
# 或者使用自定义入口文件
python main.py
```

## 🔧 开发者无感知使用

### 方式1: 自动初始化（推荐）

```python
import deepenc

# 自动初始化 - 系统会自动查找配置文件
deepenc.auto_initialize()

# 现在可以正常导入，系统会自动处理加密/解密
import onnxruntime as ort
from src import grpc_main

# 系统会自动处理加密/解密
session = ort.InferenceSession('model/eros/eros.onnx')  # 自动解密
grpc_main.start_server()                                # 自动解密导入
```

### 方式2: 手动配置

```python
import deepenc

# 手动配置模块映射
module_config = {
    'src.main': 'encrypted/python/src/main.py.encrypted',
    'src.utils': 'encrypted/python/src/utils.py.encrypted'
}

# 初始化系统
system = deepenc.initialize(module_config)

# 现在可以正常导入加密模块
from src import main, utils
```

## 📋 常用命令

```bash
# 扫描项目文件
python -m deepenc scan

# 查看系统状态
python -m deepenc status

# 清理构建目录
python -m deepenc clean

# 验证构建结果
python -m deepenc verify
```

## 🎯 高级用法

### 自定义过滤规则

```python
from deepenc.builders import ProjectBuilder
from deepenc.discovery import FileFilter

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

### 系统生命周期管理

```python
import deepenc

# 启动系统
system = deepenc.bootstrap()

# 检查系统状态
if deepenc.is_initialized():
    print("系统已启动")

# 关闭系统
deepenc.shutdown()

# 重新启动
system = deepenc.initialize()
```

## 🛠️ 故障排除

### 常见问题

#### 1. 加密密钥错误

```
❌ 授权系统初始化失败: 无法获取有效的加密密钥
```

**解决方案:**
- 检查许可证文件 `/data/appdatas/inference/license.dat` 是否存在
- 确保许可证文件内容为有效的16、24或32字符密钥
- 检查许可证文件权限是否正确

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
python -m deepenc build --verbose

# 或者在代码中
import deepenc
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 更多文档

- [API 文档](api.md) - 完整的接口参考
- [架构设计](architecture.md) - 系统架构和设计原理
- [最佳实践](best_practices.md) - 开发、部署和运维指南
- [配置参考](configuration.md) - 详细的配置选项
