from utils.toolkit import capture_exceptions


@capture_exceptions
def test_login_verification(page, env_config):
    """验证自动登录是否成功，检查是否跳转到首页 Dashboard"""
    # auto_login fixture 已经完成了登录，这里验证登录后的状态
    page.wait_for_timeout(2000)
    current_url = page.url
    title = page.title()
    # 验证 URL 包含 Dashboard（登录成功后应跳转到首页）
    assert "Dashboard" in current_url or "dashboard" in current_url, (
        f"登录失败：当前 URL 为 '{current_url}'，期望包含 Dashboard"
    )
    # 验证页面标题非空
    assert title and title.strip(), "登录失败：页面标题为空"
    print("✅ Login verified — test passed")
