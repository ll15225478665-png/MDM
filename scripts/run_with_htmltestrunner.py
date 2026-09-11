#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
运行测试并生成 HTMLTestRunner 风格报告

用法:
    python scripts/run_with_htmltestrunner.py
"""
import sys
import subprocess
from pathlib import Path


def main():
    print("=" * 80)
    print("🚀 MDM Web UI 自动化测试 - HTMLTestRunner 报告生成")
    print("=" * 80)
    
    # 运行 pytest
    print("\n📝 正在运行测试...")
    result = subprocess.run(
        ["pytest", "TestCase/role/", "-v", "--tb=short"],
        capture_output=False,
        text=True
    )
    
    if result.returncode == 0:
        print("\n✅ 所有测试通过！")
    else:
        print(f"\n⚠️  部分测试失败（退出码: {result.returncode}）")
    
    # HTMLTestRunner 报告会通过 pytest hook 自动生成
    print("\n📊 HTMLTestRunner 报告已保存到 reports/ 目录")
    print("\n💡 提示: 打开 reports/HTMLTestRunner_Report_*.html 查看报告")
    
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
