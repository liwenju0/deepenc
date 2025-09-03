#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI 主入口

实现命令行接口的主入口点。
遵循 Linux 命令行工具的标准。
"""

import sys
import argparse
from pathlib import Path
from .commands import EncryptCLI


def create_parser():
    """创建命令行解析器
    
    Returns:
        argparse.ArgumentParser: 命令行解析器
    """
    parser = argparse.ArgumentParser(
        prog='deepenc',
        description='Python 项目加密分发框架',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  deepenc build                                    # 构建当前项目
  deepenc build --project /path                   # 构建指定项目
  deepenc build --entry-point src/main.py         # 指定入口文件
  deepenc build -x tests -x docs                  # 排除tests和docs目录
  deepenc build -x .git -x __pycache__            # 排除版本控制和缓存目录
  deepenc build -xf *.log -xf *.tmp               # 排除日志和临时文件
  deepenc scan                                     # 扫描当前项目
  deepenc status                                   # 显示系统状态
  deepenc clean                                    # 清理构建目录
  deepenc verify                                   # 验证构建结果

更多信息请访问: https://github.com/your-repo/deepenc
        """
    )
    
    # 全局选项
    parser.add_argument(
        '--version', 
        action='version', 
        version='%(prog)s 1.0.0'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='显示详细信息'
    )
    
    # 子命令
    subparsers = parser.add_subparsers(
        dest='command',
        help='可用命令',
        metavar='COMMAND'
    )
    
    # build 命令
    build_parser = subparsers.add_parser(
        'build',
        help='构建加密项目',
        description='自动发现并加密项目中的 Python 文件和 ONNX 模型'
    )
    build_parser.add_argument(
        '--project', '-p',
        default='.',
        help='项目根目录 (默认: 当前目录)'
    )
    build_parser.add_argument(
        '--output', '-o',
        help='输出目录 (默认: PROJECT/build)'
    )
    build_parser.add_argument(
        '--entry-point', '-e',
        help='项目入口Python文件 (默认: src/grpc_main.py)'
    )
    build_parser.add_argument(
        '--exclude-dir', '-x',
        action='append',
        help='排除指定目录，不纳入到build中 (可多次使用)'
    )
    build_parser.add_argument(
        '--exclude-file', '-xf',
        action='append',
        help='排除指定文件，不纳入到build中 (可多次使用)'
    )
    build_parser.add_argument(
        '--no-clean',
        action='store_true',
        help='不清理构建目录'
    )
    
    # scan 命令
    scan_parser = subparsers.add_parser(
        'scan',
        help='扫描项目文件',
        description='扫描项目中的 Python 文件和 ONNX 模型'
    )
    scan_parser.add_argument(
        '--project', '-p',
        default='.',
        help='项目根目录 (默认: 当前目录)'
    )
    scan_parser.add_argument(
        '--format', '-f',
        choices=['table', 'json', 'simple'],
        default='table',
        help='输出格式 (默认: table)'
    )
    
    # status 命令
    status_parser = subparsers.add_parser(
        'status',
        help='显示系统状态',
        description='显示加密系统的当前状态'
    )
    
    # init 命令
    init_parser = subparsers.add_parser(
        'init',
        help='初始化加密系统',
        description='初始化并启动加密系统'
    )
    init_parser.add_argument(
        '--project', '-p',
        default='.',
        help='项目根目录 (默认: 当前目录)'
    )
    
    # clean 命令
    clean_parser = subparsers.add_parser(
        'clean',
        help='清理构建目录',
        description='清理项目的构建目录'
    )
    clean_parser.add_argument(
        '--project', '-p',
        default='.',
        help='项目根目录 (默认: 当前目录)'
    )
    clean_parser.add_argument(
        '--build-dir',
        help='构建目录 (默认: PROJECT/build)'
    )
    
    # verify 命令
    verify_parser = subparsers.add_parser(
        'verify',
        help='验证构建结果',
        description='验证构建结果的完整性'
    )
    verify_parser.add_argument(
        '--build-dir',
        help='构建目录 (默认: 当前目录/build)'
    )
    
    return parser


def main():
    """CLI 主函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    # 如果没有提供命令，显示帮助
    if not args.command:
        parser.print_help()
        return 1
    
    # 创建 CLI 实例
    cli = EncryptCLI()
    
    try:
        # 路由到相应的命令处理函数
        if args.command == 'build':
            return cli.build(
                project_path=args.project,
                output_dir=args.output,
                entry_point=args.entry_point,
                exclude_dirs=args.exclude_dir,
                exclude_files=args.exclude_file,
                clean=not args.no_clean,
                verbose=args.verbose
            )
        
        elif args.command == 'scan':
            return cli.scan(
                project_path=args.project,
                output_format=args.format
            )
        
        elif args.command == 'status':
            return cli.status()
        
        elif args.command == 'init':
            return cli.init(project_path=args.project)
        
        elif args.command == 'clean':
            return cli.clean(
                project_path=args.project,
                build_dir=args.build_dir
            )
        
        elif args.command == 'verify':
            return cli.verify(build_dir=args.build_dir)
        
        else:
            print(f"❌ 未知命令: {args.command}")
            parser.print_help()
            return 1
    
    except KeyboardInterrupt:
        print("\n⚠️ 操作被用户中断")
        return 130  # Linux 标准的 SIGINT 退出码
    
    except Exception as e:
        print(f"❌ 命令执行失败: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
