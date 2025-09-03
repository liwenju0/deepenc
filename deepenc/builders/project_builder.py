#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目构建器

实现自动化的项目构建和加密功能。
遵循 Linux 内核的构建系统设计理念。
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime
from ..discovery.scanner import FileScanner
from ..core.crypto import AESCrypto
from ..core.auth import AuthManager
from ..core.errors import BuildError


class ProjectBuilder:
    """项目构建器
    
    自动发现、加密和构建 Python 项目。
    """
    
    def __init__(self, project_root=None, build_dir=None):
        """初始化项目构建器
        
        Args:
            project_root: 项目根目录
            build_dir: 构建输出目录
        """
        self.project_root = Path(project_root or '.').resolve()
        self.build_dir = Path(build_dir or self.project_root / 'build').resolve()
        self.encrypted_dir = self.build_dir / 'encrypted'
        
        # 初始化组件
        self.scanner = FileScanner(self.project_root)
        self.crypto = AESCrypto()
        self.auth_manager = AuthManager()
        
        # 构建状态
        self.build_info = {
            'start_time': None,
            'end_time': None,
            'success': False,
            'errors': [],
            'encrypted_files': {}
        }
        
        print(f"🔨 项目构建器已初始化")
        print(f"📁 项目根目录: {self.project_root}")
        print(f"🏗️ 构建目录: {self.build_dir}")
    
    def build_project(self, auto_discover=True, clean=True):
        """构建加密项目
        
        Args:
            auto_discover: 是否自动发现文件
            clean: 是否清理构建目录
            
        Returns:
            dict: 构建结果信息
        """
        self.build_info['start_time'] = datetime.now()
        
        try:
            print("🚀 开始构建加密项目...")
            
            # 1. 准备构建环境
            if clean:
                self._prepare_build_environment()
            
            # 2. 发现文件
            if auto_discover:
                discovery_result = self.scanner.discover_all_files()
            else:
                discovery_result = self._load_manual_config()
            
            # 3. 加密 Python 文件
            python_result = self._encrypt_python_files(discovery_result['python_files'])
            
            # 4. 加密 ONNX 模型
            onnx_result = self._encrypt_onnx_files(discovery_result['onnx_files'])
            
            # 5. 生成配置文件
            config_result = self._generate_configuration(python_result, onnx_result)
            
            # 6. 生成启动脚本
            bootstrap_result = self._generate_bootstrap_script(config_result)
            
            # 7. 创建构建报告
            build_report = self._create_build_report(
                discovery_result, python_result, onnx_result, config_result
            )
            
            self.build_info['success'] = True
            self.build_info['end_time'] = datetime.now()
            
            print("✅ 项目构建成功！")
            self._print_build_summary(build_report)
            
            return build_report
            
        except Exception as e:
            self.build_info['errors'].append(str(e))
            self.build_info['end_time'] = datetime.now()
            raise BuildError(f"项目构建失败: {e}")
    
    def _prepare_build_environment(self):
        """准备构建环境"""
        try:
            print("🧹 准备构建环境...")
            
            # 清理构建目录
            if self.build_dir.exists():
                shutil.rmtree(self.build_dir)
            
            # 创建构建目录结构
            self.build_dir.mkdir(parents=True, exist_ok=True)
            self.encrypted_dir.mkdir(parents=True, exist_ok=True)
            
            # 创建子目录
            (self.encrypted_dir / 'python').mkdir(parents=True, exist_ok=True)
            (self.encrypted_dir / 'models').mkdir(parents=True, exist_ok=True)
            (self.build_dir / 'config').mkdir(parents=True, exist_ok=True)
            
            print("✅ 构建环境准备完成")
            
        except Exception as e:
            raise BuildError(f"准备构建环境失败: {e}")
    
    def _encrypt_python_files(self, python_files):
        """加密 Python 文件
        
        Args:
            python_files: Python 文件信息列表
            
        Returns:
            dict: 加密结果
        """
        try:
            print("🔐 加密 Python 文件...")
            
            encryption_key = self.auth_manager.get_key()
            encrypted_files = {}
            
            for file_info in python_files:
                source_path = file_info['file_path']
                relative_path = file_info['relative_path']
                module_name = file_info['module_name']
                
                # 生成加密文件路径
                encrypted_path = self.encrypted_dir / 'python' / f"{relative_path}.encrypted"
                
                # 确保目标目录存在
                encrypted_path.parent.mkdir(parents=True, exist_ok=True)
                
                # 加密文件
                self.crypto.encrypt_file(source_path, str(encrypted_path), encryption_key)
                
                encrypted_files[module_name] = {
                    'source': source_path,
                    'encrypted': str(encrypted_path),
                    'relative_encrypted': str(encrypted_path.relative_to(self.build_dir))
                }
                
                print(f"  ✅ {module_name}")
            
            print(f"🔐 Python 文件加密完成，共 {len(encrypted_files)} 个")
            return encrypted_files
            
        except Exception as e:
            raise BuildError(f"加密 Python 文件失败: {e}")
    
    def _encrypt_onnx_files(self, onnx_files):
        """加密 ONNX 文件
        
        Args:
            onnx_files: ONNX 文件信息列表
            
        Returns:
            dict: 加密结果
        """
        try:
            print("🧠 加密 ONNX 模型...")
            
            encryption_key = self.auth_manager.get_key()
            encrypted_files = {}
            
            for file_info in onnx_files:
                source_path = file_info['file_path']
                relative_path = file_info['relative_path']
                model_name = file_info['model_name']
                
                # 生成加密文件路径
                encrypted_path = self.encrypted_dir / 'models' / f"{relative_path}.encrypt"
                
                # 确保目标目录存在
                encrypted_path.parent.mkdir(parents=True, exist_ok=True)
                
                # 加密文件
                self.crypto.encrypt_file(source_path, str(encrypted_path), encryption_key)
                
                encrypted_files[model_name] = {
                    'source': source_path,
                    'encrypted': str(encrypted_path),
                    'relative_encrypted': str(encrypted_path.relative_to(self.build_dir))
                }
                
                print(f"  ✅ {model_name}")
            
            print(f"🧠 ONNX 模型加密完成，共 {len(encrypted_files)} 个")
            return encrypted_files
            
        except Exception as e:
            raise BuildError(f"加密 ONNX 文件失败: {e}")
    
    def _generate_configuration(self, python_result, onnx_result):
        """生成配置文件
        
        Args:
            python_result: Python 加密结果
            onnx_result: ONNX 加密结果
            
        Returns:
            dict: 配置信息
        """
        try:
            print("📝 生成配置文件...")
            
            # 生成模块映射配置
            module_mapping = {}
            for module_name, info in python_result.items():
                module_mapping[module_name] = info['relative_encrypted']
            
            # 生成模型映射配置
            model_mapping = {}
            for model_name, info in onnx_result.items():
                model_mapping[model_name] = info['relative_encrypted']
            
            # 配置数据
            config_data = {
                'version': '1.0.0',
                'build_time': datetime.now().isoformat(),
                'project_root': str(self.project_root),
                'auth_info': self.auth_manager.get_auth_info(),
                'module_mapping': module_mapping,
                'model_mapping': model_mapping,
                'statistics': {
                    'total_python_modules': len(python_result),
                    'total_onnx_models': len(onnx_result)
                }
            }
            
            # 保存配置文件
            config_path = self.build_dir / 'config' / 'encryption_config.json'
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            print(f"  ✅ 配置文件: {config_path}")
            
            return config_data
            
        except Exception as e:
            raise BuildError(f"生成配置文件失败: {e}")
    
    def _generate_bootstrap_script(self, config_data):
        """生成启动脚本
        
        Args:
            config_data: 配置数据
            
        Returns:
            str: 启动脚本路径
        """
        try:
            print("🚀 生成启动脚本...")
            
            # 生成启动脚本内容
            bootstrap_content = self._get_bootstrap_template(config_data)
            
            # 保存启动脚本
            bootstrap_path = self.build_dir / 'run.py'
            with open(bootstrap_path, 'w', encoding='utf-8') as f:
                f.write(bootstrap_content)
            
            # 设置可执行权限
            bootstrap_path.chmod(0o755)
            
            print(f"  ✅ 启动脚本: {bootstrap_path}")
            
            return str(bootstrap_path)
            
        except Exception as e:
            raise BuildError(f"生成启动脚本失败: {e}")
    
    def _get_bootstrap_template(self, config_data):
        """获取启动脚本模板
        
        Args:
            config_data: 配置数据
            
        Returns:
            str: 启动脚本内容
        """
        module_mappings = []
        for module_name, encrypted_path in config_data['module_mapping'].items():
            module_mappings.append(f'        "{module_name}": "{encrypted_path}",')
        
        return f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动生成的项目启动脚本

