# MDM 测试框架 - 异常处理完整指南

## 📋 异常处理工具总览

### ✅ **已有的异常捕获工具**

| 工具 | 位置 | 用途 | 推荐使用场景 |
|------|------|------|------------|
| `@capture_exceptions` | `utils/toolkit.py` | 自动捕获测试函数异常 + 截图 | **所有测试函数**（必用） |
| 手动 `try-except` | Python 内置 | 局部处理非关键异常 | 可选步骤、重试逻辑 |
| `expect()` 自动重试 | Playwright | 元素等待断言 | **所有元素断言**（推荐） |
| `logger.error()` | `utils/test_logger.py` | 记录错误日志 | 配合 try-except 使用 |

---

## 🎯 方法 1: `@capture_exceptions` 装饰器（强烈推荐）

### **核心优势**
- ✅ **零侵入** - 只需加一行代码
- ✅ **自动截图** - 失败时保存现场
- ✅ **按模块分类** - 截图保存到 `screenshots/<module>/`
- ✅ **详细日志** - 错误信息完整记录
- ✅ **重新抛出** - pytest 能正确标记失败

### **使用方式**

```python
from utils.toolkit import capture_exceptions

@capture_exceptions
def test_my_feature(page, env_config):
    # 如果这里抛出任何异常，装饰器会自动：
    # 1. 记录错误日志
    # 2. 保存截图到 screenshots/<module>/failed_test_name_timestamp.png
    # 3. 重新抛出异常（pytest 标记为 FAILED）
    
    page.goto("https://xxx.com")
    assert "Expected" in page.title()
```

### **工作原理**

```python
# 伪代码展示内部逻辑
def capture_exceptions(test_func):
    def wrapper(*args, **kwargs):
        page = extract_page_from_args(args, kwargs)  # 提取 page 对象
        try:
            return test_func(*args, **kwargs)  # 执行测试
        except Exception as e:
            logger.error(f"测试失败: {e}")  # 记录日志
            
            if page:
                module_name = extract_module_from_file(test_func)  # 提取模块名
                take_screenshot(page, f"failed_{test_func.__name__}", module_name)  # 截图
            
            raise  # 重新抛出异常（让 pytest 标记为失败）
    
    return wrapper
```

### **实际效果**

**测试成功**:
```
TestCase/role/test_xxx.py::test_xxx PASSED [100%]
```

**测试失败**:
```
TestCase/role/test_xxx.py::test_xxx FAILED [100%]

❌ 测试 'test_xxx' 失败: TimeoutError: Timeout 5000ms exceeded.
📸 截图已保存: D:\mdm\screenshots\role\failed_test_xxx_20260910_142732.png
```

---

## 🔧 方法 2: 手动 `try-except`（局部处理）

### **适用场景**
- ⚠️ **非关键步骤** - 失败不应该导致整个测试失败
- 🔄 **重试逻辑** - 需要多次尝试的操作
- 🔍 **可选验证** - 存在与否不影响核心功能

### **基本用法**

```python
@capture_exceptions
def test_with_optional_steps(page, env_config):
    # ===== 关键步骤：不使用 try-except =====
    page.goto(env_config.base_url)
    expect(page.locator(".login-form")).to_be_visible()
    
    # ===== 非关键步骤：使用 try-except =====
    try:
        # 假设这个弹窗可能不存在，但不影响核心功能
        optional_popup = page.get_by_text("欢迎提示")
        if optional_popup.is_visible():
            optional_popup.get_by_role("button", name="关闭").click()
            logger.info("✅ 关闭了可选弹窗")
    except Exception as e:
        logger.warning(f"⚠️ 未找到可选弹窗（正常）: {e}")
        # 注意：这里不 raise，测试继续执行
    
    # 核心功能继续
    page.fill("#username", "admin")
    page.fill("#password", "123456")
    page.click("button:has-text('登录')")
```

### **重试逻辑示例**

```python
@capture_exceptions
def test_with_retry(page, env_config):
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            # 尝试点击一个可能还没加载的按钮
            button = page.get_by_role("button", name="提交")
            button.wait_for(state="visible", timeout=2000)
            button.click()
            logger.info(f"✅ 第 {attempt + 1} 次尝试成功")
            break  # 成功后退出循环
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"⚠️ 第 {attempt + 1} 次失败，继续重试: {e}")
            else:
                logger.error(f"❌ 重试 {max_retries} 次后仍然失败")
                raise  # 最后一次失败，抛出异常
```

