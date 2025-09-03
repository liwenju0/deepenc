#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI测试脚本

测试修改后的CLI命令功能。
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from deepenc.builders.project_builder import ProjectBuilder


def create_test_project():
    """创建测试项目"""
    test_project = Path("test_cli_project")
    test_project.mkdir(exist_ok=True)
    
    # 创建src目录和入口文件
    src_dir = test_project / "src"
    src_dir.mkdir(exist_ok=True)
    
    entry_file = src_dir / "grpc_main.py"
    with open(entry_file, "w", encoding="utf-8") as f:
        f.write('''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试入口文件
"""
print("Hello from grpc_main.py")

def main():
    print("Running main function")
    from .utils import helper
    print(helper())

if __name__ == "__main__":
    main()
''')
    
    # 创建其他Python文件
    other_file = src_dir / "utils.py"
    with open(other_file, "w", encoding="utf-8") as f:
        f.write('''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具模块
"""
def helper():
    return "Helper function from utils module"
''')
    
    # 创建__init__.py文件
    init_file = src_dir / "__init__.py"
    with open(init_file, "w", encoding="utf-8") as f:
        f.write('''# -*- coding: utf-8 -*-
"""
src包初始化文件
"""
''')
    
    # 创建配置文件
    conf_dir = test_project / "conf"
    conf_dir.mkdir(exist_ok=True)
    
    config_file = conf_dir / "app.conf"
    with open(config_file, "w", encoding="utf-8") as f:
        f.write("""[app]
name = test_app
version = 1.0.0
debug = true
""")
    
    yaml_config = conf_dir / "settings.yaml"
    with open(yaml_config, "w", encoding="utf-8") as f:
        f.write("""app:
  name: test_app
  version: 1.0.0
  debug: true
database:
  host: localhost
  port: 5432
""")
    
    print("📁 测试项目已创建:")
    print(f"  - 项目根目录: {test_project}")
    print(f"  - 入口文件: {entry_file}")
    print(f"  - 工具模块: {other_file}")
    print(f"  - 配置文件: {config_file}, {yaml_config}")
    
    return test_project


def test_project_builder():
    """测试项目构建器"""
    print("\n🧪 测试项目构建器功能")
    print("=" * 50)
    
    test_project = create_test_project()
    
    # 测试默认入口文件
    print("\n1. 测试默认入口文件 (src/grpc_main.py)")
    try:
        builder = ProjectBuilder(test_project)
        print(f"✅ 默认入口文件: {builder.entry_point}")
    except Exception as e:
        print(f"❌ 默认入口文件测试失败: {e}")
    
    # 测试自定义入口文件
    print("\n2. 测试自定义入口文件")
    try:
        custom_entry = test_project / "src" / "utils.py"
        builder = ProjectBuilder(test_project, entry_point=str(custom_entry))
        print(f"✅ 自定义入口文件: {builder.entry_point}")
    except Exception as e:
        print(f"❌ 自定义入口文件测试失败: {e}")
    
    # 测试相对路径入口文件
    print("\n3. 测试相对路径入口文件")
    try:
        builder = ProjectBuilder(test_project, entry_point="src/utils.py")
        print(f"✅ 相对路径入口文件: {builder.entry_point}")
    except Exception as e:
        print(f"❌ 相对路径入口文件测试失败: {e}")
    
    print("\n✅ 项目构建器测试完成")
    print(f"💡 测试项目保留在: {test_project}")
    print("💡 现在可以测试CLI命令:")
    print(f"  python -m deepenc.cli.main build --project {test_project}")
    print(f"  python -m deepenc.cli.main build --project {test_project} --entry-point src/utils.py")


if __name__ == "__main__":
    test_project_builder()
