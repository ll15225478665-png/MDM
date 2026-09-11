# HTMLTestRunner 集成使用指南

## 📋 概览

MDM 测试框架已集成 **HTMLTestRunner** 风格的 HTML 报告生成器。

**特点**:
- ✅ 自动生成 HTML 测试报告
- ✅ 统计通过率、失败数、错误数
- ✅ 显示每个测试的详细结果
- ✅ 失败时关联截图链接
- ✅ 传统 HTMLTestRunner 风格，易于团队接受

---

## 🎯 使用方法

### **方法 1: 直接运行 pytest（推荐）**

```bash
# 运行所有测试，自动生成 HTMLTestRunner 报告
pytest TestCase/role/ -v

# 运行特定测试文件
pytest TestCase/role/test_role_module_logging.py -v
```

**输出**:
```
TestCase/role/test_role_module_logging.py::test_role_with_module_logging PASSED [100%]

[REPORT] HTMLTestRunner report generated: reports\HTMLTestRunner_Report_20260910_145445.html

1 passed in 46.20s
```

**报告位置**: `reports/HTMLTestRunner_Report_YYYYMMDD_HHMMSS.html`

---

### **方法 2: 使用快捷脚本**

```bash
python scripts\run_with_htmltestrunner.py
```

**效果**: 自动运行测试并提示报告位置

---

## 📊 报告内容

### **测试摘要**

| 项目 | 说明 |
|------|------|
| 总用例数 | 执行的测试总数 |
| 通过 | 成功的测试数（绿色） |
| 失败 | 失败的测试数（红色） |
| 错误 | 出错的测试数（橙色） |
| 通过率 | 成功百分比 |

### **详细结果表格**

| 列 | 说明 |
|----|------|
| # | 序号 |
| 测试名称 | 完整的测试函数名 |
| 状态 | PASS/FAIL/ERROR（带颜色） |
| 耗时 | 执行时间（秒） |
| 错误信息 | 失败时的详细错误（可滚动查看） |
| 截图 | 失败时的截图链接（点击可查看） |

---

## 🔍 报告示例

### **成功时**

```html
<tr>
    <td>1</td>
    <td><strong>test_role_module_logging.py::test_role_with_module_logging</strong></td>
    <td class="passed">✅ PASS</td>
    <td>46.20</td>
    <td></td>
    <td></td>
</tr>
```

### **失败时**

```html
<tr>
    <td>1</td>
    <td><strong>test_xxx.py::test_failed</strong></td>
    <td class="failed">❌ FAIL</td>
    <td>30.50</td>
    <td>
        <div class="error-msg">
AssertionError: Locator expected to be visible
Actual value: None
Call log:
LocatorAssertions.to_be_visible with timeout 10000ms
waiting for locator(".el-menu").first
        </div>
    </td>
    <td><a href="screenshots/role/failed_test_xxx.png" target="_blank">查看截图</a></td>
</tr>
```

---

## 💡 最佳实践

### ✅ **应该做的**

1. **每次运行后查看报告**
   ```bash
   # 运行测试
   pytest TestCase/role/ -v
   
   # 打开最新报告
   start reports\HTMLTestRunner_Report_*.html
   ```

2. **定期清理旧报告**
   ```bash
   # 删除 30 天前的报告
   forfiles /p "reports" /m "HTMLTestRunner_*.html" /d -30 /c "cmd /c del @path"
   ```

3. **将报告纳入 CI/CD**
   - Jenkins/GitHub Actions 可以归档 HTML 报告
   - 邮件发送报告链接给团队

### ❌ **不应该做的**

1. **不要手动修改报告文件**
   - 报告是自动生成的，下次运行会覆盖

2. **不要依赖报告作为唯一记录**
   - 保留日志文件（`logs/`）和截图（`screenshots/`）

---

## 🔧 自定义配置

### **修改输出目录**

编辑 `utils/htmltestrunner_integration.py`:

```python
def generate_htmltestrunner_report(test_results, output_dir="reports"):
    # 修改 output_dir 参数
    ...
```

### **修改报告文件名格式**

```python
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
html_file = output_path / f"MyReport_{timestamp}.html"  # 自定义文件名
```

### **修改 HTML 样式**

编辑 `generate_htmltestrunner_report()` 函数中的 `<style>` 部分。

---

## 📚 与其他报告工具对比

| 特性 | HTMLTestRunner | 内置 report_generator |
|------|---------------|----------------------|
| 风格 | 传统表格风格 | 现代卡片式设计 |
| 统计图表 | ❌ 无 | ✅ 有（统计卡片） |
| 风险等级 | ❌ 无 | ✅ 有（低/中/高） |
| JSON 导出 | ❌ 无 | ✅ 有 |
| 团队兼容性 | ✅ 好（熟悉 HTMLTestRunner） | ⚠️ 需适应新风格 |

**建议**: 
- 如果团队熟悉 HTMLTestRunner → 使用本集成
- 如果需要更现代的报告 → 使用内置 `report_generator.py`

---

## 🐛 故障排查

### 问题 1: 报告没有生成

**检查**:
1. `conftest.py` 是否导入了 `htmltestrunner_integration`？
2. 是否有测试被执行？
3. `reports/` 目录是否存在？

**解决**:
```python
# conftest.py 末尾应该有这一行
from utils.htmltestrunner_integration import pytest_runtest_logreport, pytest_sessionfinish
```

### 问题 2: 报告中没有截图链接

**检查**:
1. 测试是否失败？（只有失败才有截图）
2. `@capture_exceptions` 装饰器是否添加？
3. 截图是否保存到 `screenshots/` 目录？

**解决**:
```python
@capture_exceptions  # ← 确保有这个装饰器
def test_my_feature(page, env_config):
    ...
```

### 问题 3: 报告中文乱码

**原因**: Windows 控制台编码问题

**解决**: 报告本身是 UTF-8 编码，用浏览器打开即可正常显示中文。

---

## 📄 完整示例

### **运行测试**

```bash
pytest TestCase/role/ -v
```

### **生成的文件**

```
reports/
└── HTMLTestRunner_Report_20260910_145445.html
```

### **打开报告**

```bash
# Windows
start reports\HTMLTestRunner_Report_20260910_145445.html

# macOS
open reports/HTMLTestRunner_Report_20260910_145445.html

# Linux
xdg-open reports/HTMLTestRunner_Report_20260910_145445.html
```

---

**最后更新**: 2026-09-10  
**版本**: v1.0  
**维护者**: MDM QA Team
