# DeepEnc 文档中心

欢迎来到 DeepEnc 文档中心！这里提供了完整的框架使用指南和参考文档。

## 📚 文档概览

### 🚀 快速开始

- **[快速开始指南](quickstart.md)** - 5分钟上手，快速体验框架功能
- **[安装指南](installation.md)** - 详细的安装和配置说明

### 🔌 核心文档

- **[API 文档](api.md)** - 完整的接口参考和示例代码
- **[架构设计](architecture.md)** - 系统架构详解和设计理念
- **[配置参考](configuration.md)** - 配置选项详解和最佳实践

### 🎯 使用指南

- **[最佳实践](best_practices.md)** - 开发、部署和维护的最佳实践
- **[示例代码](examples.md)** - 丰富的使用示例和代码片段
- **[故障排除](troubleshooting.md)** - 常见问题和解决方案

### 🔧 高级主题

- **[性能优化](performance.md)** - 性能调优和监控指南
- **[安全指南](security.md)** - 安全配置和最佳实践
- **[部署指南](deployment.md)** - 生产环境部署方案

## 🎯 学习路径

### 新手用户

1. **开始使用** → [快速开始指南](quickstart.md)
2. **了解架构** → [架构设计](architecture.md)
3. **查看示例** → [示例代码](examples.md)

### 开发者

1. **API 参考** → [API 文档](api.md)
2. **最佳实践** → [最佳实践](best_practices.md)
3. **配置管理** → [配置参考](configuration.md)

### 运维人员

1. **部署指南** → [部署指南](deployment.md)
2. **性能优化** → [性能优化](performance.md)
3. **故障排除** → [故障排除](troubleshooting.md)

## 🔍 快速查找

### 按功能查找

| 功能 | 相关文档 |
|------|----------|
| 项目构建 | [快速开始](quickstart.md), [API 文档](api.md) |
| 系统初始化 | [快速开始](quickstart.md), [API 文档](api.md) |
| 配置管理 | [配置参考](configuration.md) |
| 文件过滤 | [最佳实践](best_practices.md), [API 文档](api.md) |
| 性能优化 | [性能优化](performance.md), [最佳实践](best_practices.md) |
| 安全配置 | [安全指南](security.md), [配置参考](configuration.md) |

### 按场景查找

| 使用场景 | 推荐文档 |
|----------|----------|
| 首次使用 | [快速开始](quickstart.md) |
| 开发环境 | [最佳实践](best_practices.md), [示例代码](examples.md) |
| 生产部署 | [部署指南](deployment.md), [安全指南](security.md) |
| 性能调优 | [性能优化](performance.md) |
| 问题排查 | [故障排除](troubleshooting.md) |

## 📖 文档特色

### 🎨 丰富的示例

每个文档都包含大量实用的代码示例：

```python
# 自动初始化示例
import deepenc
system = deepenc.auto_initialize()

# 自定义构建示例
from deepenc.builders import ProjectBuilder
builder = ProjectBuilder('/path/to/project')
report = builder.build_project()
```

### 🔧 实用工具

文档提供了多种实用工具和脚本：

- 配置验证脚本
- 性能测试工具
- 部署自动化脚本
- 监控和诊断工具

### 🌍 多语言支持

- 中文文档（主要）
- 英文文档（计划中）
- 代码注释多语言

## 🚀 快速体验

### 1. 安装框架

```bash
pip install deepenc
```

### 2. 设置环境

```bash
export ENCRYPTION_KEY="your-16-char-key"
```

### 3. 构建项目

```bash
cd /path/to/your/project
python -m deepenc build
```

### 4. 运行应用

```bash
cd build
python src/grpc_main.py
```

## 🔗 相关资源

### 在线资源

- **GitHub 仓库**: [https://github.com/your-repo/deepenc](https://github.com/your-repo/deepenc)
- **在线文档**: [https://deepenc.readthedocs.io/](https://deepenc.readthedocs.io/)
- **问题反馈**: [GitHub Issues](https://github.com/your-repo/deepenc/issues)

### 社区支持

- **讨论交流**: [GitHub Discussions](https://github.com/your-repo/deepenc/discussions)
- **贡献指南**: [CONTRIBUTING.md](https://github.com/your-repo/deepenc/blob/main/CONTRIBUTING.md)
- **行为准则**: [CODE_OF_CONDUCT.md](https://github.com/your-repo/deepenc/blob/main/CODE_OF_CONDUCT.md)

## 📝 文档反馈

我们非常重视文档质量！如果您发现：

- 文档错误或过时信息
- 缺少重要内容
- 示例代码问题
- 翻译错误

请通过以下方式反馈：

1. **GitHub Issues**: 创建新的 issue
2. **Pull Request**: 直接提交改进
3. **讨论区**: 在 Discussions 中讨论

## 🔄 文档更新

### 更新频率

- **核心文档**: 每次发布更新
- **API 文档**: 功能变更时更新
- **最佳实践**: 定期更新和优化
- **示例代码**: 持续改进和扩展

### 版本对应

| 框架版本 | 文档版本 | 更新日期 |
|----------|----------|----------|
| v1.0.0 | v1.0.0 | 2025-01-XX |
| v0.9.0 | v0.9.0 | 2024-12-XX |
| v0.8.0 | v0.8.0 | 2024-11-XX |

## 🎉 开始使用

现在您已经了解了文档结构，建议从以下文档开始：

1. **[快速开始指南](quickstart.md)** - 快速体验框架功能
2. **[架构设计](architecture.md)** - 了解系统设计理念
3. **[最佳实践](best_practices.md)** - 学习最佳使用方法

祝您使用愉快！🚀

---

**需要帮助？** 请查看 [故障排除](troubleshooting.md) 或创建 [GitHub Issue](https://github.com/your-repo/deepenc/issues)。
