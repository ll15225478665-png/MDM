# MDM Web UI 测试框架 - 功能概览

## 📋 核心功能

### 1. 自动化测试执行
- **Playwright 浏览器自动化** - Chromium 自动操作
- **OCR 验证码识别** - ddddocr 自动登录
- **多环境配置** - env.yaml 集中管理（dev/test/prod）
- **Session 级别 fixture** - 单浏览器实例共享，提升执行速度

### 2. 稳定性保障（已优化）
- ✅ Unicode 编码修复 - Windows GBK 兼容
- ✅ 页面加载策略优化 - `domcontentloaded` 避免超时
- ✅ 代理禁用 - `--no-proxy-server` 避免干扰
- ✅ URL 登录验证 - 避免选择器误判
- ✅ 显示等待 + expect 自动重试 - 替代强制等待

### 3. 详细日志记录（新增）
**工具**: `utils/test_logger.py`

**功能**:
- 分级日志（DEBUG/INFO/WARNING/ERROR）
- 模块化分类（步骤、断言、导航、元素操作）
- 自动保存日志文件到 `logs/` 目录
- pytest 自动集成

**使用示例**:
```python
from utils.test_logger import logger

def test_example(page):
    logger.info("开始测试")
    logger.step(1, "打开页面")
    logger.assertion("按钮可见", "visible", "visible", passed=True)
    logger.navigation(page.url, "首页")
```

**输出示例**:
```
2026-09-10 14:16:05 [INFO] [步骤 1] 打开页面
2026-09-10 14:16:06 [DEBUG] 🖱️ 点击 [登录按钮] (可见)
2026-09-10 14:16:06 [INFO] 🔗 导航到: https://xxx.com/home (首页)
2026-09-10 14:16:06 [INFO] ✅ PASS | 按钮可见
  期望: visible
  实际: visible
```

### 4. 结构化测试报告（新增）
**工具**: `utils/report_generator.py`

**支持格式**:
- **HTML 可视化报告** - 带统计卡片、风险等级、截图链接
- **JSON 结构化数据** - 便于后续处理和 CI/CD 集成

**功能**:
- 自动统计通过率、失败数、错误数
- 风险等级判定（低/中/高）
- 失败原因分类
- 截图关联
- pytest 自动集成

**HTML 报告特性**:
- 响应式设计
- 渐变色头部
- 统计卡片（总数/通过/失败/错误/通过率）
- 风险等级徽章（颜色区分）
- 详细结果表格（状态、耗时、错误信息、截图链接）
- 悬停效果

**使用示例**:
```python
# pytest 会自动调用报告生成器
# 无需手动调用，测试结束后自动生成

# 运行测试后查看 reports/ 目录
pytest TestCase/role/ -v
```

**报告位置**: `reports/test_report_YYYYMMDD_HHMMSS.html`

### 5. 异常截图捕获
**装饰器**: `@capture_exceptions`

**功能**:
- 测试失败时自动截图
- 保存到 `screenshots/` 目录
- 文件名包含测试名称和时间戳
- 报告中自动关联截图

---

## 🛠️ 工具脚本

### 1. 稳定性检查脚本
**文件**: `scripts/check_stability.py`

**功能**:
- 检查环境配置（env.yaml）
- 检查 conftest.py 关键修复
- 检查依赖包版本
- 一键诊断测试环境问题

**使用**:
```bash
python scripts\check_stability.py
```

### 2. 诊断测试脚本
**文件**: `test_debug.py`

**功能**:
- 最小化浏览器测试
- 验证网络连通性
- 诊断 Playwright 问题

**使用**:
```bash
python test_debug.py
```

---

## 📊 运行测试

### 标准运行
```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest TestCase/role/test_role_susscifl.py -v

# 快速验证（关键词过滤）
pytest -k role -v
```

