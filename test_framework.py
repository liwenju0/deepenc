#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
框架测试脚本

测试加密分发框架的核心功能。
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# 添加框架路径
sys.path.insert(0, str(Path(__file__).parent))

def test_basic_encryption():
    """测试基本加密功能"""
    print("🔐 测试基本加密功能...")
    
    try:
        from core.crypto import AESCrypto
        from core.auth import AuthManager
        
        # 初始化组件
        crypto = AESCrypto()
        auth = AuthManager()
        
        # 获取密钥
        key = auth.get_key()
        print(f"  密钥长度: {len(key)}")
        
        # 测试数据加密/解密
        test_data = b"Hello, Encrypted World! This is a test message."
        encrypted = crypto.encrypt(test_data, key)
        decrypted = crypto.decrypt(encrypted, key)
        
        assert test_data == decrypted
        print("  ✅ 数据加密/解密测试通过")
        
        # 测试文件加密/解密
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as tmp_file:
            tmp_file.write("print('Hello from encrypted module!')")
            tmp_file_path = tmp_file.name
        
        encrypted_file_path = tmp_file_path + '.encrypted'
        
        try:
            crypto.encrypt_file(tmp_file_path, encrypted_file_path, key)
            decrypted_content = crypto.decrypt_file(encrypted_file_path, key)
            
            with open(tmp_file_path, 'rb') as f:
                original_content = f.read()
            
            assert original_content == decrypted_content
            print("  ✅ 文件加密/解密测试通过")
            
        finally:
            # 清理临时文件
            for file_path in [tmp_file_path, encrypted_file_path]:
                if os.path.exists(file_path):
                    os.remove(file_path)
        
        return True
        
    except Exception as e:
        print(f"  ❌ 基本加密测试失败: {e}")
        return False


def test_file_discovery():
    """测试文件发现功能"""
    print("🔍 测试文件发现功能...")
    
    try:
        from discovery.scanner import FileScanner
        
        # 创建临时项目结构
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # 创建测试文件 - 使用更合理的项目结构
            (temp_path / 'src').mkdir()
            (temp_path / 'src' / 'main.py').write_text("# Main module")
            (temp_path / 'src' / 'utils.py').write_text("# Utils module")
            
            (temp_path / 'assets').mkdir()
            (temp_path / 'assets' / 'test.onnx').write_bytes(b"fake onnx data")
            
            # 测试文件发现
            scanner = FileScanner(temp_path)
            result = scanner.discover_all_files()
            
            # 验证结果
            python_files = result['python_files']
            onnx_files = result['onnx_files']
            
            # 应该发现 src 下的文件
            python_modules = [f['module_name'] for f in python_files]
            assert 'src.main' in python_modules
            assert 'src.utils' in python_modules
            
            # 应该发现 ONNX 文件
            onnx_models = [f['model_name'] for f in onnx_files]
            assert 'test' in onnx_models or 'assets.test' in onnx_models
            
            print(f"  ✅ 发现 Python 文件: {len(python_files)} 个")
            print(f"  ✅ 发现 ONNX 文件: {len(onnx_files)} 个")
            
        return True
        
    except Exception as e:
        print(f"  ❌ 文件发现测试失败: {e}")
        return False


def test_module_loading():
    """测试模块加载功能"""
    print("📦 测试模块加载功能...")
    
    try:
        from loaders.module_loader import SmartModuleLoader
        from core.crypto import AESCrypto
        from core.auth import AuthManager
        
        # 设置测试环境
        os.environ['ENCRYPTION_KEY'] = '1234567890123456'
        
        # 创建临时模块
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # 创建测试模块
            test_module_content = '''
def test_function():
    return "Hello from encrypted module!"

TEST_CONSTANT = "This is a test constant"
'''
            
            module_file = temp_path / 'test_module.py'
            module_file.write_text(test_module_content)
            
            # 加密模块
            crypto = AESCrypto()
            auth = AuthManager()
            key = auth.get_key()
            
            encrypted_file = temp_path / 'test_module.py.encrypted'
            crypto.encrypt_file(str(module_file), str(encrypted_file), key)
            
            # 测试模块加载器
            loader = SmartModuleLoader()
            loader.register_encrypted_module('test_module', str(encrypted_file))
            
            # 模拟模块导入
            import types
            module = types.ModuleType('test_module')
            loader.exec_module(module)
            
            # 验证模块内容
            assert hasattr(module, 'test_function')
            assert hasattr(module, 'TEST_CONSTANT')
            assert module.test_function() == "Hello from encrypted module!"
            assert module.TEST_CONSTANT == "This is a test constant"
            
            print("  ✅ 加密模块加载测试通过")
            
        return True
        
    except Exception as e:
        print(f"  ❌ 模块加载测试失败: {e}")
        return False


def test_system_integration():
    """测试系统集成"""
    print("🚀 测试系统集成...")
    
    try:
        import bootstrap
        
        # 设置测试环境
        os.environ['ENCRYPTION_KEY'] = '1234567890123456'
        
        # 初始化系统
        system = bootstrap.initialize()
        
        # 验证系统状态
        assert system is not None
        assert system._is_initialized
        
        status = system.get_status()
        assert status['initialized']
        
        print("  ✅ 系统初始化测试通过")
        
        # 清理系统
        system.shutdown()
        print("  ✅ 系统关闭测试通过")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 系统集成测试失败: {e}")
        return False


def run_all_tests():
    """运行所有测试"""
    print("🧪 运行框架测试套件")
    print("=" * 50)
    
    tests = [
        ("基本加密功能", test_basic_encryption),
        ("文件发现功能", test_file_discovery),
        ("模块加载功能", test_module_loading),
        ("系统集成", test_system_integration),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"  ❌ 测试异常: {e}")
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！")
        return True
    else:
        print("❌ 部分测试失败")
        return False


if __name__ == '__main__':
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ 测试被用户中断")
        sys.exit(130)
