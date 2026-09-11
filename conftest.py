# -*- coding: utf-8 -*-
"""
conftest.py — pytest 全局配置文件
===================================

pytest 运行时会**自动加载** conftest.py 里的 fixture（夹具）。
fixture 就是"准备工作"——比如启动浏览器、加载配置、自动登录等。
测试用例不需要自己写这些代码，直接在参数里"要"就能拿到。
"""

import os
import sys
from pathlib import Path

import pytest
import yaml
import os
from types import SimpleNamespace
from playwright.sync_api import sync_playwright
from ddddocr import DdddOcr
# 🎯 在这里切换环境
CURRENT_ENV = "test"  # 可选: "dev", "test", "prod"

def _resolve_env_vars(value):
    """如果值是 ${VAR} 格式，则从系统环境变量中获取"""
    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
        var_name = value[2:-1]
        return os.getenv(var_name, "")
    return value

def _load_env_config(env_name: str = CURRENT_ENV):
    """从 config/env.yaml 读取环境配置"""
    config_path = None
    for parent in [Path(__file__).resolve()] + list(Path(__file__).resolve().parents):
        candidate = parent / "config" / "env.yaml"
        if candidate.is_file():
            config_path = str(candidate)
            break
    if not config_path:
        raise FileNotFoundError("❌ 未找到 'env.yaml' 配置文件！")
    with open(config_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if "environments" not in data:
        raise KeyError(" env.yaml 中缺少 'environments' 根节点")
    if env_name not in data["environments"]:
        raise ValueError(f"❌ 未知环境 '{env_name}'")
    
    config_dict = data["environments"][env_name]
    config_dict["name"] = env_name
    
    # 处理用户名和密码的占位符
    config_dict["username"] = _resolve_env_vars(config_dict.get("username"))
    config_dict["password"] = _resolve_env_vars(config_dict.get("password"))
    
    return SimpleNamespace(**config_dict)
@pytest.fixture(scope="session")
def env_config():
    """环境配置，所有测试共享"""
    return _load_env_config(CURRENT_ENV)
@pytest.fixture(scope="session")
def browser():
    """启动 Chromium 浏览器（整个测试运行期间只启动一次）"""
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(
        headless=False,
        args=[
            "--window-size=1920,1080",
            "--disable-dev-shm-usage",
            "--no-sandbox",
            "--force-device-scale-factor=1",
            "--disable-background-timer-throttling",
            "--disable-renderer-backgrounding",
            "--no-proxy-server",  # 禁用代理，避免网络超时
        ]
    )
    yield browser

    # DEBUG 模式或 PyCharm 运行时：按 Enter 才关闭浏览器
    if os.getenv("DEBUG") or os.getenv("PYCHARM_HOSTED"):
        try:
            input("\n 浏览器保持打开，按 Enter 关闭...\n")
        except (EOFError, OSError):
            pass

    browser.close()
    playwright.stop()

@pytest.fixture(scope="session")
def page(browser):
    """
    在浏览器中打开一个页面（所有测试共用）。
    如果测试之间互相干扰，把 scope 改为 "function"。
    """
    context = browser.new_context(
        ignore_https_errors=True,
        viewport={"width": 1920, "height": 1080},
        device_scale_factor=1,
        is_mobile=False,
        has_touch=False,
    )
    page_instance = context.new_page()

    # 隐藏滚动条
    page_instance.add_init_script("""
        const style = document.createElement('style');
        style.textContent = 'body{overflow:hidden!important;scrollbar-width:none}';
        document.head.appendChild(style);
    """)

    yield page_instance

@pytest.fixture(scope="session", autouse=True)
def auto_login(page, env_config):
    """
    自动登录（autouse=True 表示所有测试自动执行）。

    流程: 打开登录页 → OCR 识别验证码 → 填入表单 → 点击登录 → 验证跳转
    最多重试 3 次。
    """
    username = env_config.username
    password = env_config.password
    max_retries = 3
    ocr = DdddOcr(show_ad=False)  # 只初始化一次

    print(f"[LOGIN] 自动登录: {username} @ {env_config.name}")

    for attempt in range(1, max_retries + 1):
        try:
            # 使用 domcontentloaded 而非 load，避免等待所有资源加载完成导致超时
            page.goto(env_config.base_url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_selector("button:has-text('登录')", timeout=15000)

            # 定位验证码图片
            captcha_img = page.locator(".captcha_append img.el-image__inner")
            captcha_img.wait_for(state="visible", timeout=8000)

            # OCR 识别（最多 4 次，每次刷新验证码）
            captcha_text = ""
            for ocr_attempt in range(1, 5):
                if ocr_attempt > 1:
                    captcha_img.click()
                    captcha_img.wait_for(state="visible", timeout=3000)
                    page.wait_for_timeout(500)

                # 直接截取 img 元素本身（更小更快，超时 10 秒）
                img_bytes = captcha_img.screenshot(timeout=10000)
                captcha_text = ocr.classification(img_bytes).strip().lower()

                if len(captcha_text) == 4 and captcha_text.isalnum():
                    break

            # 填充表单并登录
            page.fill("[placeholder='用户名']", username)
            page.fill("[placeholder='密码']", password)
            page.fill("[placeholder='请输入验证码']", captcha_text)
            page.get_by_role("button", name="登录").click(timeout=8000)
            page.wait_for_timeout(3000)

            # 验证是否离开登录页
            if "/Login" not in page.url:
                # 等待 Dashboard 页面加载稳定（用 URL 判断更可靠）
                page.wait_for_function("window.location.href.includes('/Dashboard')", timeout=10000)
                print("✅ 登录成功")
                return

        except Exception as e:
            if attempt == max_retries:
                print(f" 登录失败: {e}")
                raise
            page.wait_for_timeout(1000)


# ==============================
# HTMLTestRunner 集成
# ==============================
from utils.htmltestrunner_integration import pytest_runtest_logreport, pytest_sessionfinish

