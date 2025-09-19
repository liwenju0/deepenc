# ZIP 包生成功能

## 概述

deepenc 现在支持在构建完成后自动生成带密码的 ZIP 包。这个功能可以帮助用户更方便地分发和部署加密后的项目。

## 使用方法

### 基本用法

```bash
# 构建项目并生成zip包
deepenc build --genzip

# 指定项目路径并生成zip包
deepenc build --project /path/to/project --genzip

# 结合其他参数使用
deepenc build --project /path/to/project --genzip --verbose
```

### 参数说明

- `--genzip`: 启用zip包生成功能
- 其他参数与普通 `build` 命令相同

## 功能特性

### 自动版本检测

- 自动读取项目根目录下的 `VERSION` 文件
- 支持任意格式的版本号（如：`1.0.0`、`v2.1.3`、`release-2024.01` 等）

### 智能命名

- 自动从项目目录名获取项目名称
- 生成格式：`{projectname}.{version}.zip`
- 示例：`myproject.1.2.3.zip`

### 密码保护

- 支持从环境变量 `UNZIP_CODE` 读取密码
- 如果环境变量未设置，使用默认密码：`deepenc`
- 密码用于保护zip包内容

### 目录结构

生成的zip包包含构建目录下的所有文件，目录结构如下：

```
projectname.version.zip
├── encrypted/
│   ├── main.py
│   └── utils.py
├── config.json
└── bootstrap.py
```

## 环境变量配置

### 设置自定义密码

```bash
# Linux/macOS
export UNZIP_CODE="your_custom_password"

# Windows
set UNZIP_CODE=your_custom_password

# 然后运行命令
deepenc build --genzip
```

### 使用默认密码

如果不设置环境变量，系统将使用默认密码：`deepenc`

## 输出位置

zip包将生成在以下位置：

```
{project_root}/build/dist/{projectname}.{version}.zip
```

## 错误处理

### 常见错误

1. **VERSION文件不存在**
   ```
   ⚠️ 项目根目录下未找到VERSION文件: /path/to/project/VERSION
   ```

2. **VERSION文件为空**
   ```
   ⚠️ VERSION文件内容为空
   ```

3. **权限问题**
   ```
   ❌ 生成zip包失败: [Errno 13] Permission denied
   ```

### 调试模式

使用 `--verbose` 参数可以获得详细的调试信息：

```bash
deepenc build --genzip --verbose
```

## 使用场景

### 开发环境

- 快速打包测试版本
- 方便团队成员共享构建结果

### 生产环境

- 自动化部署流程
- 版本管理和发布

### CI/CD 集成

```yaml
# GitHub Actions 示例
- name: Build and package
  run: |
    deepenc build --genzip
    echo "ZIP package generated"
```

## 注意事项

1. **VERSION文件要求**
   - 必须位于项目根目录
   - 不能为空
   - 建议使用语义化版本号

2. **目录结构**
   - 确保项目有正确的目录结构
   - 构建目录必须存在且包含文件

3. **密码安全**
   - 不要在代码中硬编码密码
   - 使用环境变量管理敏感信息

4. **文件大小**
   - 大型项目可能生成较大的zip包
   - 注意磁盘空间和传输时间

## 示例项目

参考 `example_project/` 目录中的示例，了解如何正确配置项目以使用此功能。

## 故障排除

### 问题：zip包生成失败

**解决方案：**
1. 检查项目根目录是否存在 `VERSION` 文件
2. 确认 `VERSION` 文件内容不为空
3. 验证构建目录权限
4. 使用 `--verbose` 参数查看详细错误信息

### 问题：zip包内容不完整

**解决方案：**
1. 确认构建过程成功完成
2. 检查构建目录是否包含预期文件
3. 验证文件权限设置

### 问题：密码设置无效

**解决方案：**
1. 确认环境变量设置正确
2. 检查环境变量名称拼写
3. 重启终端或重新加载环境配置