这个脚本会自动初始化加密系统，让您的项目透明地支持加密模块和模型。

生成时间: {config_data['build_time']}
项目根目录: {config_data['project_root']}
Python 模块数: {config_data['statistics']['total_python_modules']}
ONNX 模型数: {config_data['statistics']['total_onnx_models']}
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.resolve()
sys.path.insert(0, str(project_root))

def bootstrap_encryption_system():
    """启动加密系统"""
    try:
        # 导入加密框架
        from encrypt.bootstrap import initialize
        
        # 模块映射配置
        module_config = {{
{chr(10).join(module_mappings)}
        }}
        
        # 初始化加密系统
        system = initialize(module_config)
        
        print("✅ 加密系统启动成功")
        print(f"🔐 已注册 {len(module_config)} 个加密模块")
        print(f"🧠 ONNX 模型自动解密已启用")
        
        return system
        
    except Exception as e:
        print(f"❌ 加密系统启动失败: {{e}}")
        print("💡 提示: 确保环境变量 ENCRYPTION_KEY 或许可证文件存在")
        raise

def main():
    """主函数"""
    print("🚀 启动加密项目...")
    
    # 启动加密系统
    system = bootstrap_encryption_system()
    
    # 尝试导入主模块
    try:
        # 这里可以根据项目结构自动检测主模块
        possible_main_modules = ['src.main', 'main', 'app', 'server']
        
        for main_module in possible_main_modules:
            try:
                module = __import__(main_module, fromlist=[''])
                if hasattr(module, 'main') or hasattr(module, 'run'):
                    print(f"🎯 找到主模块: {{main_module}}")
                    
                    # 尝试运行主函数
                    if hasattr(module, 'main'):
                        module.main()
                    elif hasattr(module, 'run'):
                        module.run()
                    
                    return
            except ImportError:
                continue
        
        print("⚠️ 未找到主模块，系统已就绪")
        print("💡 您可以手动导入需要的模块:")
        for module_name in module_config.keys():
            print(f"   import {{module_name}}")
        
    except Exception as e:
        print(f"❌ 运行主模块失败: {{e}}")

