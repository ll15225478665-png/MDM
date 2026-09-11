#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MDM 测试报告生成器
支持 HTML 和 Excel 格式的结构化测试报告
"""
import os
import json
import html
from datetime import datetime
from pathlib import Path


class TestReportGenerator:
    """测试报告生成器"""
    
    def __init__(self, output_dir="reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results = []
    
    def add_result(self, test_name, status, duration=0, error_msg="", screenshot=""):
        """添加测试结果"""
        self.results.append({
            "test_name": test_name,
            "status": status,  # PASSED/FAILED/ERROR
            "duration": duration,
            "error_msg": error_msg,
            "screenshot": screenshot,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    def generate_html_report(self, filename=None):
        """生成 HTML 报告"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_report_{timestamp}.html"
        
        filepath = self.output_dir / filename
        
        # 统计数据
        total = len(self.results)
        passed = sum(1 for r in self.results if r["status"] == "PASSED")
        failed = sum(1 for r in self.results if r["status"] == "FAILED")
        errors = sum(1 for r in self.results if r["status"] == "ERROR")
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        # 风险等级判定
        if errors > 0 or (failed > 3 and pass_rate < 80):
            risk_level = "高风险"
            risk_color = "#FF0000"
        elif failed > 0 or pass_rate < 95:
            risk_level = "中风险"
            risk_color = "#FFA500"
        else:
            risk_level = "低风险"
            risk_color = "#00AA00"
        
        # 生成 HTML
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MDM 测试报告</title>
    <style>
        body {{
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
        }}
        .header .subtitle {{
            margin-top: 10px;
            opacity: 0.9;
            font-size: 14px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #fafafa;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            text-align: center;
        }}
        .stat-card .number {{
            font-size: 36px;
            font-weight: bold;
            margin: 10px 0;
        }}
        .stat-card .label {{
            color: #666;
            font-size: 14px;
        }}
        .stat-card.passed .number {{ color: #00AA00; }}
        .stat-card.failed .number {{ color: #FF0000; }}
        .stat-card.errors .number {{ color: #FF6600; }}
        .stat-card.rate .number {{ color: #667eea; }}
        .risk-badge {{
            display: inline-block;
            padding: 8px 20px;
            border-radius: 20px;
            color: white;
            font-weight: bold;
            margin-top: 10px;
        }}
        .results-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 0;
        }}
        .results-table th {{
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        .results-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }}
        .results-table tr:hover {{
            background: #f9f9f9;
        }}
        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            color: white;
        }}
        .status-passed {{ background: #00AA00; }}
        .status-failed {{ background: #FF0000; }}
        .status-error {{ background: #FF6600; }}
        .error-msg {{
            color: #FF0000;
            font-size: 13px;
            margin-top: 5px;
            padding: 10px;
            background: #FFF5F5;
            border-left: 3px solid #FF0000;
            border-radius: 4px;
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
            padding: 20px;
            color: #999;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 MDM Web UI 自动化测试报告</h1>
            <div class="subtitle">生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
        </div>
        
        <div class="summary">
            <div class="stat-card">
                <div class="label">总用例数</div>
                <div class="number">{total}</div>
            </div>
            <div class="stat-card passed">
                <div class="label">通过</div>
                <div class="number">{passed}</div>
            </div>
            <div class="stat-card failed">
                <div class="label">失败</div>
                <div class="number">{failed}</div>
            </div>
            <div class="stat-card errors">
                <div class="label">错误</div>
                <div class="number">{errors}</div>
            </div>
            <div class="stat-card rate">
                <div class="label">通过率</div>
                <div class="number">{pass_rate:.1f}%</div>
            </div>
        </div>
        
        <div style="text-align: center; padding: 20px;">
            <span class="risk-badge" style="background: {risk_color};">
                风险等级: {risk_level}
            </span>
        </div>
        
        <table class="results-table">
            <thead>
                <tr>
                    <th style="width: 5%;">#</th>
                    <th style="width: 30%;">测试名称</th>
                    <th style="width: 10%;">状态</th>
                    <th style="width: 10%;">耗时</th>
                    <th style="width: 35%;">错误信息</th>
                    <th style="width: 10%;">截图</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for idx, result in enumerate(self.results, 1):
            status_class = f"status-{result['status'].lower()}"
            status_text = {"PASSED": "✅ 通过", "FAILED": "❌ 失败", "ERROR": "⚠️ 错误"}.get(result["status"], result["status"])
            
            error_html = ""
            if result["error_msg"]:
                escaped_error = html.escape(result["error_msg"])
                error_html = f'<div class="error-msg">{escaped_error}</div>'
            
            screenshot_html = ""
            if result["screenshot"]:
                screenshot_html = f'<a href="{result["screenshot"]}" class="screenshot-link" target="_blank">查看截图</a>'
            
            html_content += f"""
                <tr>
                    <td>{idx}</td>
                    <td><strong>{html.escape(result["test_name"])}</strong></td>
                    <td><span class="status-badge {status_class}">{status_text}</span>{error_html}</td>
                    <td>{result["duration"]:.2f}s</td>
                    <td></td>
                    <td>{screenshot_html}</td>
                </tr>
"""
        
        html_content += """
            </tbody>
        </table>
        
        <div class="footer">
            Generated by MDM Test Report Generator | Powered by Playwright + pytest
        </div>
    </div>
</body>
</html>
"""
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        return str(filepath)
    
    def generate_json_report(self, filename=None):
        """生成 JSON 报告（便于后续处理）"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_report_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        report_data = {
            "generated_at": datetime.now().isoformat(),
            "total": len(self.results),
            "passed": sum(1 for r in self.results if r["status"] == "PASSED"),
            "failed": sum(1 for r in self.results if r["status"] == "FAILED"),
            "errors": sum(1 for r in self.results if r["status"] == "ERROR"),
            "results": self.results
        }
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        return str(filepath)


# pytest hook 集成
def pytest_configure(config):
    """pytest 配置钩子"""
    config.report_generator = TestReportGenerator()


def pytest_runtest_logreport(report):
    """测试运行日志钩子"""
    from _pytest.runner import pytest
    
    # 只在测试完成时记录
    if report.when == "call":
        generator = getattr(pytest.config, "report_generator", None)
        if generator:
            # 提取测试名称
            test_name = f"{report.nodeid}"
            
            # 判断状态
            if report.passed:
                status = "PASSED"
            elif report.failed:
                status = "FAILED"
            else:
                status = "ERROR"
            
            # 提取错误信息
            error_msg = ""
            if hasattr(report, "longrepr"):
                error_msg = str(report.longrepr)
            
            # 查找截图
            screenshot = ""
            screenshots_dir = Path("screenshots")
            if screenshots_dir.exists():
                # 查找最新的截图文件
                screenshot_files = list(screenshots_dir.glob("*.png"))
                if screenshot_files:
                    latest_screenshot = max(screenshot_files, key=lambda p: p.stat().st_mtime)
                    screenshot = str(latest_screenshot)
            
            generator.add_result(
                test_name=test_name,
                status=status,
                duration=report.duration,
                error_msg=error_msg,
                screenshot=screenshot
            )


def pytest_sessionfinish(session, exitstatus):
    """测试会话结束钩子"""
    generator = getattr(session.config, "report_generator", None)
    if generator and generator.results:
        # 生成 HTML 报告
        html_report = generator.generate_html_report()
        print(f"\n📊 HTML 报告已生成: {html_report}")
        
        # 生成 JSON 报告
        json_report = generator.generate_json_report()
        print(f"📄 JSON 报告已生成: {json_report}")
