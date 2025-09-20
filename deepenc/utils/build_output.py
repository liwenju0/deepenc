#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
构建输出格式化器

遵循 Linus Torvalds 的架构审美：
- 单一职责：只负责格式化构建信息输出
- 简单性：避免过度设计
- 一致性：统一的输出格式
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class BuildInfo:
    """简化的构建信息结构
    
    遵循 Linus 原则：保持简单，只包含必要信息
    """
    success: bool
    duration: float
    build_dir: str
    files_processed: int
    files_encrypted: int
    skip_encryption: bool = False
    project_root: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None


class BuildOutputFormatter:
    """构建输出格式化器
    
    单一职责：只负责格式化构建信息输出
    遵循 Linus 原则：Do one thing and do it well
    """
    
    def format_summary(self, info: BuildInfo) -> str:
        """格式化构建摘要
        
        Args:
            info: 构建信息
            
        Returns:
            str: 格式化的摘要字符串
        """
        lines = []
        lines.append("Build Summary:")
        lines.append(f"  Status: {'SUCCESS' if info.success else 'FAILED'}")
        lines.append(f"  Duration: {info.duration:.2f}s")
        lines.append(f"  Build Directory: {info.build_dir}")
        lines.append(f"  Files Processed: {info.files_processed}")
        
        if info.skip_encryption:
            lines.append(f"  Encryption: SKIPPED")
        else:
            lines.append(f"  Files Encrypted: {info.files_encrypted}")
        
        return "\n".join(lines)
    
    def format_verbose(self, info: BuildInfo) -> str:
        """格式化详细构建信息
        
        Args:
            info: 构建信息
            
        Returns:
            str: 格式化的详细信息字符串
        """
        lines = []
        lines.append("Build Report:")
        lines.append("=" * 50)
        
        # 基本信息
        lines.append("Basic Info:")
        lines.append(f"  Project Root: {info.project_root or 'N/A'}")
        lines.append(f"  Build Directory: {info.build_dir}")
        lines.append(f"  Status: {'SUCCESS' if info.success else 'FAILED'}")
        
        # 时间信息
        if info.start_time:
            lines.append(f"  Start Time: {info.start_time}")
        if info.end_time:
            lines.append(f"  End Time: {info.end_time}")
        lines.append(f"  Duration: {info.duration:.2f}s")
        
        # 文件信息
        lines.append("\nFile Processing:")
        lines.append(f"  Files Processed: {info.files_processed}")
        
        if info.skip_encryption:
            lines.append(f"  Encryption: SKIPPED")
            lines.append("  Note: All files copied without encryption")
        else:
            lines.append(f"  Files Encrypted: {info.files_encrypted}")
            lines.append("  Note: Python files and ONNX models encrypted")
        
        return "\n".join(lines)
    
    def format_json(self, info: BuildInfo) -> str:
        """格式化 JSON 输出
        
        Args:
            info: 构建信息
            
        Returns:
            str: JSON 格式的字符串
        """
        import json
        
        data = {
            "success": info.success,
            "duration": info.duration,
            "build_dir": info.build_dir,
            "files_processed": info.files_processed,
            "files_encrypted": info.files_encrypted,
            "skip_encryption": info.skip_encryption,
            "project_root": info.project_root,
            "start_time": info.start_time,
            "end_time": info.end_time,
        }
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def format_simple(self, info: BuildInfo) -> str:
        """格式化简单输出（用于脚本集成）
        
        Args:
            info: 构建信息
            
        Returns:
            str: 简单的单行输出
        """
        status = "OK" if info.success else "FAILED"
        encryption = "SKIP" if info.skip_encryption else f"{info.files_encrypted}"
        
        return f"BUILD {status} {info.duration:.2f}s {info.files_processed} files {encryption} encrypted"


def create_build_info_from_report(build_report: Dict[str, Any]) -> BuildInfo:
    """从构建报告创建 BuildInfo 对象
    
    Args:
        build_report: 原始构建报告
        
    Returns:
        BuildInfo: 简化的构建信息
    """
    build_info = build_report.get("build_info", {})
    discovery = build_report.get("discovery", {})
    encryption = build_report.get("encryption", {})
    
    return BuildInfo(
        success=build_report.get("success", False),
        duration=build_info.get("duration_seconds", 0.0),
        build_dir=build_info.get("build_dir", ""),
        files_processed=discovery.get("total_files", 0),
        files_encrypted=encryption.get("python_files_processed", 0) + 
                       encryption.get("onnx_files_processed", 0),
        skip_encryption=build_report.get("skip_encryption", False),
        project_root=build_info.get("project_root"),
        start_time=build_info.get("start_time"),
        end_time=build_info.get("end_time"),
    )