### 调试模式
```bash
# 保持浏览器打开（按 Enter 关闭）
set DEBUG=1 && pytest TestCase/role/test_role_susscifl.py -v -s

# PyCharm 运行时自动保持打开（无需设置 DEBUG）
```

### 带日志和报告
```bash
# 正常运行即自动生成日志和报告
pytest TestCase/role/ -v

# 查看输出
# - 控制台: 实时日志
# - logs/: 详细日志文件
# - reports/: HTML/JSON 报告
# - screenshots/: 失败截图
```

---

## 📁 项目结构

```
D:\mdm\
├── conftest.py              # pytest 配置和 fixtures
├── requirements.txt         # Python 依赖
├── config/
│   └── env.yaml            # 环境配置
├── utils/
│   ├── toolkit.py          # 工具集（截图、日志等）
│   ├── test_logger.py      # ✨ 新增：详细日志记录
│   └── report_generator.py # ✨ 新增：报告生成器
├── TestCase/
│   └── role/
│       ├── test_role_susscifl.py        # 基础测试
│       └── test_role_with_logging.py    # ✨ 示例：带详细日志的测试
├── scripts/
│   └── check_stability.py  # ✨ 稳定性检查脚本
├── logs/                   # ✨ 新增：日志文件目录
├── reports/                # ✨ 新增：测试报告目录
├── screenshots/            # 失败截图
└── test_debug.py           # 诊断脚本
```

---

## 🎯 最佳实践

### 1. 编写新测试
```python
from utils.test_logger import logger
from playwright.sync_api import expect

@capture_exceptions
def test_my_feature(page, env_config):
    logger.info("开始测试: 我的功能")
    
    # 步骤 1: 导航
    logger.step(1, "打开页面")
    page.goto(f"{env_config.base_url}/#/my-page")
    logger.navigation(page.url, "我的页面")
    
    # 步骤 2: 验证元素
    logger.step(2, "验证按钮可见")
    expect(page.get_by_role("button", name="提交")).to_be_visible()
    logger.assertion("按钮可见", "visible", "visible", passed=True)
    
    # 步骤 3: 执行操作
    logger.step(3, "点击提交按钮")
    page.get_by_role("button", name="提交").click()
    logger.element_action("点击", "提交按钮")
    
    logger.info("✅ 测试通过")
```

### 2. 运行前检查
```bash
# 每次运行前执行
python scripts\check_stability.py

# 确认所有检查通过后，再运行测试
pytest TestCase/role/ -v
```

### 3. 故障排查
```
测试失败 → 查看 reports/test_report_*.html
         → 查看 logs/test_*.log
         → 查看 screenshots/ 目录截图
         → 运行 python test_debug.py 诊断网络
```

---

## 🚀 未来改进方向

### 短期（建议优先实现）
1. **Excel 报告生成** - 参考记忆中的 5 大核心分类标准
2. **CI/CD 集成** - GitHub Actions / Jenkins 自动运行
3. **邮件通知** - 测试失败自动发送邮件
4. **历史趋势分析** - 通过率变化图表

### 中期
1. **AI 辅助用例生成** - 基于 PRD 自动生成测试用例
2. **视觉回归测试** - Percy / Applitools 集成
3. **性能监控** - 页面加载时间、API 响应时间统计
4. **多浏览器测试** - Firefox / WebKit 覆盖

### 长期
1. **零代码测试平台** - 导入 Excel 用例自动执行
2. **智能元素定位** - AI 辅助元素识别
3. **自愈能力** - 元素定位失败时自动尝试其他策略
4. **分布式执行** - 并行运行多个测试文件

---

## 📞 技术支持

如有问题，请查看：
1. `QWEN.md` - 项目完整文档
2. `README.md` - 快速入门指南
3. `logs/` 目录 - 详细执行日志
4. `reports/` 目录 - 结构化测试报告

---

**最后更新**: 2026-09-10  
**版本**: v1.0  
**维护者**: MDM QA Team
