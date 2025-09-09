#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整构建测试

测试修改后的项目构建器的完整构建流程。
"""

import sys
from pathlib import Path

from deepenc.builders.project_builder import ProjectBuilder

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))


def test_full_build():
    """测试完整构建流程"""
    print("🧪 测试完整构建流程")
    print("=" * 50)

    # 创建测试项目结构
    test_project = Path("test_build_project")
    test_project.mkdir(exist_ok=True)

    # 创建src目录和入口文件
    src_dir = test_project / "src"
    src_dir.mkdir(exist_ok=True)

    entry_file = src_dir / "grpc_main.py"
    with open(entry_file, "w", encoding="utf-8") as f:
        f.write(
            '''#!/usr/bin/env python3
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
'''
        )

    # 创建其他Python文件
    other_file = src_dir / "utils.py"
    with open(other_file, "w", encoding="utf-8") as f:
        f.write(
            '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具模块
"""
def helper():
    return "Helper function from utils module"
'''
        )

    # 创建__init__.py文件
    init_file = src_dir / "__init__.py"
    with open(init_file, "w", encoding="utf-8") as f:
        f.write(
            '''# -*- coding: utf-8 -*-
"""
src包初始化文件
"""
'''
        )

    # 创建配置文件
    conf_dir = test_project / "conf"
    conf_dir.mkdir(exist_ok=True)

    config_file = conf_dir / "app.conf"
    with open(config_file, "w", encoding="utf-8") as f:
        f.write(
            """[app]
name = test_app
version = 1.0.0
debug = true
"""
        )

    yaml_config = conf_dir / "settings.yaml"
    with open(yaml_config, "w", encoding="utf-8") as f:
        f.write(
            """app:
  name: test_app
  version: 1.0.0
  debug: true
database:
  host: localhost
  port: 5432
"""
        )

    # 创建requirements.txt
    requirements_file = test_project / "requirements.txt"
    with open(requirements_file, "w", encoding="utf-8") as f:
        f.write(
            """requests>=2.25.0
numpy>=1.19.0
"""
        )

    print("📁 测试项目结构:")
    print(f"  - 项目根目录: {test_project}")
    print(f"  - 入口文件: {entry_file}")
    print(f"  - 工具模块: {other_file}")
    print(f"  - 配置文件: {config_file}, {yaml_config}")

    # 测试构建
    print("\n🔨 开始构建测试...")
    try:
        builder = ProjectBuilder(test_project, entry_point="src/grpc_main.py")

        # 构建项目
        build_report = builder.build_project(auto_discover=True, clean=True)

        print("\n📊 构建结果:")
        print(f"  - 构建成功: {build_report['build_info']['success']}")
        print(f"  - 构建时间: {build_report['build_info']['duration_seconds']:.2f} 秒")
        print(
            f"  - Python模块: {build_report['encryption']['encrypted_python_modules']} 个"
        )
        print(f"  - 入口文件: {build_report['encryption']['entry_point']}")
        print(f"  - 构建目录: {build_report['output']['build_dir']}")
        print(f"  - 配置文件目录: {build_report['output']['conf_dir']}")

        # 验证构建结果
        print("\n🔍 验证构建结果...")
        if builder.verify_build():
            print("✅ 构建验证通过")
        else:
            print("❌ 构建验证失败")

        # 检查生成的文件
        build_dir = Path(build_report["output"]["build_dir"])
        print(f"\n📁 构建目录内容:")
        for item in build_dir.rglob("*"):
            if item.is_file():
                print(f"  - {item.relative_to(build_dir)}")

        # 检查配置文件内容
        config_file = Path(build_report["output"]["config_file"])
        if config_file.exists():
            print(f"\n📋 配置文件内容:")
            with open(config_file, "r", encoding="utf-8") as f:
                config_content = f.read()
                print(config_content)
        else:
            print(f"\n❌ 配置文件不存在: {config_file}")

        # 检查入口文件
        entry_file = Path(build_report["output"]["entry_point"])
        if entry_file.exists():
            print(f"\n🚪 入口文件内容:")
            with open(entry_file, "r", encoding="utf-8") as f:
                entry_content = f.read()
                print(
                    entry_content[:200] + "..."
                    if len(entry_content) > 200
                    else entry_content
                )
        else:
            print(f"\n❌ 入口文件不存在: {entry_file}")

    except Exception as e:
        print(f"❌ 构建测试失败: {e}")
        import traceback

        traceback.print_exc()

    # 清理测试文件
    import shutil

    if test_project.exists():
        shutil.rmtree(test_project)

    print("\n✅ 完整构建测试完成")


if __name__ == "__main__":
    test_full_build()
