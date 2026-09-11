# MDM 测试框架 - 按模块组织日志和截图

## 📊 功能概览

### ✅ **已实现：按模块自动分类**

#### 1️⃣ **日志文件按模块组织**

**目录结构**:
```
logs/
├── test_20260910_141526.log          # 全局日志（所有测试）
├── test_20260910_142049.log          # 全局日志（所有测试）
├── role/                              # ✨ 角色模块专属目录
│   └── role_20260910_142119.log      # 角色模块专属日志
├── user/                              # ✨ 用户模块专属目录（未来）
│   └── user_YYYYMMDD_HHMMSS.log
└── device/                            # ✨ 设备模块专属目录（未来）
    └── device_YYYYMMDD_HHMMSS.log
```

**使用方式**:
```python
from utils.test_logger import logger

@capture_exceptions
def test_my_feature(page, env_config):
    # 获取模块专属 logger（自动保存到 logs/<module>/ 目录）
    module_logger = logger.get_module_logger("role")  # 传入模块名
    
    module_logger.info("开始测试")
    module_logger.step(1, "打开页面")
    # ... 测试步骤
```

**优势**:
- ✅ 每个模块有独立的日志文件
- ✅ 便于排查特定模块的问题
- ✅ 日志文件名带时间戳，便于追溯
- ✅ 全局日志 + 模块日志双重记录

---

#### 2️⃣ **截图文件按模块组织**

**目录结构**:
```
screenshots/
├── failed_test_login_verification.png     # 旧截图（根目录）
├── role/                                   # ✨ 角色模块专属目录
│   └── failed_test_role_successful_20260910_142119.png  # 带时间戳
├── user/                                   # ✨ 用户模块专属目录（未来）
│   └── failed_test_xxx_YYYYMMDD_HHMMSS.png
└── device/                                 # ✨ 设备模块专属目录（未来）
    └── failed_test_xxx_YYYYMMDD_HHMMSS.png
```

**自动提取模块名**:
- `@capture_exceptions` 装饰器会自动从测试文件路径提取模块名
- 例如：`TestCase/role/test_role_susscifl.py` → 模块名 = `"role"`
- 失败截图自动保存到 `screenshots/role/` 目录

**使用方式**:
```python
# 无需手动指定模块名，装饰器自动处理
@capture_exceptions
def test_role_susscifl(page, env_config):
    # 如果测试失败，截图自动保存到 screenshots/role/
    ...
```

**手动指定模块名**（可选）:
```python
from utils.toolkit import Utils

def test_custom(page):
    try:
        # 测试代码
        pass
    except Exception as e:
        # 手动保存截图并指定模块名
        Utils.take_screenshot(page, "failed_test", test_module="role")
```

**优势**:
- ✅ 截图按模块分类，便于查找
- ✅ 文件名带时间戳，避免覆盖
- ✅ 报告中可直接链接到对应模块的截图
- ✅ 便于清理旧截图（按模块批量删除）

---

## 🎯 完整示例

### 测试文件：`TestCase/role/test_role_module_logging.py`

```python
from playwright.sync_api import expect
from utils.toolkit import capture_exceptions
from utils.test_logger import logger


@capture_exceptions
def test_role_with_module_logging(page, env_config):
    """
    测试角色管理页面（使用模块专属日志）
    
    此测试会生成独立的模块日志文件：
    logs/role/role_YYYYMMDD_HHMMSS.log
    """
    # 获取模块专属 logger
    role_logger = logger.get_module_logger("role")
    
    role_logger.info("=" * 60)
    role_logger.info("🧪 [角色模块] 开始测试: 角色管理页面加载")
    role_logger.info("=" * 60)
    
    # 测试步骤...
    role_logger.info("[步骤 1] 等待侧边栏菜单加载")
    expect(page.locator(".el-menu").first).to_be_visible(timeout=10000)
    
    # ... 更多步骤
    
    role_logger.info("✅ [角色模块] 所有测试步骤通过")
```

### 运行测试

```bash
pytest TestCase/role/test_role_module_logging.py -v
```

### 生成的文件

**日志文件**:
- `logs/test_20260910_142049.log` - 全局日志（包含所有测试）
- `logs/role/role_20260910_142119.log` - 角色模块专属日志

**截图文件**（如果失败）:
- `screenshots/role/failed_test_role_module_logging_20260910_142119.png`

---

## 📋 最佳实践

### 1. 为新模块创建专属 logger

```python
# 在测试文件顶部
from utils.test_logger import logger

# 在测试函数中获取模块 logger
def test_user_management(page, env_config):
    user_logger = logger.get_module_logger("user")  # 用户模块
    user_logger.info("开始测试用户管理")
    
def test_device_activation(page, env_config):
    device_logger = logger.get_module_logger("device")  # 设备模块
    device_logger.info("开始测试设备激活")
```

