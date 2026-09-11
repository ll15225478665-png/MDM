"""
按模块记录日志的测试示例
展示如何使用 TestLogger.get_module_logger() 创建模块专属日志 + @capture_exceptions 异常捕获
"""
from playwright.sync_api import expect
from utils.toolkit import capture_exceptions
from utils.test_logger import logger
@capture_exceptions
def test_role_with_module_logging(page, env_config):
    """
    测试角色管理页面（使用模块专属日志 + 自动异常捕获）
    
    功能：
      1. 自动登录后导航到角色管理页面
      2. 验证页面加载正确（多维度断言）
      3. 生成独立的模块日志文件
    
    生成的文件：
      - logs/role/role_YYYYMMDD_HHMMSS.log （模块专属日志）
      - screenshots/role/failed_xxx.png （如果失败，自动截图）
    """
    # 获取模块专属 logger（自动保存到 logs/role/ 目录）
    module_logger = logger.get_module_logger("role")
    module_logger.info("=" * 60)
    module_logger.info("🧪 [角色模块] 开始测试: 角色管理页面加载")
    module_logger.info("=" * 60)
    
    # auto_login 已完成登录，等待 Dashboard 菜单可见
    logger.step(1, "等待侧边栏菜单加载")
    expect(page.locator(".el-menu").first).to_be_visible(timeout=10000)
    logger.element_action("检查", ".el-menu", visible=True)
    
    # 展开系统管理菜单
    logger.step(2, "展开系统管理菜单")
    page.get_by_role("menuitem", name="系统管理").click()
    logger.element_action("点击", "系统管理菜单")
    
    # 等待"角色"子菜单出现
    logger.step(3, "等待角色子菜单出现")
    page.get_by_role("menuitem", name="角色").wait_for()
    logger.element_action("等待", "角色菜单", visible=True)
    
    # 点击角色
    logger.step(4, "点击角色菜单项")
    page.get_by_role("menuitem", name="角色").click()
    logger.element_action("点击", "角色菜单")
    
    # 等待 URL 变化
    logger.step(5, "验证页面跳转")
    page.wait_for_function("window.location.href.includes('/system/role')", timeout=10000)
    logger.navigation(page.url, "角色管理页面")
    
    # ===== 多维度断言验证页面加载正确 =====
    
    # 断言 1: URL 正确
    logger.step(6, "验证 URL 包含 /system/role")
    assert "/system/role" in page.url
    logger.assertion("URL 正确", "包含 /system/role", page.url, passed=True)
    
    # 断言 2: 表格加载完成
    logger.step(7, "验证数据表格可见")
    expect(page.locator(".el-table")).to_be_visible(timeout=10000)
    logger.element_action("检查", ".el-table", visible=True)
    
    # 断言 3: 表格列头完整（使用 exact=True 精确匹配）
    logger.step(8, "验证表格列头")
    headers = ["企业", "角色名", "备注", "创建时间", "操作"]
    for header in headers:
        expect(page.get_by_text(header, exact=True)).to_be_visible()
        logger.assertion(f"列头 '{header}' 可见", "visible", "visible", passed=True)
    
    # 断言 4: 关键按钮存在
    logger.step(9, "验证操作按钮")
    expect(page.get_by_role("button", name="添加角色")).to_be_visible()
    logger.element_action("检查", "添加角色按钮", visible=True)
    
    # 断言 5: 左侧菜单高亮（验证导航状态）
    logger.step(10, "验证菜单高亮状态")
    expect(page.locator(".el-menu-item.is-active")).to_contain_text("角色")
    logger.assertion("菜单项高亮", "包含'角色'", "包含'角色'", passed=True)
    
    # 断言 6: 搜索框存在
    logger.step(11, "验证搜索功能")
    expect(page.get_by_placeholder("角色名")).to_be_visible()
    logger.element_action("检查", "搜索框", visible=True)
    
    # 断言 7: 分页器默认值正确
    logger.step(12, "验证分页器")
    page_size_select = page.get_by_placeholder("请选择")
    expect(page_size_select).to_be_visible(timeout=5000)
    expect(page_size_select).to_have_value("10条/页", timeout=5000)
    logger.assertion("分页器默认值", "10条/页", "10条/页", passed=True)
    
    module_logger.info("=" * 60)
    module_logger.info("✅ [角色模块] 所有测试步骤通过")
    module_logger.info("=" * 60)
