# MDM Web UI 自动化测试框架

基于 Playwright + pytest 的 MDM Web 端 UI 自动化测试框架。

## 快速开始

```bash
# 1. 激活虚拟环境
venv\Scripts\activate

# 2. 安装依赖
pip install -r requirements.txt
pip install ddddocr

# 3. 安装浏览器
playwright install chromium

# 4. 运行测试
pytest
```

## 目录结构

```
├── conftest.py           # pytest fixtures（浏览器、页面、自动登录）
├── requirements.txt      # Python 依赖
├── .gitignore
├── config/
│   ├── __init__.py
│   └── env.yaml          # 多环境配置（dev/test/prod）
├── pages/
│   ├── __init__.py
│   ├── base_page.py      # 页面基类
│   └── login_page.py     # 登录页 POM
├── utils/
│   ├── __init__.py
│   └── toolkit.py        # 工具：日志、截图、文件搜索
├── TestCase/
│   ├── __init__.py
│   └── test_*.py         # 测试用例
├── scripts/              # 调试/辅助脚本（不被 pytest 收集）
├── screenshots/          # 运行时的失败截图
└── openspec/             # OpenSpec 工作流文件
```

## 环境配置

编辑 `config/env.yaml` 管理各环境 URL 和账号。切换环境修改 `conftest.py` 中的 `CURRENT_ENV` 变量。

## 运行测试

```bash
pytest                           # 全部测试
pytest TestCase/test_xxx.py -v   # 单个文件
pytest -k "login" -v             # 按名称过滤
DEBUG=1 pytest -v -s             # 调试模式（浏览器不自动关闭）
```

## 编写新测试

在 `TestCase/` 下创建 `test_*.py`，使用 `@capture_exceptions` 装饰器自动在失败时截图：

```python
from utils.toolkit import capture_exceptions

@capture_exceptions
def test_my_feature(page, env_config):
    page.goto(f"{env_config.base_url}/#/my-page")
    assert page.title() == "Expected Title"
```