### **条件验证示例**

```python
@capture_exceptions
def test_conditional_check(page, env_config):
    # 检查某个功能是否启用
    try:
        premium_feature = page.get_by_text("高级功能")
        if premium_feature.is_visible():
            logger.info("✅ 高级功能已启用")
            # 执行高级功能的测试
            premium_feature.click()
            ...
        else:
            logger.info("ℹ️ 高级功能未启用（跳过相关测试）")
    except Exception as e:
        logger.warning(f"⚠️ 无法检测高级功能状态: {e}")
        # 不 raise，继续测试其他功能
```

---

## 🎯 方法 3: `expect()` 自动重试（Playwright 最佳实践）

### **为什么用 `expect()` 而不是 `assert`？**

| 特性 | `assert element.is_visible()` | `expect(element).to_be_visible()` |
|------|-------------------------------|-----------------------------------|
| 重试机制 | ❌ 立刻判断，不重试 | ✅ **自动重试**，直到超时 |
| 动态页面 | ❌ 容易误报 | ✅ 等待元素出现 |
| 错误提示 | ❌ 简单 | ✅ 详细（等待时长、当前状态） |
| 超时控制 | ❌ 需手动 sleep | ✅ 内置 timeout 参数 |

### **推荐用法**

```python
from playwright.sync_api import expect

@capture_exceptions
def test_with_expect(page, env_config):
    # ✅ 推荐：自动重试，最多等 5 秒
    expect(page.locator(".el-table")).to_be_visible(timeout=5000)
    
    # ✅ 推荐：带自定义超时
    expect(page.get_by_role("button", name="提交")).to_be_enabled(timeout=10000)
    
    # ✅ 推荐：文本内容断言
    expect(page.locator(".success-message")).to_contain_text("操作成功")
    
    # ❌ 不推荐：没有重试机制
    assert page.locator(".el-table").is_visible()
```

### **常用 `expect()` 断言**

```python
# 可见性
expect(element).to_be_visible()
expect(element).to_be_hidden()

# 启用状态
expect(element).to_be_enabled()
expect(element).to_be_disabled()

# 文本内容
expect(element).to_contain_text("部分文本")
expect(element).to_have_text("完整文本")

# 属性值
expect(element).to_have_attribute("href", "/some-url")
expect(element).to_have_value("输入框的值")

# 数量
expect(page.locator(".item")).to_have_count(5)

# CSS 类
expect(element).to_have_class("active selected")
```

---

## 📊 异常处理决策树

```
测试中遇到可能的异常
│
├─ 是关键步骤吗？（失败则测试无意义）
│   ├─ ✅ 是 → 不加 try-except，让 @capture_exceptions 处理
│   │         使用 expect() 自动重试
│   │
│   └─ ❌ 否 → 是非关键步骤吗？（可选验证、重试逻辑）
│       ├─ ✅ 是 → 使用 try-except 捕获，记录 warning 日志
│       │         不 raise，继续执行
│       │
│       └─ ❌ 不确定 → 默认当作关键步骤，不加 try-except
```

---

## 💡 最佳实践总结

### ✅ **应该做的**

1. **所有测试函数都加 `@capture_exceptions`**
   ```python
   @capture_exceptions
   def test_xxx(page, env_config):
       ...
   ```

2. **优先使用 `expect()` 而非 `assert`**
   ```python
   expect(page.locator(".btn")).to_be_visible()  # ✅
   # assert page.locator(".btn").is_visible()     # ❌
   ```

3. **非关键步骤用 try-except + warning 日志**
   ```python
   try:
       optional_step()
   except Exception as e:
       logger.warning(f"可选步骤失败（已忽略）: {e}")
   ```

4. **关键步骤不加 try-except**
   ```python
   # 登录失败应该让测试立即失败
   page.fill("#username", username)
   page.fill("#password", password)
   page.click("button:has-text('登录')")
   ```

### ❌ **不应该做的**

1. **不要捕获所有异常并静默忽略**
   ```python
   try:
       critical_step()
   except:
       pass  # ❌ 危险！隐藏了真正的错误
   ```

2. **不要在 `@capture_exceptions` 后再加一层 try-except**
   ```python
   @capture_exceptions
   def test_xxx(page, env_config):
       try:
           ...  # ❌ 多余
       except Exception as e:
           logger.error(e)
           raise
   ```