### 2. 日志级别选择

| 级别 | 用途 | 示例 |
|------|------|------|
| `DEBUG` | 调试信息、元素状态 | `logger.debug("按钮可见性: True")` |
| `INFO` | 测试步骤、断言结果 | `logger.info("[步骤 1] 打开页面")` |
| `WARNING` | 非致命警告 | `logger.warning("网络较慢，但不影响测试")` |
| `ERROR` | 测试失败、异常 | `logger.error("测试失败", exc_info=True)` |

### 3. 查看日志

**查看所有日志**:
```bash
# 全局日志
type logs\test_*.log

# 模块日志
type logs\role\role_*.log
```

**实时跟踪日志**（Windows PowerShell）:
```powershell
Get-Content logs\role\role_*.log -Wait -Tail 10
```

### 4. 清理旧日志和截图

**建议保留策略**:
- 保留最近 7 天的日志
- 保留最近 30 天的截图
- 按模块定期清理

**清理脚本示例**:
```bash
# 删除 7 天前的日志
forfiles /p "logs" /s /m *.log /d -7 /c "cmd /c del @path"

# 删除 30 天前的截图
forfiles /p "screenshots" /s /m *.png /d -30 /c "cmd /c del @path"
```

---

## 🔍 故障排查

### 问题 1: 找不到模块日志文件

**检查**:
1. 是否调用了 `logger.get_module_logger("模块名")`
2. 模块名是否正确（小写、无特殊字符）
3. 是否有写入权限

**解决**:
```python
# 确保在测试函数中调用
role_logger = logger.get_module_logger("role")  # ✅ 正确
```

### 问题 2: 截图没有按模块保存

**检查**:
1. 是否使用了 `@capture_exceptions` 装饰器
2. 测试文件路径是否正确（应在 `TestCase/<module>/` 下）
3. 装饰器是否能正确提取模块名

**解决**:
```python
# 确保测试文件在正确的目录下
# TestCase/role/test_xxx.py → 模块名 = "role" ✅

# 或者手动指定模块名
Utils.take_screenshot(page, "failed", test_module="role")
```

### 问题 3: 日志内容重复

**原因**: 同时使用了全局 logger 和模块 logger

**解决**:
```python
# 只使用模块 logger（推荐）
module_logger = logger.get_module_logger("role")
module_logger.info("...")

# 不要同时使用
logger.info("...")  # ❌ 避免
module_logger.info("...")  # ✅ 推荐
```

---

## 📊 效果对比

### ❌ 之前（未按模块组织）

```
logs/
└── test_20260910_141526.log  # 所有测试混在一起

screenshots/
├── failed_test_role_xxx.png
├── failed_test_user_xxx.png
└── failed_test_device_xxx.png  # 所有截图混在一起
```

**问题**:
- ❌ 难以定位特定模块的日志
- ❌ 截图文件名相似，容易混淆
- ❌ 无法快速找到某个模块的所有失败案例

### ✅ 现在（按模块组织）

```
logs/
├── test_20260910_142049.log  # 全局日志
├── role/
│   └── role_20260910_142119.log  # 角色模块专属
├── user/
│   └── user_20260910_142200.log  # 用户模块专属
└── device/
    └── device_20260910_142300.log  # 设备模块专属

screenshots/
├── role/
│   └── failed_test_role_xxx_20260910_142119.png
├── user/
│   └── failed_test_user_xxx_20260910_142200.png
└── device/
    └── failed_test_device_xxx_20260910_142300.png
```

**优势**:
- ✅ 每个模块独立日志，便于排查
- ✅ 截图按模块分类，一目了然
- ✅ 文件名带时间戳，不会覆盖
- ✅ 便于统计各模块的失败率

---

## 🚀 未来扩展

### 1. 按日期进一步细分

```
logs/
├── 2026-09/
│   ├── 10/
│   │   ├── role/
│   │   │   └── role_142119.log
│   │   └── user/
│   │       └── user_142200.log
```

### 2. 自动生成模块测试报告

```python
# 统计每个模块的通过率
module_stats = {
    "role": {"total": 10, "passed": 8, "failed": 2},
    "user": {"total": 15, "passed": 15, "failed": 0},
}
```

### 3. 日志聚合分析

```python
# 分析所有模块的失败原因
failure_analysis = {
    "timeout": 5,
    "element_not_found": 3,
    "assertion_failed": 2,
}
```

---

**最后更新**: 2026-09-10  
**版本**: v1.1  
**维护者**: MDM QA Team
