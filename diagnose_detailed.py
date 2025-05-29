import sys
import os


def check_transformers_installation():
    print("=== 详细诊断 transformers 安装 ===")

    try:
        import transformers
        print(f"✅ transformers 导入成功")
        print(f"   版本: {transformers.__version__}")
        print(f"   文件位置: {transformers.__file__}")

        # 检查 __init__.py 内容
        init_file = transformers.__file__
        if init_file.endswith('__init__.py'):
            print(f"   __init__.py 路径: {init_file}")

            # 读取文件内容
            try:
                with open(init_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(f"   文件大小: {len(content)} 字符")

                    # 检查是否包含 pipeline
                    if 'from .pipelines import pipeline' in content:
                        print("   ✅ 找到 pipeline 导入语句")
                    elif 'pipeline' in content:
                        print("   ⚠️ 包含 pipeline 但导入语句可能不同")
                        # 显示包含 pipeline 的行
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if 'pipeline' in line.lower():
                                print(f"     第{i+1}行: {line.strip()}")
                    else:
                        print("   ❌ 未找到 pipeline 相关内容")

            except Exception as e:
                print(f"   ❌ 读取 __init__.py 失败: {e}")

        # 检查 transformers 目录结构
        transformers_dir = os.path.dirname(transformers.__file__)
        print(f"\n   transformers 目录: {transformers_dir}")

        try:
            files = os.listdir(transformers_dir)
            print(f"   目录包含 {len(files)} 个项目")

            # 检查关键文件/目录
            key_items = ['pipelines', 'models', 'tokenization_utils.py']
            for item in key_items:
                item_path = os.path.join(transformers_dir, item)
                if os.path.exists(item_path):
                    if os.path.isdir(item_path):
                        print(f"   ✅ 目录 {item} 存在")
                    else:
                        print(f"   ✅ 文件 {item} 存在")
                else:
                    print(f"   ❌ {item} 不存在")

        except Exception as e:
            print(f"   ❌ 检查目录失败: {e}")

    except Exception as e:
        print(f"❌ transformers 导入失败: {e}")
        return False

    # 尝试不同的导入方式
    print(f"\n=== 测试不同的导入方式 ===")

    # 方式1：直接从 transformers 导入
    try:
        from transformers import pipeline
        print("✅ 方式1成功: from transformers import pipeline")
    except Exception as e:
        print(f"❌ 方式1失败: {e}")

    # 方式2：从 pipelines 子模块导入
    try:
        from transformers.pipelines import pipeline
        print("✅ 方式2成功: from transformers.pipelines import pipeline")
    except Exception as e:
        print(f"❌ 方式2失败: {e}")

    # 方式3：检查 pipelines 模块
    try:
        import transformers.pipelines
        print("✅ 方式3成功: import transformers.pipelines")
        if hasattr(transformers.pipelines, 'pipeline'):
            print("   ✅ pipelines.pipeline 属性存在")
        else:
            print("   ❌ pipelines.pipeline 属性不存在")
    except Exception as e:
        print(f"❌ 方式3失败: {e}")

    return True


def check_conflicting_packages():
    print(f"\n=== 检查可能冲突的包 ===")

    import pkg_resources

    # 检查所有 transformers 相关的包
    transformers_packages = []
    for pkg in pkg_resources.working_set:
        if 'transform' in pkg.project_name.lower():
            transformers_packages.append(
                (pkg.project_name, pkg.version, pkg.location))

    print(f"找到 {len(transformers_packages)} 个相关包:")
    for name, version, location in transformers_packages:
        print(f"  - {name} {version}")
        print(f"    位置: {location}")


if __name__ == "__main__":
    check_transformers_installation()
    check_conflicting_packages()
