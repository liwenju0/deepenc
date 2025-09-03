# DeepEnc 框架文档

## 🚀 快速开始

### 5分钟上手

```bash
# 1. 安装依赖
pip install pycrypto onnxruntime

# 2. 设置开发环境
mkdir -p /data/appdatas/inference
echo "your-16-char-key" > /data/appdatas/inference/license.dat
export AUTH_MODE="DEV"

# 3. 构建加密项目
cd /path/to/your/project
python -m deepenc build

# 4. 运行项目
cd build
python src/grpc_main.py
```

### 开发者无感知使用

```python
import deepenc

# 自动初始化 - 系统会自动处理加密/解密
deepenc.auto_initialize()

# 现在可以正常导入，系统自动处理
import onnxruntime as ort
from src import grpc_main

# 自动解密 ONNX 模型
session = ort.InferenceSession('model/eros/eros.onnx')
# 自动解密 Python 模块
grpc_main.start_server()
```

## 📚 文档导航

| 文档 | 描述 | 适用场景 |
|------|------|----------|
| **[快速开始](quickstart.md)** | 详细的上手指南和示例 | 新用户入门 |
| **[API 参考](api.md)** | 完整的接口文档和示例 | 开发者参考 |
| **[架构设计](architecture.md)** | 系统架构和设计原理 | 架构师和高级用户 |
| **[最佳实践](best_practices.md)** | 开发、部署和运维指南 | 生产环境部署 |
| **[配置参考](configuration.md)** | 详细的配置选项和说明 | 系统配置和调优 |

## 🎯 核心特性

- **🔐 智能加密**: 自动识别和加密 Python 模块和 ONNX 模型
- **🚀 零配置**: 开箱即用，自动发现项目结构
- **🔄 透明加载**: 开发者完全无感知，无需修改代码
- **⚡ 高性能**: 支持部分加密，最小化性能影响
- **🛡️ 企业级安全**: 支持硬件授权和生产环境部署

## 🔧 常用命令

```bash
# 构建项目
python -m deepenc build

# 扫描项目文件
python -m deepenc scan

# 查看系统状态
python -m deepenc status

# 清理构建目录
python -m deepenc clean
```

## 🏗️ 项目结构

```
your_project/
├── src/                    # 核心源码（自动加密）
│   ├── main.py
│   ├── grpc_main.py
│   └── utils/
├── model/                  # ONNX 模型（自动加密）
├── conf/                   # 配置文件
├── tests/                  # 测试代码（不加密）
├── docs/                   # 文档（不加密）
└── requirements.txt
```

## 🚨 故障排除

### 常见问题

**1. 授权失败**
```bash
# 检查许可证文件
ls -la /data/appdatas/inference/license.dat
# 确保内容为16、24或32字符密钥
cat /data/appdatas/inference/license.dat
```

**2. 模块导入失败**
```bash
# 检查构建结果
ls -la build/encrypted/
# 重新构建项目
python -m deepenc build --clean
```

**3. ONNX 模型加载失败**
```bash
# 检查模型文件
ls -la model/
# 验证 onnxruntime 安装
python -c "import onnxruntime; print('OK')"
```

**4. __file__ 属性错误（已修复）**
```bash
# 如果遇到 __file__ 未定义错误，请确保使用最新版本
# 该问题已在模块加载器中修复，自动设置所有必要的模块属性
```

## 🔧 最近修复

### 模块加载器 __file__ 属性修复

**问题描述**: 在使用加密模块加载器时，遇到 `__file__` 属性未定义的错误。

**修复内容**: 在 `SmartModuleLoader.exec_module()` 方法中添加了 `_setup_module_attributes()` 方法，确保加密模块具有与普通模块相同的属性：

- **`__file__`**: 设置为加密文件的实际路径
- **`__name__`**: 设置为模块的完整名称  
- **`__package__`**: 根据模块名自动推断包名
- **`__cached__`**: 设置为加密文件路径
- **`__loader__`**: 设置为加载器实例
- **`__path__`**: 对于包模块，设置为包目录路径

**修复效果**: 修复后，加密模块加载器会自动设置所有重要的模块属性，确保加密模块能够像普通模块一样正常工作，特别是对于依赖 `__file__` 等属性的代码。

详细修复说明请参考: [模块加载器修复说明](module_loader_fix.md)

## 📞 获取帮助

- **GitHub Issues**: [报告问题](https://github.com/your-repo/deepenc/issues)
- **文档反馈**: [改进建议](https://github.com/your-repo/deepenc/discussions)
- **社区交流**: [技术讨论](https://github.com/your-repo/deepenc/discussions)

---

## 📖 文档结构

```
docs/
├── README.md                    # 主文档（本文档）
├── quickstart.md               # 快速开始指南
├── api.md                      # API 参考文档
├── architecture.md             # 架构设计文档
├── best_practices.md           # 最佳实践指南
├── configuration.md            # 配置参考文档
└── module_loader_fix.md        # 模块加载器修复说明
```

**DeepEnc 团队** - 让加密变得简单 🚀
