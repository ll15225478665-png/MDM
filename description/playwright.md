# Playwright 快速参考

> 浏览器自动化框架 — 定位、操作、等待、断言

---

## 一、元素定位（推荐优先级：高 → 低）

### 1. get_by_role（最推荐）

按 ARIA 角色 + 名称定位，最接近用户视角。

```python
page.get_by_role("button", name="登录")         # 按钮
page.get_by_role("textbox", name="用户名")      # 输入框
page.get_by_role("checkbox", name="记住我")     # 复选框
page.get_by_role("link", name="忘记密码")       # 链接
page.get_by_role("heading", level=1)            # 一级标题
page.get_by_role("img", name="Logo")            # 图片
```

**常用 role**：`button`, `textbox`, `checkbox`, `radio`, `combobox`, `listbox`, `link`, `heading`, `img`, `table`, `row`, `cell`, `dialog`, `alert`

### 2. get_by_placeholder / get_by_label

```python
page.get_by_placeholder("请输入账号")     # 按输入框提示文字
page.get_by_label("邮箱地址")            # 按 <label> 标签文字
```

### 3. get_by_text / get_by_alt_text

```python
page.get_by_text("欢迎使用")             # 按页面可见文本
page.get_by_alt_text("公司 Logo")        # 按图片 alt 属性
```

### 4. get_by_test_id

需要开发在元素上加 `data-testid="xxx"`，最稳定。

```python
page.get_by_test_id("submit-btn")
```

### 5. locator (CSS 选择器)

灵活但容易因页面结构变化失效。

```python
page.locator(".login-form input")        # class 下的 input
page.locator("#username")                # id 定位
page.locator("div.container > p")        # 直接子元素
page.locator("input[name='email']")      # 按 name 属性
page.locator("[placeholder='验证码']")   # 按任意属性
```

### 6. locator (XPath)

适合复杂结构，可读性差，不推荐。

```python
page.locator("xpath=//div[@class='form']/input[1]")
page.locator("xpath=..")                 # 父元素
```

---

## 二、常用操作

### 导航

```python
page.goto("https://example.com", wait_until="domcontentloaded")  # 打开页面
page.reload()                                                    # 刷新
page.go_back()                                                   # 后退
page.go_forward()                                                # 前进
```

### 等待

```python
page.wait_for_selector(".result")           # 等元素出现
page.wait_for_url("**/success")             # 等 URL 匹配
page.wait_for_load_state("networkidle")     # 等网络空闲
```

### 输入

```python
page.fill("[placeholder='账号']", "admin")  # 清空后输入
page.type("[placeholder='账号']", "admin")  # 逐字输入（模拟键盘）
page.press("Enter")                         # 按键
```

### 下拉选择框

**原生 `<select>`**：
```python
page.select_option("#country", "中国")           # 按值选择
page.select_option("#country", label="中国")     # 按文字选择
page.select_option("#country", index=2)          # 按索引选择
```

**Element UI / Ant Design 等框架的下拉框**（底层不是原生 `<select>`）：
```python
# 1. 点击打开下拉菜单
page.get_by_placeholder("状态（全部）").click()

# 2. 选择选项
page.get_by_role("option", name="启用").click()

# 如果选项不在可见区域，可能需要滚动
page.get_by_role("listbox").locator("[role='option']").last.scroll_into_view_if_needed()
```

**常见框架下拉框的 role 映射**：
| 组件 | role |
|------|------|
| 下拉框本体 | `combobox` |
| 下拉列表容器 | `listbox` |
| 单个选项 | `option` |

### 断言

```python
assert page.get_by_text("成功").is_visible()    # 元素可见
assert page.url.endswith("/dashboard")          # URL 检查
assert page.title() == "MDM 后台"               # 标题检查
```

### 提取内容

```python
text = page.locator(".result").text_content()   # 提取文本
value = page.locator("#total").input_value()    # 提取输入框值
```

### 截图

```python
page.screenshot(path="screenshots/result.png")                  # 整页
page.locator(".table").screenshot(path="screenshots/table.png") # 单个元素
```

---

## 三、与 Playwright 无关但常用的操作

```python
import time
time.sleep(2)                        # 强制等待（不推荐，优先用 wait_for_*）

from playwright.sync_api import expect
expect(page.locator(".result")).to_be_visible()   # 自动重试的断言（推荐）
```
