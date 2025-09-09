#!/usr/bin/env python3
"""
性能基准测试脚本
"""

import time
import os

# 设置环境变量
os.environ['ENCRYPTION_KEY'] = '1234567890123456'

try:
    from core.crypto import AESCrypto
    from core.auth import AuthManager
    
    crypto = AESCrypto()
    auth = AuthManager()
    key = auth.get_key()
    
    # 测试不同大小的文件
    sizes = [1024, 10240, 102400, 1024000]
    
    for size in sizes:
        data = os.urandom(size)
        
        # 测试加密性能
        start = time.time()
        encrypted = crypto.encrypt(data, key)
        encrypt_time = time.time() - start
        
        # 测试解密性能
        start = time.time()
        decrypted = crypto.decrypt(encrypted, key)
        decrypt_time = time.time() - start
        
        print(f'{size//1024:>6}KB: 加密 {encrypt_time*1000:>6.2f}ms, 解密 {decrypt_time*1000:>6.2f}ms')
        
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保已正确安装项目依赖")
except Exception as e:
    print(f"基准测试错误: {e}")
