# 文档索引

## 📋 文档概览

DeepEnc 框架提供完整的文档体系，帮助您快速上手和深入使用：

### 🚀 入门文档

- **[快速开始指南](quickstart.md)** - 5分钟上手，零基础入门
- **[安装配置](configuration.md)** - 详细的安装和配置说明
- **[API 文档](api.md)** - 完整的接口参考和示例

### 🏗️ 架构设计

- **[架构设计](architecture.md)** - 系统架构、设计原则和组件说明
- **[最佳实践](best_practices.md)** - 开发、部署和运维最佳实践

### 🔧 工具和示例

- **[命令行工具](quickstart.md#命令行工具)** - CLI 工具使用说明
- **[部署示例](best_practices.md#部署最佳实践)** - Docker、Kubernetes 部署
- **[故障排除](quickstart.md#故障排除)** - 常见问题和解决方案

## 🎯 学习路径

### 👶 新用户入门

1. **快速体验** → [快速开始指南](quickstart.md)
2. **了解架构** → [架构设计](architecture.md)
3. **深入学习** → [最佳实践](best_practices.md)

### 👨‍💻 开发者进阶

1. **API 使用** → [API 文档](api.md)
2. **配置管理** → [配置参考](configuration.md)
3. **性能优化** → [最佳实践](best_practices.md#性能优化最佳实践)

### 🚀 运维部署

1. **部署准备** → [配置参考](configuration.md)
2. **容器部署** → [最佳实践](best_practices.md#docker-部署)
3. **监控调试** → [架构设计](architecture.md#监控和调试)

## 🔍 快速查找

### 按功能查找

| 功能 | 相关文档 | 关键章节 |
|------|----------|----------|
| **项目构建** | [快速开始](quickstart.md) | 构建加密项目 |
| **模块导入** | [快速开始](quickstart.md) | 开发者无感知使用 |
| **系统启动** | [API 文档](api.md) | 系统启动器 |
| **文件发现** | [API 文档](api.md) | 发现接口 |
| **错误处理** | [API 文档](api.md) | 错误处理 |
| **性能优化** | [最佳实践](best_practices.md) | 性能优化最佳实践 |
| **安全配置** | [配置参考](configuration.md) | 许可证文件配置 |
| **部署配置** | [最佳实践](best_practices.md) | 部署最佳实践 |

### 按场景查找

| 使用场景 | 推荐文档 | 说明 |
|----------|----------|------|
| **快速原型** | [快速开始](quickstart.md) | 5分钟上手 |
| **生产部署** | [最佳实践](best_practices.md) | 企业级部署指南 |
| **性能调优** | [最佳实践](best_practices.md) | 性能优化策略 |
| **故障排查** | [快速开始](quickstart.md) | 常见问题解决 |
| **架构设计** | [架构设计](architecture.md) | 系统设计原理 |
| **配置管理** | [配置参考](configuration.md) | 完整配置选项 |

## ✨ 文档特色

### 📚 丰富示例

每个文档都包含大量实际代码示例：

```python
# 自动初始化示例
import deepenc
system = deepenc.auto_initialize()

# 手动配置示例
module_config = {
    'src.main': 'encrypted/python/src/main.py.encrypted'
}
system = deepenc.initialize(module_config)
```

### 🛠️ 实用工具

提供完整的工具链支持：

- **CLI 工具**: `deepenc build`, `deepenc scan`, `deepenc status`
- **Python API**: 完整的编程接口
- **配置管理**: 支持多种配置格式

### 🌍 多语言支持

- **中文文档**: 完整的中文文档体系
- **代码示例**: 清晰的代码注释和说明
- **国际化**: 支持多语言环境

## 🚀 快速体验

### 1. 环境准备

```bash
# 安装依赖
pip install pycrypto onnxruntime

# 设置开发环境
make dev-setup

# 或者手动设置
mkdir -p /data/appdatas/inference
echo "your-16-char-key" > /data/appdatas/inference/license.dat
export AUTH_MODE="DEV"
```

### 2. 构建项目

```bash
# 在项目根目录执行
cd /path/to/your/project
python -m deepenc build

# 查看构建结果
ls -la build/
```

### 3. 运行应用

```python
# 在您的代码中
import deepenc

# 自动初始化
deepenc.auto_initialize()

# 正常导入和使用
from src import main
main.run()
```

### 4. 验证结果

```bash
# 检查系统状态
python -m deepenc status

# 验证构建结果
python -m deepenc verify
```

## 🔗 相关资源

### 📖 在线资源

- **GitHub 仓库**: [https://github.com/your-repo/deepenc](https://github.com/your-repo/deepenc)
- **在线文档**: [https://deepenc.readthedocs.io/](https://deepenc.readthedocs.io/)
- **问题反馈**: [GitHub Issues](https://github.com/your-repo/deepenc/issues)

### 💬 社区交流

- **技术讨论**: [GitHub Discussions](https://github.com/your-repo/deepenc/discussions)
- **使用交流**: [社区论坛](https://community.deepenc.io/)
- **邮件列表**: [deepenc-users@googlegroups.com](mailto:deepenc-users@googlegroups.com)

### 📚 学习资源

- **示例项目**: [examples/](https://github.com/your-repo/deepenc/examples)
- **视频教程**: [YouTube 频道](https://www.youtube.com/c/DeepEnc)
- **在线课程**: [学习平台](https://learn.deepenc.io/)

## 📝 文档反馈

### 🐛 报告问题

如果您发现文档中的错误或问题：

1. **GitHub Issues**: 在 [GitHub Issues](https://github.com/your-repo/deepenc/issues) 中报告
2. **邮件反馈**: 发送邮件到 [docs@deepenc.io](mailto:docs@deepenc.io)
3. **社区讨论**: 在 [GitHub Discussions](https://github.com/your-repo/deepenc/discussions) 中讨论

### 💡 改进建议

我们欢迎所有改进建议：

- **内容补充**: 添加缺失的文档内容
- **示例改进**: 提供更好的代码示例
- **结构优化**: 改进文档组织结构
- **翻译支持**: 添加更多语言支持

### 🤝 贡献文档

参与文档改进：

1. **Fork 项目**: 复制项目到您的账户
2. **创建分支**: 为改进创建新分支
3. **提交更改**: 提交您的改进
4. **发起 PR**: 创建 Pull Request

## 📅 文档更新

### 🔄 更新频率

- **核心文档**: 每两周更新一次
- **API 文档**: 每次发布新版本时更新
- **最佳实践**: 每月更新一次
- **示例代码**: 根据用户反馈持续更新

### 📋 更新日志

| 版本 | 更新日期 | 主要变更 |
|------|----------|----------|
| **1.0.0** | 2024-01-15 | 初始版本发布 |
| **1.0.1** | 2024-01-20 | 修复配置文档 |
| **1.0.2** | 2024-01-25 | 添加部署示例 |
| **1.1.0** | 2024-02-01 | 架构文档重构 |

### 🔍 变更通知

- **邮件订阅**: 订阅文档更新通知
- **RSS 订阅**: 通过 RSS 获取更新
- **GitHub Watch**: 关注仓库获取通知
- **社区公告**: 在社区中发布重要更新

---

**DeepEnc 文档团队** - 致力于提供最好的文档体验 📚✨

如有任何问题或建议，请随时联系我们！
