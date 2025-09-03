# Python 项目加密分发框架 Makefile
# 遵循 Linux 项目的标准 Makefile 风格

.PHONY: help build test clean install uninstall check format lint docs

# 默认目标
.DEFAULT_GOAL := help

# 项目配置
PROJECT_NAME := encrypt
VERSION := 1.0.0
PYTHON := python3
PIP := pip3

# 目录配置
BUILD_DIR := build
DIST_DIR := dist
DOCS_DIR := docs

help: ## 显示帮助信息
	@echo "Python 项目加密分发框架 - $(VERSION)"
	@echo ""
	@echo "可用命令:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## 构建加密项目
	@echo "🔨 构建加密项目..."
	$(PYTHON) -m encrypt build --verbose
	@echo "✅ 构建完成"

test: ## 运行测试
	@echo "🧪 运行测试..."
	$(PYTHON) test_framework.py
	@echo "✅ 测试完成"

clean: ## 清理构建文件
	@echo "🧹 清理构建文件..."
	$(PYTHON) -m encrypt clean
	rm -rf $(BUILD_DIR) $(DIST_DIR)
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ 清理完成"

install: ## 安装依赖
	@echo "📦 安装依赖..."
	$(PIP) install pycrypto onnxruntime
	@echo "✅ 依赖安装完成"

check: ## 检查系统状态
	@echo "🔍 检查系统状态..."
	$(PYTHON) -m encrypt status
	@echo "✅ 检查完成"

format: ## 格式化代码
	@echo "🎨 格式化代码..."
	@command -v black >/dev/null 2>&1 || { echo "请安装 black: pip install black"; exit 1; }
	black --line-length 88 .
	@echo "✅ 代码格式化完成"

lint: ## 代码检查
	@echo "🔍 代码检查..."
	@command -v flake8 >/dev/null 2>&1 || { echo "请安装 flake8: pip install flake8"; exit 1; }
	flake8 --max-line-length 88 --ignore E203,W503 .
	@echo "✅ 代码检查完成"

docs: ## 生成文档
	@echo "📚 生成文档..."
	@echo "文档已存在于 docs/ 目录"
	@echo "✅ 文档生成完成"

example: ## 运行示例
	@echo "🎯 运行示例..."
	$(PYTHON) examples/basic_usage.py
	@echo ""
	$(PYTHON) examples/advanced_usage.py
	@echo "✅ 示例运行完成"

verify: ## 验证安装
	@echo "🔍 验证安装..."
	@$(PYTHON) -c "import encrypt; print(f'框架版本: {encrypt.__version__}')"
	@$(PYTHON) -c "from encrypt.core import AESCrypto, AuthManager; print('✅ 核心组件正常')"
	@echo "✅ 验证完成"

package: build ## 打包分发
	@echo "📦 打包分发..."
	mkdir -p $(DIST_DIR)
	cd $(BUILD_DIR) && tar -czf ../$(DIST_DIR)/$(PROJECT_NAME)-$(VERSION).tar.gz .
	@echo "✅ 打包完成: $(DIST_DIR)/$(PROJECT_NAME)-$(VERSION).tar.gz"

# 设置开发环境
dev-setup:
	@echo "🔧 设置开发环境..."
	@echo "📝 创建许可证文件..."
	@mkdir -p /data/appdatas/inference
	@echo "dev-key-16chars" > /data/appdatas/inference/license.dat
	@echo "export AUTH_MODE=DEV" >> ~/.bashrc
	@echo "✅ 开发环境设置完成"
	@echo "📋 许可证文件: /data/appdatas/inference/license.dat"
	@echo "🔑 开发模式: AUTH_MODE=DEV"

# 设置生产环境
prod-setup:
	@echo "🔐 设置生产环境..."
	@echo "⚠️  请确保硬件授权库可用"
	@echo "export AUTH_MODE=PROD" >> ~/.bashrc
	@echo "✅ 生产环境设置完成"
	@echo "🔑 生产模式: AUTH_MODE=PROD"

# 测试构建
test-build:
	@echo "🧪 测试项目构建..."
	@echo "📝 检查许可证文件..."
	@test -f "/data/appdatas/inference/license.dat" || { echo "❌ 请先运行 'make dev-setup' 创建许可证文件"; exit 1; }
	@echo "✅ 许可证文件检查通过"
	@python -m deepenc build --verbose

benchmark: ## 性能基准测试
	@echo "⚡ 运行性能基准测试..."
	$(PYTHON) -c "
import time
import os
os.environ['ENCRYPTION_KEY'] = '1234567890123456'
from core.crypto import AESCrypto
from core.auth import AuthManager

crypto = AESCrypto()
auth = AuthManager()
key = auth.get_key()

# 测试不同大小的文件
sizes = [1024, 10240, 102400, 1024000]
for size in sizes:
    data = os.urandom(size)
    start = time.time()
    encrypted = crypto.encrypt(data, key)
    encrypt_time = time.time() - start
    
    start = time.time()
    decrypted = crypto.decrypt(encrypted, key)
    decrypt_time = time.time() - start
    
    print(f'{size//1024:>6}KB: 加密 {encrypt_time*1000:>6.2f}ms, 解密 {decrypt_time*1000:>6.2f}ms')
"
	@echo "✅ 基准测试完成"

all: clean install build test verify ## 完整构建流程
	@echo "🎉 完整构建流程完成"

# 调试目标
debug: ## 调试模式运行
	@echo "🐛 调试模式..."
	ENCRYPT_DEBUG=1 $(PYTHON) test_framework.py

# 生产构建
prod-build: ## 生产环境构建
	@echo "🏭 生产环境构建..."
	@test -n "$(ENCRYPTION_KEY)" || { echo "❌ 请设置 ENCRYPTION_KEY 环境变量"; exit 1; }
	AUTH_MODE=PROD $(PYTHON) -m encrypt build
	@echo "✅ 生产构建完成"

# 显示版本信息
version: ## 显示版本信息
	@echo "$(PROJECT_NAME) v$(VERSION)"
	@$(PYTHON) --version
	@$(PYTHON) -c "import encrypt; print(f'框架版本: {encrypt.__version__}')"
