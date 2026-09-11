# test_role_module_logging.py - 完整使用指南

## 📋 文件概览

**位置**: `TestCase/role/test_role_module_logging.py`

**功能**: 测试角色管理页面加载，展示如何使用：
1. ✅ `@capture_exceptions` 装饰器 - 自动异常捕获 + 截图
2. ✅ 模块专属日志 - 保存到 `logs/role/`
3. ✅ 多维度断言 - URL、表格、按钮、菜单高亮等

---

## 🎯 核心特性

### 1️⃣ **自动异常捕获**

```python
@capture_exceptions
def test_role_with_module_logging(page, env_config):
    ...
```

**效果**:
- ✅ 测试失败时自动保存截图到 `screenshots/role/failed_xxx_timestamp.png`
- ✅ 自动记录错误日志
- ✅ 重新抛出异常（pytest 标记为 FAILED）

### 2️⃣ **模块专属日志**

```python
# 获取模块专属 logger
module_logger = logger.get_module_logger("role")
module_logger.info("模块特定信息")
```

**生成的文件**:
- `logs/role/role_YYYYMMDD_HHMMSS.log` - 模块专属日志
- `logs/test_YYYYMMDD_HHMMSS.log` - 全局日志（包含所有测试的详细步骤）

### 3️⃣ **多维度断言**

```python
# 断言 1: URL 正确
assert "/system/role" in page.url

# 断言 2: 表格可见
expect(page.locator(".el-table")).to_be_visible(timeout=10000)

# 断言 3: 列头完整
expect(page.get_by_text("企业", exact=True)).to_be_visible()

# 断言 4: 按钮存在
expect(page.get_by_role("button", name="添加角色")).to_be_visible()

# 断言 5: 菜单高亮
expect(page.locator(".el-menu-item.is-active")).to_contain_text("角色")

# 断言 6: 搜索框存在
expect(page.get_by_placeholder("角色名")).to_be_visible()

# 断言 7: 分页器默认值
expect(page.get_by_placeholder("请选择")).to_have_value("10条/页")
```

---

## 📊 运行测试

### **标准运行**
```bash
pytest TestCase/role/test_role_module_logging.py -v
```

**输出**:
```
TestCase/role/test_role_module_logging.py::test_role_with_module_logging PASSED [100%]
1 passed in 37.36s
```

### **调试模式（浏览器保持打开）**
```bash
set DEBUG=1 && pytest TestCase/role/test_role_module_logging.py -v -s
```

---

## 📁 生成的文件

### **成功时**
```
logs/
├── test_20260910_143228.log          # 全局日志（详细步骤）
└── role/
    └── role_20260910_143228.log      # 模块日志（摘要）
```

### **失败时**
```
logs/
├── test_20260910_143228.log          # 全局日志
└── role/
    └── role_20260910_143228.log      # 模块日志

screenshots/
└── role/
    └── failed_test_role_with_module_logging_20260910_143228.png  # 失败截图
```

---

## 🔍 日志内容示例

### **模块日志 (`logs/role/role_*.log`)**
```
2026-09-10 14:32:28 [INFO] MDM_TEST.role:26 - ============================================================
2026-09-10 14:32:28 [INFO] MDM_TEST.role:27 - 🧪 [角色模块] 开始测试: 角色管理页面加载
2026-09-10 14:32:28 [INFO] MDM_TEST.role:28 - ============================================================
2026-09-10 14:32:31 [INFO] MDM_TEST.role:96 - ============================================================
2026-09-10 14:32:31 [INFO] MDM_TEST.role:97 - ✅ [角色模块] 所有测试步骤通过
2026-09-10 14:32:31 [INFO] MDM_TEST.role:98 - ============================================================
```

### **全局日志 (`logs/test_*.log`)**
```
2026-09-10 14:32:28 [INFO] MDM_TEST:84 - [步骤 1] 等待侧边栏菜单加载
2026-09-10 14:32:28 [DEBUG] MDM_TEST:103 - 🖱️  检查 [.el-menu] (可见)
2026-09-10 14:32:28 [INFO] MDM_TEST:84 - [步骤 2] 展开系统管理菜单
2026-09-10 14:32:28 [DEBUG] MDM_TEST:103 - 🖱️  点击 [系统管理菜单] (可见)
...
2026-09-10 14:32:28 [INFO] MDM_TEST:91 - ✅ PASS | URL 正确
  期望: 包含 /system/role
  实际: https://test-platform.easycontrol.io/mdm-web/system/role
...
```

---

## 💡 最佳实践

### ✅ **应该做的**

1. **所有测试函数都加 `@capture_exceptions`**
   ```python
   @capture_exceptions
   def test_my_feature(page, env_config):
       ...
   ```

2. **使用 `expect()` 而非 `assert`**
   ```python
   expect(element).to_be_visible()  # ✅ 自动重试
   assert element.is_visible()      # ❌ 无重试
   ```

3. **使用 `exact=True` 精确匹配**
   ```python
   page.get_by_text("企业", exact=True)  # ✅ 精确匹配
   page.get_by_text("企业")              # ❌ 可能匹配多个
   ```

4. **多维度断言**
   ```python
   # 验证页面加载正确，从 4 个维度断言：
   # 1. URL
   # 2. 关键元素（表格、按钮）
   # 3. 页面标题/列头
   # 4. 导航状态（菜单高亮）
   ```

### ❌ **不应该做的**

1. **不要在测试函数中手动 try-except 关键步骤**
   ```python
   try:
       critical_step()  # ❌ 隐藏了真正的错误
   except:
       pass
   ```

2. **不要用 `time.sleep()` 替代 `expect()`**
   ```python
   time.sleep(3)  # ❌ 固定等待
   expect(element).to_be_visible(timeout=3000)  # ✅ 智能等待
   ```

3. **不要忽略 `@capture_exceptions` 装饰器**
   ```python
   def test_without_decorator(page, env_config):  # ❌ 没有异常捕获
       ...
   
   @capture_exceptions  # ✅ 有异常捕获
   def test_with_decorator(page, env_config):
       ...
   ```

---

## 🔧 自定义扩展

### **为新模块创建类似测试**

```python
# 1. 在 TestCase/<module>/ 下创建测试文件
# 例如: TestCase/user/test_user_management.py

from utils.toolkit import capture_exceptions
from utils.test_logger import logger

@capture_exceptions
def test_user_management(page, env_config):
    # 获取模块专属 logger
    module_logger = logger.get_module_logger("user")
    module_logger.info("🧪 [用户模块] 开始测试")
    
    # 测试步骤...
    logger.step(1, "导航到用户管理页面")
    ...
    
    module_logger.info("✅ [用户模块] 所有测试步骤通过")
```

### **添加自定义断言**

```python
# 验证下拉框默认值
page_size_select = page.get_by_placeholder("请选择")
expect(page_size_select).to_be_visible()
expect(page_size_select).to_have_value("10条/页")

# 验证表格行数
expect(page.locator(".el-table__row")).to_have_count(10)

# 验证按钮禁用状态
expect(page.get_by_role("button", name="删除")).to_be_disabled()
```

---

## 📚 相关文档

- `docs/exception_handling.md` - 异常处理完整指南
- `docs/module_organization.md` - 按模块组织日志和截图
- `docs/testing_features.md` - 完整功能概览
- `QWEN.md` - 项目总览

---

**最后更新**: 2026-09-10  
**版本**: v1.0  
**维护者**: MDM QA Team
