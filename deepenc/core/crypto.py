#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AES 加密实现

重新实现的 AES-CFB 加密系统，与原项目保持兼容。
遵循 Linux 内核的错误处理风格。
"""

import os

from .errors import DecryptionError, EncryptionError

try:
    from Crypto.Cipher import AES
except ImportError:
    raise ImportError("PyCrypto is required. Install with: pip install pycrypto")


class AESCrypto:
    """AES-CFB 加密实现

    与原项目的 Crypt 类兼容的加密实现。
    使用固定的 salt 和 CFB 模式进行加密。
    """

    # 固定的 salt，与原项目保持一致
    SALT = b"SlTKeYOpHygTYkP3"

    # 默认加密长度：10MB
    DEFAULT_ENC_LEN = 1024 * 1024 * 10

    def __init__(self, enc_len=None):
        """初始化加密器

        Args:
            enc_len: 加密长度，默认 10MB
        """
        self.enc_len = enc_len or self.DEFAULT_ENC_LEN
        self.enc_dec_method = "utf-8"

    def encrypt(self, data, key):
        """加密数据

        Args:
            data: 要加密的数据 (bytes)
            key: 加密密钥 (str)

        Returns:
            bytes: 加密后的数据

        Raises:
            EncryptionError: 加密失败
        """
        if not isinstance(data, bytes):
            raise EncryptionError("数据必须是 bytes 类型")

        if not isinstance(key, str):
            raise EncryptionError("密钥必须是 str 类型")

        try:
            # 验证密钥长度
            key_bytes = key.encode("utf-8")
            if len(key_bytes) not in [16, 24, 32]:
                raise EncryptionError(
                    f"AES 密钥长度必须是 16、24 或 32 字节，当前长度: {len(key_bytes)}"
                )

            # 验证 salt 长度
            if len(self.SALT) != 16:
                raise EncryptionError(f"IV 必须是 16 字节长度，当前长度: {len(self.SALT)}")

            # 创建 AES 加密对象
            aes_obj = AES.new(key_bytes, AES.MODE_CFB, self.SALT, segment_size=128)

            # 部分加密：只加密前面的部分，后面保持原样
            encrypted_part = aes_obj.encrypt(data[: self.enc_len])
            remaining_part = data[self.enc_len :]

            return encrypted_part + remaining_part

        except ValueError as e:
            if "IV must be 16 bytes long" in str(e):
                raise EncryptionError("加密错误: SALT 必须是 16 字符长度")
            elif "AES key must be either 16, 24, or 32 bytes long" in str(e):
                raise EncryptionError("加密错误: 加密密钥必须是 16、24 或 32 字符长度")
            else:
                raise EncryptionError(f"加密失败: {e}")
        except Exception as e:
            raise EncryptionError(f"加密过程中发生错误: {e}")

    def decrypt(self, encrypted_data, key):
        """解密数据

        Args:
            encrypted_data: 加密的数据 (bytes)
            key: 解密密钥 (str)

        Returns:
            bytes: 解密后的数据

        Raises:
            DecryptionError: 解密失败
        """
        if not isinstance(encrypted_data, bytes):
            raise DecryptionError("加密数据必须是 bytes 类型")

        if not isinstance(key, str):
            raise DecryptionError("密钥必须是 str 类型")

        try:
            # 验证密钥长度
            key_bytes = key.encode("utf-8")
            if len(key_bytes) not in [16, 24, 32]:
                raise DecryptionError(
                    f"AES 密钥长度必须是 16、24 或 32 字节，当前长度: {len(key_bytes)}"
                )

            # 验证 salt 长度
            if len(self.SALT) != 16:
                raise DecryptionError(f"IV 必须是 16 字节长度，当前长度: {len(self.SALT)}")

            # 创建 AES 解密对象
            aes_obj = AES.new(key_bytes, AES.MODE_CFB, self.SALT, segment_size=128)

            # 部分解密：只解密前面的部分，后面保持原样
            decrypted_part = aes_obj.decrypt(encrypted_data[: self.enc_len])
            remaining_part = encrypted_data[self.enc_len :]

            return decrypted_part + remaining_part

        except ValueError as e:
            if "IV must be 16 bytes long" in str(e):
                raise DecryptionError("解密错误: SALT 必须是 16 字符长度")
            elif "AES key must be either 16, 24, or 32 bytes long" in str(e):
                raise DecryptionError("解密错误: 解密密钥必须是 16、24 或 32 字符长度")
            else:
                raise DecryptionError(f"解密失败: {e}")
        except Exception as e:
            raise DecryptionError(f"解密过程中发生错误: {e}")

    def encrypt_file(self, input_path, output_path, key):
        """加密文件

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            key: 加密密钥
        """
        try:
            with open(input_path, "rb") as f:
                data = f.read()

            encrypted_data = self.encrypt(data, key)

            # 确保输出目录存在
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            with open(output_path, "wb") as f:
                f.write(encrypted_data)

        except Exception as e:
            raise EncryptionError(f"加密文件失败 {input_path}: {e}")

    def decrypt_file(self, encrypted_path, key):
        """解密文件到内存

        Args:
            encrypted_path: 加密文件路径
            key: 解密密钥

        Returns:
            bytes: 解密后的数据
        """
        try:
            with open(encrypted_path, "rb") as f:
                encrypted_data = f.read()

            return self.decrypt(encrypted_data, key)

        except Exception as e:
            raise DecryptionError(f"解密文件失败 {encrypted_path}: {e}")

    def verify_key(self, key):
        """验证密钥格式

        Args:
            key: 要验证的密钥

        Returns:
            bool: 密钥是否有效
        """
        try:
            if not isinstance(key, str):
                return False

            key_bytes = key.encode("utf-8")
            return len(key_bytes) in [16, 24, 32]

        except Exception:
            return False
