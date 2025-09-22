# DeepEnc Python 项目加密分发框架 Makefile

.PHONY: help build clean install test check

# 默认目标
.DEFAULT_GOAL := help

# 项目配置
VERSION := 1.0.0
PYTHON := python3
PIP := pip3

help: ## 显示帮助信息
	@echo "DeepEnc Python 项目加密分发框架 - $(VERSION)"
	@echo ""
	@echo "可用命令:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## 构建加密项目
	@echo "🔨 构建加密项目..."
	$(PYTHON) -m deepenc build --verbose
	@echo "✅ 构建完成"


build-zip: ## 构建并生成ZIP包
	@echo "🔨 构建并生成ZIP包..."
	$(PYTHON) -m deepenc build --verbose --genzip
	@echo "✅ 构建和打包完成"


clean: ## 清理构建文件
	@echo "🧹 清理构建文件..."
	$(PYTHON) -m deepenc clean
	rm -rf build dist *.egg-info
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ 清理完成"


test: ## 运行测试
	@echo "🧪 运行测试..."
	$(PYTHON) -m deepenc status
	@echo "✅ 测试完成"

check: ## 检查系统状态
	@echo "🔍 检查系统状态..."
	$(PYTHON) -m deepenc status
	@echo "✅ 检查完成"

format: ## 格式化代码
	@echo "🎨 格式化代码..."
	@command -v black >/dev/null 2>&1 || { echo "请先安装: pip install black"; exit 1; }
	black --line-length 88 .
	@echo "✅ 代码格式化完成"

lint: ## 代码检查
	@echo "🔍 代码检查..."
	@command -v flake8 >/dev/null 2>&1 || { echo "请先安装: pip install flake8"; exit 1; }
	flake8 --max-line-length 88 --ignore E203,W503 .
	@echo "✅ 代码检查完成"


all: clean build test ## 完整构建流程
	@echo "🎉 完整构建流程完成"

version: ## 显示版本信息
	@echo "DeepEnc v$(VERSION)"
	@$(PYTHON) --version
	@$(PYTHON) -c "import deepenc; print(f'框架版本: {deepenc.__version__}')" 2>/dev/null || echo "框架未安装"