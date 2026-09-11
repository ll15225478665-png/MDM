#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HTMLTestRunner 集成方案
用于生成传统风格的 HTML 测试报告
"""
import sys
import os
from pathlib import Path
from datetime import datetime


def generate_htmltestrunner_report(test_results, output_dir="reports"):
    """
    生成 HTMLTestRunner 风格的 HTML 报告
    
    Args:
        test_results: 测试结果列表，每个元素包含：
            - test_name: 测试名称
            - status: PASSED/FAILED/ERROR
            - duration: 耗时（秒）
            - error_msg: 错误信息（可选）
            - screenshot: 截图路径（可选）
        output_dir: 输出目录
    
    Returns:
        str: HTML 报告文件路径
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_file = output_path / f"HTMLTestRunner_Report_{timestamp}.html"
    
    # 统计数据
    total = len(test_results)
    passed = sum(1 for r in test_results if r["status"] == "PASSED")
    failed = sum(1 for r in test_results if r["status"] == "FAILED")
    errors = sum(1 for r in test_results if r["status"] == "ERROR")
    pass_rate = (passed / total * 100) if total > 0 else 0
    
    # 生成 HTML（HTMLTestRunner 风格）
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>MDM Web UI 测试报告 - HTMLTestRunner 风格</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            padding: 20px;
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        .summary {{
            background: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .summary table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .summary td {{
            padding: 8px;
            border: 1px solid #ddd;
        }}
        .summary .label {{
            font-weight: bold;
            background: #f0f0f0;
            width: 150px;
        }}
        .pass {{
            color: #00AA00;
            font-weight: bold;
        }}
        .fail {{
            color: #FF0000;
            font-weight: bold;
        }}
        .error {{
            color: #FF6600;
            font-weight: bold;
        }}
        table.results {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        table.results th {{
            background: #667eea;
            color: white;
            padding: 10px;
            text-align: left;
        }}
        table.results td {{
            padding: 8px;
            border: 1px solid #ddd;
        }}
        table.results tr:nth-child(even) {{
            background: #f9f9f9;
        }}
        table.results tr:hover {{
            background: #f0f0f0;
        }}
        .error-msg {{
            color: #FF0000;
            font-size: 12px;
            white-space: pre-wrap;
            max-height: 200px;
            overflow-y: auto;
            background: #FFF5F5;
            padding: 10px;
            border-left: 3px solid #FF0000;
        }}
        .screenshot-link {{
            color: #667eea;
            text-decoration: none;
        }}
        .screenshot-link:hover {{
            text-decoration: underline;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #999;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 MDM Web UI 自动化测试报告</h1>
        <p style="color: #666;">生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | 风格: HTMLTestRunner</p>
        
        <div class="summary">
            <h2>测试摘要</h2>
            <table>
                <tr>
                    <td class="label">总用例数:</td>
                    <td>{total}</td>
                    <td class="label">通过:</td>
                    <td class="pass">{passed}</td>
                </tr>
                <tr>
                    <td class="label">失败:</td>
                    <td class="fail">{failed}</td>
                    <td class="label">错误:</td>
                    <td class="error">{errors}</td>
                </tr>
                <tr>
                    <td class="label">通过率:</td>
                    <td colspan="3"><strong>{pass_rate:.1f}%</strong></td>
                </tr>
            </table>
        </div>
        
        <h2>详细结果</h2>
        <table class="results">
            <thead>
                <tr>
                    <th style="width: 5%;">#</th>
                    <th style="width: 30%;">测试名称</th>
                    <th style="width: 10%;">状态</th>
                    <th style="width: 10%;">耗时 (秒)</th>
                    <th style="width: 35%;">错误信息</th>
                    <th style="width: 10%;">截图</th>
                </tr>
            </thead>
            <tbody>
"""
    
    for idx, result in enumerate(test_results, 1):
        status_class = result["status"].lower()
        status_text = {
            "PASSED": "✅ PASS",
            "FAILED": "❌ FAIL",
            "ERROR": "⚠️ ERROR"
        }.get(result["status"], result["status"])
        
        error_html = ""
        if result.get("error_msg"):
            import html as html_module
            escaped_error = html_module.escape(result["error_msg"])
            error_html = f'<div class="error-msg">{escaped_error}</div>'
        
        screenshot_html = ""
        if result.get("screenshot"):
            screenshot_html = f'<a href="{result["screenshot"]}" class="screenshot-link" target="_blank">查看截图</a>'
        
        html_content += f"""
                <tr>
                    <td>{idx}</td>
                    <td><strong>{result["test_name"]}</strong></td>
                    <td class="{status_class}">{status_text}</td>
                    <td>{result["duration"]:.2f}</td>
                    <td>{error_html}</td>
                    <td>{screenshot_html}</td>
                </tr>
"""
    
    html_content += """
            </tbody>
        </table>
        
        <div class="footer">
            Generated by MDM Test Framework (HTMLTestRunner Style) | Powered by Playwright + pytest
        </div>
    </div>
</body>
</html>
"""
    
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    return str(html_file)


# pytest 集成钩子
_test_results = []


def pytest_runtest_logreport(report):
    """收集测试结果"""
    if report.when == "call":
        test_name = report.nodeid
        
        if report.passed:
            status = "PASSED"
        elif report.failed:
            status = "FAILED"
        else:
            status = "ERROR"
        
        error_msg = ""
        if hasattr(report, "longrepr"):
            error_msg = str(report.longrepr)
        
        # 查找截图
        screenshot = ""
        screenshots_dir = Path("screenshots")
        if screenshots_dir.exists():
            screenshot_files = list(screenshots_dir.rglob("*.png"))
            if screenshot_files:
                latest_screenshot = max(screenshot_files, key=lambda p: p.stat().st_mtime)
                screenshot = str(latest_screenshot)
        
        _test_results.append({
            "test_name": test_name,
            "status": status,
            "duration": report.duration,
            "error_msg": error_msg,
            "screenshot": screenshot
        })


def pytest_sessionfinish(session, exitstatus):
    """测试结束后生成 HTMLTestRunner 报告"""
    if _test_results:
        html_file = generate_htmltestrunner_report(_test_results)
        print(f"\n[REPORT] HTMLTestRunner report generated: {html_file}")
