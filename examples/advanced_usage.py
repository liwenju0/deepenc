#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级使用示例

演示框架的高级功能。
"""

import os
import sys
from pathlib import Path

import encrypt

# 添加框架路径
sys.path.insert(0, str(Path(__file__).parent.parent))


def example_custom_filter():
    """自定义过滤器示例"""
    print("🔍 自定义过滤器示例")

    from encrypt.discovery import FileFilter, FileScanner

    # 创建自定义过滤规则
    custom_rules = {
        "exclude_dirs": ["my_test_dir", "experimental"],
        "exclude_files": ["config.py", "settings.py"],
        "include_files": ["important.py"],  # 强制包含
    }

    # 使用自定义过滤器
    FileFilter(custom_rules)
    scanner = FileScanner(filter_rules=custom_rules)

    try:
        result = scanner.discover_all_files()
        print(f"发现文件: {result['total_files']} 个")
    except Exception as e:
        print(f"❌ 扫描失败: {e}")


def example_manual_encryption():
    """手动加密示例"""
    print("🔐 手动加密示例")

    from encrypt.core import AESCrypto, AuthManager

    try:
        # 初始化组件
        crypto = AESCrypto()
        auth = AuthManager()

        # 获取密钥
        key = auth.get_key()
        print(f"使用密钥长度: {len(key)}")

        # 加密数据
        test_data = b"Hello, Encrypted World!"
        encrypted = crypto.encrypt(test_data, key)

        # 解密数据
        decrypted = crypto.decrypt(encrypted, key)

        print(f"原始数据: {test_data}")
        print(f"解密数据: {decrypted}")
        print(f"加密成功: {test_data == decrypted}")

    except Exception as e:
        print(f"❌ 手动加密失败: {e}")


def example_system_monitoring():
    """系统监控示例"""
    print("📊 系统监控示例")

    # 启动系统
    system = encrypt.bootstrap()

    try:
        # 获取详细状态
        status = system.get_status()

        print("系统状态:")
        print(f"  已初始化: {status['initialized']}")
        print(f"  模块加载器: {status['module_loader_installed']}")
        print(f"  ONNX 加载器: {status['onnx_loader_installed']}")

        # 模块缓存信息
        module_cache = status["module_cache_info"]
        if module_cache:
            print(f"  缓存模块数: {module_cache.get('cached_modules', 0)}")
            print(f"  注册模块数: {module_cache.get('registered_modules', 0)}")

        # ONNX 缓存信息
        onnx_cache = status["onnx_cache_info"]
        if onnx_cache:
            print(f"  缓存模型数: {onnx_cache.get('cached_models', 0)}")
            print(f"  临时文件数: {onnx_cache.get('temp_files', 0)}")

    except Exception as e:
        print(f"❌ 获取状态失败: {e}")

    finally:
        system.shutdown()


def example_error_handling():
    """错误处理示例"""
    print("❌ 错误处理示例")

    from encrypt.core import AuthenticationError, EncryptionError

    try:
        # 故意触发错误
        encrypt.bootstrap()

        # 尝试使用无效密钥
        from encrypt.core import AESCrypto

        crypto = AESCrypto()

        try:
            crypto.encrypt(b"test", "invalid_key")  # 无效密钥长度
        except EncryptionError as e:
            print(f"✅ 捕获加密错误: {e}")

        # 尝试访问不存在的授权
        try:
            from encrypt.core import AuthManager

            AuthManager()
            # 这里可能会失败，取决于环境

        except AuthenticationError as e:
            print(f"✅ 捕获授权错误: {e}")

    except Exception as e:
        print(f"⚠️ 未处理的错误: {e}")


def example_performance_test():
    """性能测试示例"""
    print("⚡ 性能测试示例")

    import time

    from encrypt.core import AESCrypto, AuthManager

    try:
        # 初始化
        crypto = AESCrypto()
        auth = AuthManager()
        key = auth.get_key()

        # 测试数据
        test_sizes = [1024, 10240, 102400, 1024000]  # 1KB, 10KB, 100KB, 1MB

        print("加密性能测试:")
        print(f"{'大小':<10} {'加密时间':<12} {'解密时间':<12} {'速度':<15}")
        print("-" * 55)

        for size in test_sizes:
            test_data = os.urandom(size)

            # 测试加密
            start_time = time.time()
            encrypted = crypto.encrypt(test_data, key)
            encrypt_time = time.time() - start_time

            # 测试解密
            start_time = time.time()
            decrypted = crypto.decrypt(encrypted, key)
            decrypt_time = time.time() - start_time

            # 验证正确性
            assert test_data == decrypted

            # 计算速度
            speed_mbps = (size / (1024 * 1024)) / max(encrypt_time, 0.001)

            print(
                f"{size//1024:>6}KB {encrypt_time*1000:>8.2f}ms {decrypt_time*1000:>8.2f}ms {speed_mbps:>10.2f}MB/s"
            )

    except Exception as e:
        print(f"❌ 性能测试失败: {e}")


if __name__ == "__main__":
    print("🎯 Python 项目加密分发框架 - 高级示例")
    print("=" * 60)

    examples = [
        ("自定义过滤器", example_custom_filter),
        ("手动加密", example_manual_encryption),
        ("系统监控", example_system_monitoring),
        ("错误处理", example_error_handling),
        ("性能测试", example_performance_test),
    ]

    for name, func in examples:
        print(f"\n📋 {name}")
        print("-" * 30)
        try:
            func()
        except KeyboardInterrupt:
            print("\n⚠️ 示例被用户中断")
            break
        except Exception as e:
            print(f"❌ 示例失败: {e}")

        print()  # 空行分隔
