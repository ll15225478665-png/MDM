#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MDM 测试稳定性检查脚本
运行前执行此脚本，确保所有配置正确
"""
import sys
import yaml
from pathlib import Path

def check_env_config():
    """检查环境配置"""
    print("=" * 60)
    print("1. 检查环境配置文件")
    print("=" * 60)
    
    config_path = Path(__file__).parent.parent / "config" / "env.yaml"
    if not config_path.exists():
        print(f"❌ 配置文件不存在: {config_path}")
        return False
    
    with open(config_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    if "environments" not in data:
        print("❌ env.yaml 缺少 'environments' 根节点")
        return False
    
    # 读取 conftest.py 中的 CURRENT_ENV（更健壮的解析）
    conftest_path = Path(__file__).parent.parent / "conftest.py"
    current_env = None
    with open(conftest_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("CURRENT_ENV") and "=" in line:
                # 提取引号内的值
                parts = line.split("=")
                if len(parts) >= 2:
                    value = parts[1].strip()
                    # 移除引号和注释
                    value = value.split("#")[0]  # 去掉注释
                    value = value.strip().strip('"').strip("'")
                    current_env = value
                    break
    
    if not current_env:
        print("❌ conftest.py 中未找到 CURRENT_ENV")
        return False
    
    print(f"✅ 当前环境: {current_env}")
    
    if current_env not in data["environments"]:
        print(f"❌ 环境 '{current_env}' 未在 env.yaml 中定义")
        return False
    
    env_config = data["environments"][current_env]
    print(f"✅ Base URL: {env_config.get('base_url', 'N/A')}")
    print(f"✅ Username: {env_config.get('username', 'N/A')}")
    print(f"✅ Password: {'*' * len(env_config.get('password', ''))}")
    
    return True


def check_conftest_fixes():
    """检查 conftest.py 的关键修复"""
    print("\n" + "=" * 60)
    print("2. 检查 conftest.py 关键修复")
    print("=" * 60)
    
    conftest_path = Path(__file__).parent.parent / "conftest.py"
    content = conftest_path.read_text(encoding="utf-8")
    
    issues = []
    
    # 检查 1: Unicode emoji
    if "🔐" in content or "\\U0001f510" in content:
        issues.append("❌ 仍包含 Unicode emoji (🔐)，应改为 [LOGIN]")
    else:
        print("✅ Unicode emoji 已修复")
    
    # 检查 2: wait_until 参数
    if 'wait_until="load"' in content:
        issues.append("❌ 仍使用 wait_until='load'，应改为 'domcontentloaded'")
    elif 'wait_until="domcontentloaded"' in content:
        print("✅ wait_until 参数正确 (domcontentloaded)")
    else:
        issues.append("⚠️  未找到 wait_until 参数")
    
    # 检查 3: --no-proxy-server
    if "--no-proxy-server" in content:
        print("✅ 已禁用代理 (--no-proxy-server)")
    else:
        issues.append("⚠️  未禁用代理，可能受系统代理影响")
    
    # 检查 4: 登录验证用 URL
    if "window.location.href.includes('/Dashboard')" in content:
        print("✅ 登录验证使用 URL 判断（正确）")
    else:
        issues.append("❌ 登录验证未使用 URL 判断，可能导致误判")
    
    if issues:
        print("\n".join(issues))
        return False
    
    return True


def check_dependencies():
    """检查依赖包"""
    print("\n" + "=" * 60)
    print("3. 检查依赖包")
    print("=" * 60)
    
    try:
        import playwright
        # Playwright 没有 __version__，用 subprocess 获取
        import subprocess
        result = subprocess.run(
            ["python", "-m", "pip", "show", "playwright"],
            capture_output=True, text=True
        )
        version = "unknown"
        for line in result.stdout.splitlines():
            if line.startswith("Version:"):
                version = line.split(":")[1].strip()
                break
        print(f"✅ Playwright: {version}")
    except ImportError:
        print("❌ Playwright 未安装")
        return False
    
    try:
        import pytest
        print(f"✅ pytest: {pytest.__version__}")
    except ImportError:
        print("❌ pytest 未安装")
        return False
    
    try:
        import ddddocr
        print(f"✅ ddddocr: 已安装")
    except ImportError:
        print("❌ ddddocr 未安装（OCR 验证码需要）")
        return False
    
    try:
        import yaml
        print(f"✅ PyYAML: 已安装")
    except ImportError:
        print("❌ PyYAML 未安装")
        return False
    
    return True


def main():
    print("🔍 MDM 测试稳定性检查\n")
    
    results = []
    results.append(("环境配置", check_env_config()))
    results.append(("conftest.py 修复", check_conftest_fixes()))
    results.append(("依赖包", check_dependencies()))
    
    print("\n" + "=" * 60)
    print("检查结果汇总")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 所有检查通过！可以运行测试了。")
        print("\n💡 运行建议:")
        print("   - 首次运行: pytest TestCase/role/test_role_susscifl.py -v")
        print("   - 调试模式: set DEBUG=1 && pytest ... （浏览器保持打开）")
        print("   - 快速验证: pytest -k role -v")
        return 0
    else:
        print("\n⚠️  存在配置问题，请先修复后再运行测试。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
