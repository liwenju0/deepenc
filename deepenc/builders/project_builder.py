#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目构建器 - 遵循 Linux 内核设计理念

核心设计原则:
1. 单一职责: 每个类只负责一个特定功能
2. 模块化: 功能分解为独立的、可测试的组件
3. 错误处理: 明确的错误类型和恢复策略
4. 配置驱动: 最小化硬编码，支持灵活配置
5. 可观测性: 详细的日志和状态跟踪

架构说明:
- ProjectBuilder: 主协调器，负责流程编排
- BuildEnvironment: 构建环境管理
- FileProcessor: 文件处理抽象基类
- PythonProcessor: Python文件加密处理器
- ONNXProcessor: ONNX模型加密处理器
- ConfigGenerator: 配置文件生成器
"""

import os
import shutil
import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from ..discovery.scanner import FileScanner
from ..core.crypto import AESCrypto
from ..core.auth import AuthManager
from ..core.errors import BuildError


# 构建系统常量 - 避免魔法数字和字符串
class BuildConstants:
    """构建系统常量定义"""
    
    # 目录结构
    BUILD_DIR_NAME = 'build'
    ENCRYPTED_DIR_NAME = 'encrypted'
    PYTHON_SUBDIR = 'python'
    MODELS_SUBDIR = 'models'
    CONFIG_SUBDIR = 'config'
    
    # 文件扩展名
    PYTHON_ENCRYPTED_EXT = '.encrypted'
    ONNX_ENCRYPTED_EXT = '.encrypt'
    
    # 配置版本
    CONFIG_VERSION = '1.0.0'
    
    # 配置文件
    CONFIG_FILE_NAME = 'encryption_config.json'
    
    # 排除的文件模式 - 确保关键文件不被加密
    EXCLUDED_PATTERNS = [
        'src/grpc_main.py',  # gRPC主服务文件，不加密
        '*.pyc',             # Python字节码文件
        '__pycache__',       # Python缓存目录
        '.git',              # Git版本控制目录
        'build',             # 构建输出目录
        'dist',              # 分发目录
        '*.egg-info'         # Python包信息
    ]


@dataclass
class BuildResult:
    """构建结果数据类"""
    success: bool
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    errors: List[str] = None
    encrypted_files: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.encrypted_files is None:
            self.encrypted_files = {}


class BuildEnvironment:
    """构建环境管理器
    
    职责: 管理构建目录的创建、清理和验证
    设计理念: 单一职责，清晰的接口，可测试性
    """
    
    def __init__(self, project_root: Path, build_dir: Path):
        self.project_root = project_root
        self.build_dir = build_dir
        self.encrypted_dir = build_dir / BuildConstants.ENCRYPTED_DIR_NAME
        
        # 设置日志
        self.logger = logging.getLogger(__name__)
    
    def prepare(self, clean: bool = True) -> None:
        """准备构建环境
        
        Args:
            clean: 是否清理现有构建目录
            
        Raises:
            BuildError: 环境准备失败时抛出
        """
        try:
            self.logger.info("准备构建环境...")
            
            if clean:
                self._clean_build_directory()
            
            self._create_directory_structure()
            self.logger.info("构建环境准备完成")
            
        except Exception as e:
            raise BuildError(f"准备构建环境失败: {e}")
    
    def _clean_build_directory(self) -> None:
        """清理构建目录"""
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
            self.logger.debug(f"已清理构建目录: {self.build_dir}")
    
    def _create_directory_structure(self) -> None:
        """创建目录结构"""
        # 主构建目录
        self.build_dir.mkdir(parents=True, exist_ok=True)
        
        # 加密文件目录
        self.encrypted_dir.mkdir(parents=True, exist_ok=True)
        
        # 子目录
        (self.encrypted_dir / BuildConstants.PYTHON_SUBDIR).mkdir(parents=True, exist_ok=True)
        (self.encrypted_dir / BuildConstants.MODELS_SUBDIR).mkdir(parents=True, exist_ok=True)
        (self.build_dir / BuildConstants.CONFIG_SUBDIR).mkdir(parents=True, exist_ok=True)
    
    def verify(self) -> bool:
        """验证构建环境
        
        Returns:
            bool: 环境是否有效
        """
        required_dirs = [
            self.build_dir,
            self.encrypted_dir,
            self.encrypted_dir / BuildConstants.PYTHON_SUBDIR,
            self.encrypted_dir / BuildConstants.MODELS_SUBDIR,
            self.build_dir / BuildConstants.CONFIG_SUBDIR
        ]
        
        return all(d.exists() for d in required_dirs)


class FileProcessor(ABC):
    """文件处理器抽象基类
    
    设计理念: 策略模式，支持不同类型的文件处理
    遵循开闭原则: 新增文件类型只需继承此类
    """
    
    def __init__(self, encrypted_dir: Path, crypto: AESCrypto, auth_manager: AuthManager):
        self.encrypted_dir = encrypted_dir
        self.crypto = crypto
        self.auth_manager = auth_manager
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def process_files(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """处理文件列表
        
        Args:
            files: 文件信息列表
            
        Returns:
            Dict[str, Any]: 处理结果
        """
        pass
    
    @abstractmethod
    def _get_encrypted_path(self, file_info: Dict[str, Any]) -> Path:
        """获取加密文件路径
        
        Args:
            file_info: 文件信息
            
        Returns:
            Path: 加密文件路径
        """
        pass


class PythonProcessor(FileProcessor):
    """Python文件处理器
    
    职责: 专门处理Python文件的加密
    设计: 继承FileProcessor，实现具体策略
    """
    
    def process_files(self, python_files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """加密Python文件
        
        Args:
            python_files: Python文件信息列表
            
        Returns:
            Dict[str, Any]: 加密结果
            
        Raises:
            BuildError: 加密失败时抛出
        """
        try:
            self.logger.info("开始加密Python文件...")
            
            encryption_key = self.auth_manager.get_key()
            encrypted_files = {}
            
            for file_info in python_files:
                result = self._encrypt_single_file(file_info, encryption_key)
                encrypted_files[file_info['module_name']] = result
                self.logger.debug(f"已加密: {file_info['module_name']}")
            
            self.logger.info(f"Python文件加密完成，共 {len(encrypted_files)} 个")
            return encrypted_files
            
        except Exception as e:
            raise BuildError(f"加密Python文件失败: {e}")
    
    def _encrypt_single_file(self, file_info: Dict[str, Any], key: str) -> Dict[str, Any]:
        """加密单个Python文件
        
        Args:
            file_info: 文件信息
            key: 加密密钥
            
        Returns:
            Dict[str, Any]: 加密结果信息
        """
        source_path = file_info['file_path']
        relative_path = file_info['relative_path']
        module_name = file_info['module_name']
        
        # 生成加密文件路径
        encrypted_path = self._get_encrypted_path(file_info)
        encrypted_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 执行加密
        self.crypto.encrypt_file(source_path, str(encrypted_path), key)
        
        return {
            'source': source_path,
            'encrypted': str(encrypted_path),
            'relative_encrypted': str(encrypted_path.relative_to(self.encrypted_dir.parent))
        }
    
    def _get_encrypted_path(self, file_info: Dict[str, Any]) -> Path:
        """获取Python文件加密路径"""
        relative_path = file_info['relative_path']
        return self.encrypted_dir / BuildConstants.PYTHON_SUBDIR / f"{relative_path}{BuildConstants.PYTHON_ENCRYPTED_EXT}"


class ONNXProcessor(FileProcessor):
    """ONNX模型处理器
    
    职责: 专门处理ONNX模型的加密
    设计: 与PythonProcessor保持一致的接口
    """
    
    def process_files(self, onnx_files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """加密ONNX模型文件
        
        Args:
            onnx_files: ONNX文件信息列表
            
        Returns:
            Dict[str, Any]: 加密结果
            
        Raises:
            BuildError: 加密失败时抛出
        """
        try:
            self.logger.info("开始加密ONNX模型...")
            
            encryption_key = self.auth_manager.get_key()
            encrypted_files = {}
            
            for file_info in onnx_files:
                result = self._encrypt_single_file(file_info, encryption_key)
                encrypted_files[file_info['model_name']] = result
                self.logger.debug(f"已加密: {file_info['model_name']}")
            
            self.logger.info(f"ONNX模型加密完成，共 {len(encrypted_files)} 个")
            return encrypted_files
            
        except Exception as e:
            raise BuildError(f"加密ONNX文件失败: {e}")
    
    def _encrypt_single_file(self, file_info: Dict[str, Any], key: str) -> Dict[str, Any]:
        """加密单个ONNX文件"""
        source_path = file_info['file_path']
        relative_path = file_info['relative_path']
        model_name = file_info['model_name']
        
        # 生成加密文件路径
        encrypted_path = self._get_encrypted_path(file_info)
        encrypted_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 执行加密
        self.crypto.encrypt_file(source_path, str(encrypted_path), key)
        
        return {
            'source': source_path,
            'encrypted': str(encrypted_path),
            'relative_encrypted': str(encrypted_path.relative_to(self.encrypted_dir.parent))
        }
    
    def _get_encrypted_path(self, file_info: Dict[str, Any]) -> Path:
        """获取ONNX文件加密路径"""
        relative_path = file_info['relative_path']
        return self.encrypted_dir / BuildConstants.MODELS_SUBDIR / f"{relative_path}{BuildConstants.ONNX_ENCRYPTED_EXT}"


class ConfigGenerator:
    """配置文件生成器
    
    职责: 生成项目配置和映射文件
    设计: 数据驱动，支持配置模板
    """
    
    def __init__(self, build_dir: Path, auth_manager: AuthManager):
        self.build_dir = build_dir
        self.auth_manager = auth_manager
        self.logger = logging.getLogger(__name__)
    
    def generate(self, python_result: Dict[str, Any], onnx_result: Dict[str, Any]) -> Dict[str, Any]:
        """生成配置文件
        
        Args:
            python_result: Python加密结果
            onnx_result: ONNX加密结果
            
        Returns:
            Dict[str, Any]: 配置数据
            
        Raises:
            BuildError: 配置生成失败时抛出
        """
        try:
            self.logger.info("生成配置文件...")
            
            config_data = self._build_config_data(python_result, onnx_result)
            self._save_config_file(config_data)
            
            self.logger.info("配置文件生成完成")
            return config_data
            
        except Exception as e:
            raise BuildError(f"生成配置文件失败: {e}")
    
    def _build_config_data(self, python_result: Dict[str, Any], onnx_result: Dict[str, Any]) -> Dict[str, Any]:
        """构建配置数据"""
        # 模块映射配置
        module_mapping = {
            module_name: info['relative_encrypted']
            for module_name, info in python_result.items()
        }
        
        # 模型映射配置
        model_mapping = {
            model_name: info['relative_encrypted']
            for model_name, info in onnx_result.items()
        }
        
        return {
            'version': BuildConstants.CONFIG_VERSION,
            'build_time': datetime.now().isoformat(),
            'auth_info': self.auth_manager.get_auth_info(),
            'module_mapping': module_mapping,
            'model_mapping': model_mapping,
            'statistics': {
                'total_python_modules': len(python_result),
                'total_onnx_models': len(onnx_result)
            }
        }
    
    def _save_config_file(self, config_data: Dict[str, Any]) -> None:
        """保存配置文件到磁盘"""
        config_path = self.build_dir / BuildConstants.CONFIG_SUBDIR / BuildConstants.CONFIG_FILE_NAME
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        
        self.logger.debug(f"配置文件已保存: {config_path}")





class ProjectBuilder:
    """项目构建器 - 主协调器
    
    设计理念:
    1. 组合优于继承: 使用组合模式整合各个组件
    2. 单一职责: 只负责流程编排，具体工作委托给专门组件
    3. 依赖注入: 通过构造函数注入依赖，便于测试和扩展
    4. 错误恢复: 每个步骤都有明确的错误处理策略
    
    架构说明:
    - 主协调器: 负责构建流程的编排
    - 组件管理: 管理各个功能组件的生命周期
    - 状态跟踪: 维护构建状态和结果
    - 错误处理: 统一的错误处理和恢复策略
    """
    
    def __init__(self, project_root=None, build_dir=None, entry_point=None):
        """初始化项目构建器
        
        Args:
            project_root: 项目根目录
            build_dir: 构建输出目录
            entry_point: 项目入口点文件（可选）
        """
        # 路径设置
        self.project_root = Path(project_root or '.').resolve()
        self.build_dir = Path(build_dir or self.project_root / BuildConstants.BUILD_DIR_NAME).resolve()
        self.entry_point = Path(entry_point).resolve() if entry_point else None
        
        # 初始化核心组件
        self.scanner = FileScanner(self.project_root)
        self.crypto = AESCrypto()
        self.auth_manager = AuthManager()
        
        # 初始化功能组件
        self.build_env = BuildEnvironment(self.project_root, self.build_dir)
        self.python_processor = PythonProcessor(
            self.build_env.encrypted_dir, self.crypto, self.auth_manager
        )
        self.onnx_processor = ONNXProcessor(
            self.build_env.encrypted_dir, self.crypto, self.auth_manager
        )
        self.config_generator = ConfigGenerator(self.build_dir, self.auth_manager)
        
        # 构建状态跟踪
        self.build_result = BuildResult(
            success=False,
            start_time=datetime.now()
        )
        
        # 设置日志
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
        
        self.logger.info("项目构建器初始化完成")
        self.logger.info(f"项目根目录: {self.project_root}")
        self.logger.info(f"构建目录: {self.build_dir}")
        if self.entry_point:
            self.logger.info(f"项目入口点: {self.entry_point}")
    
    def _setup_logging(self):
        """设置日志配置"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def build_project(self, auto_discover=True, clean=True) -> Dict[str, Any]:
        """构建加密项目
        
        构建流程:
        1. 环境准备: 清理和创建构建目录
        2. 文件发现: 自动发现或加载手动配置（排除关键文件）
        3. 文件加密: 并行处理Python和ONNX文件
        4. 配置生成: 生成配置文件和映射
        5. 结果验证: 验证构建结果的完整性
        
        Args:
            auto_discover: 是否自动发现文件
            clean: 是否清理构建目录
            
        Returns:
            Dict[str, Any]: 构建结果信息
            
        Raises:
            BuildError: 构建失败时抛出
        """
        try:
            self.logger.info("开始构建加密项目...")
            
            # 步骤1: 准备构建环境
            self.build_env.prepare(clean=clean)
            
            # 步骤2: 发现文件（自动排除关键文件）
            discovery_result = self._discover_files(auto_discover)
            
            # 步骤3: 加密文件
            python_result = self.python_processor.process_files(discovery_result['python_files'])
            onnx_result = self.onnx_processor.process_files(discovery_result['onnx_files'])
            
            # 步骤4: 生成配置
            config_result = self.config_generator.generate(python_result, onnx_result)
            
            # 步骤5: 创建构建报告
            build_report = self._create_build_report(
                discovery_result, python_result, onnx_result, config_result
            )
            
            # 更新构建状态
            self.build_result.success = True
            self.build_result.end_time = datetime.now()
            self.build_result.duration_seconds = (
                self.build_result.end_time - self.build_result.start_time
            ).total_seconds()
            
            self.logger.info("项目构建成功完成")
            self._print_build_summary(build_report)
            
            return build_report
            
        except Exception as e:
            self.build_result.errors.append(str(e))
            self.build_result.end_time = datetime.now()
            self.logger.error(f"项目构建失败: {e}")
            raise BuildError(f"项目构建失败: {e}")
    
    def _discover_files(self, auto_discover: bool) -> Dict[str, Any]:
        """发现项目文件
        
        Args:
            auto_discover: 是否自动发现
            
        Returns:
            Dict[str, Any]: 文件发现结果
        """
        if auto_discover:
            discovery_result = self.scanner.discover_all_files()
            # 过滤掉不应该加密的文件
            discovery_result = self._filter_excluded_files(discovery_result)
            return discovery_result
        else:
            return self._load_manual_config()
    
    def _filter_excluded_files(self, discovery_result: Dict[str, Any]) -> Dict[str, Any]:
        """过滤掉不应该加密的文件
        
        Args:
            discovery_result: 原始发现结果
            
        Returns:
            Dict[str, Any]: 过滤后的结果
        """
        # 过滤Python文件
        filtered_python_files = []
        for file_info in discovery_result['python_files']:
            file_path = str(file_info['file_path'])
            if not self._should_exclude_file(file_path):
                filtered_python_files.append(file_info)
            else:
                self.logger.info(f"排除文件（不加密）: {file_path}")
        
        # 过滤ONNX文件
        filtered_onnx_files = []
        for file_info in discovery_result['onnx_files']:
            file_path = str(file_info['file_path'])
            if not self._should_exclude_file(file_path):
                filtered_onnx_files.append(file_info)
            else:
                self.logger.info(f"排除文件（不加密）: {file_path}")
        
        return {
            'python_files': filtered_python_files,
            'onnx_files': filtered_onnx_files,
            'project_root': discovery_result['project_root']
        }
    
    def _should_exclude_file(self, file_path: str) -> bool:
        """判断文件是否应该被排除
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否应该排除
        """
        # 检查是否匹配排除模式
        for pattern in BuildConstants.EXCLUDED_PATTERNS:
            if pattern in file_path:
                return True
        
        # 特别检查grpc_main.py
        if 'grpc_main.py' in file_path:
            return True
        
        # 检查是否为指定的入口点文件
        if self.entry_point and str(self.entry_point) in file_path:
            self.logger.info(f"排除入口点文件（不加密）: {file_path}")
            return True
        
        return False
    
    def _load_manual_config(self) -> Dict[str, Any]:
        """加载手动配置文件
        
        Returns:
            Dict[str, Any]: 配置数据
        """
        # TODO: 实现从配置文件加载的逻辑
        # 暂时使用自动发现作为回退
        self.logger.warning("手动配置加载未实现，回退到自动发现")
        return self.scanner.discover_all_files()
    
    def _create_build_report(self, discovery_result: Dict[str, Any], 
                           python_result: Dict[str, Any], 
                           onnx_result: Dict[str, Any], 
                           config_result: Dict[str, Any]) -> Dict[str, Any]:
        """创建构建报告
        
        Args:
            discovery_result: 文件发现结果
            python_result: Python加密结果
            onnx_result: ONNX加密结果
            config_result: 配置生成结果
            
        Returns:
            Dict[str, Any]: 构建报告
        """
        return {
            'build_info': {
                'success': self.build_result.success,
                'start_time': self.build_result.start_time.isoformat(),
                'end_time': self.build_result.end_time.isoformat() if self.build_result.end_time else None,
                'duration_seconds': self.build_result.duration_seconds,
                'errors': self.build_result.errors
            },
            'discovery': {
                'total_python_files': len(discovery_result['python_files']),
                'total_onnx_files': len(discovery_result['onnx_files']),
                'project_root': discovery_result['project_root']
            },
            'encryption': {
                'encrypted_python_modules': len(python_result),
                'encrypted_onnx_models': len(onnx_result),
                'python_modules': list(python_result.keys()),
                'onnx_models': list(onnx_result.keys())
            },
            'output': {
                'build_dir': str(self.build_dir),
                'encrypted_dir': str(self.build_env.encrypted_dir),
                'config_file': str(self.build_dir / BuildConstants.CONFIG_SUBDIR / BuildConstants.CONFIG_FILE_NAME)
            },
            'auth_info': config_result['auth_info']
        }
    
    def _print_build_summary(self, build_report: Dict[str, Any]) -> None:
        """打印构建摘要
        
        Args:
            build_report: 构建报告
        """
        print("\n📊 构建摘要:")
        duration = build_report['build_info']['duration_seconds']
        if duration is not None:
            print(f"  ⏱️  构建时间: {duration:.2f} 秒")
        else:
            print("  ⏱️  构建时间: 未知")
        print(f"  🐍 Python 模块: {build_report['encryption']['encrypted_python_modules']} 个")
        print(f"  🧠 ONNX 模型: {build_report['encryption']['encrypted_onnx_models']} 个")
        print(f"  📁 构建目录: {build_report['output']['build_dir']}")
        print(f"  🔐 授权模式: {build_report['auth_info']['auth_mode']}")
        print(f"  🔑 密钥来源: {build_report['auth_info']['key_source']}")
        
        print("\n🎯 重要说明:")
        print("  ✅ src/grpc_main.py 已被排除，不会被加密")
        print("  📝 启动方式由用户自行决定")
        print("  🔧 可参考配置文件了解模块映射关系")
    
    def clean_build(self) -> None:
        """清理构建目录
        
        Raises:
            BuildError: 清理失败时抛出
        """
        try:
            if self.build_dir.exists():
                shutil.rmtree(self.build_dir)
                self.logger.info(f"已清理构建目录: {self.build_dir}")
            else:
                self.logger.info("构建目录不存在，无需清理")
                
        except Exception as e:
            raise BuildError(f"清理构建目录失败: {e}")
    
    def get_build_info(self) -> Dict[str, Any]:
        """获取构建信息
        
        Returns:
            Dict[str, Any]: 构建信息
        """
        return {
            'success': self.build_result.success,
            'start_time': self.build_result.start_time.isoformat(),
            'end_time': self.build_result.end_time.isoformat() if self.build_result.end_time else None,
            'duration_seconds': self.build_result.duration_seconds,
            'errors': self.build_result.errors.copy()
        }
    
    def verify_build(self) -> bool:
        """验证构建结果
        
        Returns:
            bool: 构建是否有效
        """
        try:
            # 检查构建环境
            if not self.build_env.verify():
                self.logger.error("构建环境验证失败")
                return False
            
            # 检查关键文件
            required_files = [
                self.build_dir / BuildConstants.CONFIG_SUBDIR / BuildConstants.CONFIG_FILE_NAME
            ]
            
            for required_file in required_files:
                if not required_file.exists():
                    self.logger.error(f"缺少关键文件: {required_file}")
                    return False
            
            self.logger.info("构建验证通过")
            return True
            
        except Exception as e:
            self.logger.error(f"构建验证失败: {e}")
            return False
