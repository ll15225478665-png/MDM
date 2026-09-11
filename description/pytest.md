# pytest 快速参考

> Python 测试框架 — fixture、命令、命名规则

---

## 一、Fixture（夹具）

fixture 是"准备工作"函数，测试函数通过参数名自动获取。

### 定义 fixture

```python
# conftest.py（pytest 自动加载）
import pytest

@pytest.fixture(scope="session")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page              # yield 前=准备，yield 后=清理
    context.close()
```

### 使用 fixture

```python
# 测试函数参数名和 fixture 同名，pytest 自动注入
def test_login(page):
    page.goto("https://example.com")
```

### scope 作用范围

| scope | 创建时机 | 适用场景 |
|-------|----------|----------|
| `function` | 每个测试函数运行前 | 测试需要完全隔离 |
| `class` | 每个测试类运行前 | 一组测试共享状态 |
| `module` | 每个 .py 文件运行前 | 同文件测试共享 |
| `session` | 整个 pytest 运行只一次 | 浏览器、数据库等重量级资源 |

### autouse=True

自动执行，测试函数不需要显式声明。

```python
@pytest.fixture(scope="session", autouse=True)
def auto_login(page):
    """所有测试运行前自动登录"""
    page.fill("#user", "admin")
    page.click("#login")
```

---

## 二、常用命令

```bash
pytest                          # 运行所有测试
pytest TestCase/test_xxx.py     # 运行指定文件
pytest -k "login"               # 按名称关键字过滤
pytest -v                       # 详细输出（显示每个测试名）
pytest -s                       # 显示 print() 输出
pytest --tb=short               # 简短错误堆栈
pytest --tb=long                # 完整错误堆栈
pytest -x                       # 遇到第一个失败就停止
pytest --lf                     # 只运行上次失败的测试
pytest --collect-only           # 只收集测试，不运行（查看有哪些测试）
DEBUG=1 pytest                  # 传环境变量
```

---

## 三、命名规则

| 类型 | 规则 | 示例 |
|------|------|------|
| 测试文件 | `test_` 开头 | `test_login_verify.py` |
| 测试函数 | `test_` 开头 | `test_login_with_invalid_password` |
| 测试类 | `Test` 开头 | `TestLoginModule` |

pytest 只收集符合命名规则的文件和函数，不符合的会被忽略。

---

## 四、参数化测试

同一套逻辑测多组数据，避免写重复代码。

```python
import pytest

@pytest.mark.parametrize("username, password, expect_success", [
    ("admin", "123456", True),
    ("guest", "", False),
    ("", "123456", False),
], ids=["正常登录", "无密码", "无用户名"])
def test_login(page, username, password, expect_success):
    page.fill("#user", username)
    page.fill("#pass", password)
    page.click("#login")

    if expect_success:
        assert "/dashboard" in page.url
    else:
        assert page.locator(".error").is_visible()
```

`ids` 参数让每个用例在报告中有可读名称。

---

## 五、推荐的文件结构

```python
# TestCase/test_xxx.py
from utils.toolkit import capture_exceptions

@capture_exceptions               # 失败时自动截图
def test_<模块>_<操作>_<条件>(page, env_config):
    """一句话描述测试目的"""
    # 1. 执行操作
    page.goto(f"{env_config.base_url}/#/target")

    # 2. 断言验证
    assert page.locator(".success").is_visible()
```

---

## 六、常用断言

pytest 直接用 Python 原生 `assert`，不需要 `self.assertEqual`。

```python
assert value == expected          # 等于
assert value != expected          # 不等于
assert value > 0                  # 大于
assert "sub" in text              # 包含
assert obj is None                # 是 None
assert len(items) == 5            # 长度
assert page.url.endswith("/ok")   # URL 结尾
```

断言失败时 pytest 会自动显示失败值，无需额外消息。