3. **不要用 `time.sleep()` 替代 `expect()`**
   ```python
   time.sleep(3)  # ❌ 固定等待，浪费时间
   expect(element).to_be_visible(timeout=3000)  # ✅ 智能等待
   ```

---

## 🔍 故障排查

### 问题 1: 测试失败了但没有截图

**检查**:
1. 是否加了 `@capture_exceptions` 装饰器？
2. `page` 对象是否正确传递？
3. 是否有权限写入 `screenshots/` 目录？

**解决**:
```python
@capture_exceptions  # ✅ 确保有这一行
def test_xxx(page, env_config):
    ...
```

### 问题 2: try-except 捕获了异常但测试还是失败了

**原因**: `@capture_exceptions` 会重新抛出异常

**解决**: 这是预期行为。如果不想让测试失败，应该在 try-except 中**不 raise**：
```python
try:
    optional_step()
except Exception as e:
    logger.warning(f"已忽略: {e}")
    # 不要 raise ← 这样测试会继续
```

### 问题 3: expect() 超时了怎么办？

**检查**:
1. 选择器是否正确？
2. 元素是否真的会出现？
3. timeout 是否太短？

**解决**:
```python
# 增加超时时间
expect(element).to_be_visible(timeout=10000)  # 从默认 5s 增加到 10s

# 或者改用 wait_for
element.wait_for(state="visible", timeout=10000)
```

---

## 📚 完整示例对比

### ❌ **不好的做法**

```python
def test_bad_example(page, env_config):  # ❌ 没有 @capture_exceptions
    page.goto(env_config.base_url)
    
    # ❌ 用 assert 而非 expect
    assert page.locator(".login-form").is_visible()
    
    # ❌ 用 sleep 替代等待
    time.sleep(3)
    
    # ❌ 捕获所有异常并静默忽略
    try:
        page.click("button:has-text('登录')")
    except:
        pass
    
    # ❌ 没有日志记录
    assert page.url == "/dashboard"
```

### ✅ **推荐的做法**

```python
from utils.toolkit import capture_exceptions
from utils.test_logger import logger
from playwright.sync_api import expect

@capture_exceptions  # ✅ 自动异常捕获 + 截图
def test_good_example(page, env_config):
    logger.info("开始测试登录流程")
    
    # ✅ 导航
    page.goto(env_config.base_url)
    logger.navigation(page.url, "登录页")
    
    # ✅ 使用 expect 自动重试
    expect(page.locator(".login-form")).to_be_visible(timeout=5000)
    logger.info("✅ 登录表单可见")
    
    # ✅ 填写表单
    page.fill("#username", env_config.username)
    page.fill("#password", env_config.password)
    logger.step(1, "填写登录信息")
    
    # ✅ 点击登录（关键步骤，不加 try-except）
    page.click("button:has-text('登录')")
    logger.step(2, "点击登录按钮")
    
    # ✅ 等待跳转
    page.wait_for_function("window.location.href.includes('/Dashboard')", timeout=10000)
    logger.info("✅ 登录成功，跳转到 Dashboard")
    
    # ✅ 验证登录后的页面
    expect(page.locator(".dashboard")).to_be_visible(timeout=5000)
    logger.assertion("Dashboard 可见", "visible", "visible", passed=True)
```

---

## 🎯 快速参考卡片

```python
# ========== 导入 ==========
from utils.toolkit import capture_exceptions
from utils.test_logger import logger
from playwright.sync_api import expect

# ========== 测试函数模板 ==========
@capture_exceptions
def test_my_feature(page, env_config):
    module_logger = logger.get_module_logger("my_module")
    
    # 关键步骤：不加 try-except
    page.goto(env_config.base_url)
    expect(page.locator(".target")).to_be_visible()
    
    # 非关键步骤：加 try-except
    try:
        optional_step()
    except Exception as e:
        module_logger.warning(f"已忽略: {e}")
    
    # 重试逻辑
    for attempt in range(3):
        try:
            retryable_step()
            break
        except:
            if attempt == 2:
                raise

# ========== 常用断言 ==========
expect(element).to_be_visible()
expect(element).to_have_text("xxx")
expect(element).to_be_enabled()
expect(page.locator(".item")).to_have_count(5)
```

---

**最后更新**: 2026-09-10  
**版本**: v1.0  
**维护者**: MDM QA Team