if __name__ == "__main__":
    main()
'''
    
    def _create_build_report(self, discovery_result, python_result, onnx_result, config_result):
        """创建构建报告
        
        Args:
            discovery_result: 文件发现结果
            python_result: Python 加密结果
            onnx_result: ONNX 加密结果
            config_result: 配置生成结果
            
        Returns:
            dict: 构建报告
        """
        build_duration = (
            self.build_info['end_time'] - self.build_info['start_time']
        ).total_seconds()
        
        return {
            'build_info': {
                'success': self.build_info['success'],
                'start_time': self.build_info['start_time'].isoformat(),
                'end_time': self.build_info['end_time'].isoformat(),
                'duration_seconds': build_duration,
                'errors': self.build_info['errors']
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
                'encrypted_dir': str(self.encrypted_dir),
                'config_file': str(self.build_dir / 'config' / 'encryption_config.json'),
                'bootstrap_script': str(self.build_dir / 'run.py')
            },
            'auth_info': config_result['auth_info']
        }
    
    def _print_build_summary(self, build_report):
        """打印构建摘要
        
        Args:
            build_report: 构建报告
        """
        print("\n📊 构建摘要:")
        print(f"  ⏱️  构建时间: {build_report['build_info']['duration_seconds']:.2f} 秒")
        print(f"  🐍 Python 模块: {build_report['encryption']['encrypted_python_modules']} 个")
        print(f"  🧠 ONNX 模型: {build_report['encryption']['encrypted_onnx_models']} 个")
        print(f"  📁 构建目录: {build_report['output']['build_dir']}")
        print(f"  🚀 启动脚本: {build_report['output']['bootstrap_script']}")
        print(f"  🔐 授权模式: {build_report['auth_info']['auth_mode']}")
        print(f"  🔑 密钥来源: {build_report['auth_info']['key_source']}")
        
        print("\n🎯 使用方法:")
        print(f"  cd {build_report['output']['build_dir']}")
        print("  python run.py")
    
    def _load_manual_config(self):
        """加载手动配置
        
        Returns:
            dict: 配置数据
        """
        # 这里可以实现从配置文件加载的逻辑
        # 暂时使用自动发现作为回退
        return self.scanner.discover_all_files()
    
    def clean_build(self):
        """清理构建目录"""
        try:
            if self.build_dir.exists():
                shutil.rmtree(self.build_dir)
                print(f"🧹 已清理构建目录: {self.build_dir}")
            else:
                print("🧹 构建目录不存在，无需清理")
                
        except Exception as e:
            raise BuildError(f"清理构建目录失败: {e}")
    
    def get_build_info(self):
        """获取构建信息
        
        Returns:
            dict: 构建信息
        """
        return self.build_info.copy()
    
    def verify_build(self):
        """验证构建结果
        
        Returns:
            bool: 构建是否有效
        """
        try:
            # 检查构建目录
            if not self.build_dir.exists():
                return False
            
            # 检查关键文件
            required_files = [
                self.build_dir / 'run.py',
                self.build_dir / 'config' / 'encryption_config.json'
            ]
            
            for required_file in required_files:
                if not required_file.exists():
                    print(f"❌ 缺少关键文件: {required_file}")
                    return False
            
            # 检查加密目录
            if not self.encrypted_dir.exists():
                print(f"❌ 加密目录不存在: {self.encrypted_dir}")
                return False
            
            print("✅ 构建验证通过")
            return True
            
        except Exception as e:
            print(f"❌ 构建验证失败: {e}")
            return False
