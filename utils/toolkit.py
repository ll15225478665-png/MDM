# utils/toolkit.py
import logging
import os
import functools
from datetime import datetime  # 新增：用于时间戳
from typing import Callable, Optional
from playwright.sync_api import Page
from pathlib import Path

import os
import base64
import requests
from typing import Optional, Union

class Utils:
    """工具类：整合日志和截图功能"""

    @staticmethod
    def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
        logger = logging.getLogger(name)
        if not logger.handlers:
            logger.setLevel(level)
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s | %(name)-15s | %(levelname)-8s | %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.propagate = False
        return logger

    @staticmethod
    def take_screenshot(page: Page, name: str = "failure", test_module: str = "") -> str:
        """
        保存测试截图（按模块组织）
        
        Args:
            page: Playwright Page 对象
            name: 截图名称（通常是测试函数名）
            test_module: 测试模块名（如 "role", "user", "device"）
        
        Returns:
            截图文件的绝对路径
        """
        screenshot_dir = Path("screenshots")
        
        # 如果提供了模块名，创建子目录
        if test_module:
            module_dir = screenshot_dir / test_module
            module_dir.mkdir(parents=True, exist_ok=True)
            screenshot_dir = module_dir
        
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成安全的文件名
        safe_name = "".join(c if c.isalnum() or c in ('_', '-') else '_' for c in name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = screenshot_dir / f"{safe_name}_{timestamp}.png"
        
        page.screenshot(path=str(filepath), full_page=True)
        Utils.get_logger("Screenshot").info(f"📸 截图已保存: {filepath}")
        return str(filepath)

    @staticmethod
    def find_file(filename: str, start_path: Optional[str] = None) -> Optional[str]:
        """
        跨平台查找文件：从指定目录（默认项目根目录）递归搜索文件

        Args:
            filename (str): 要查找的文件名，例如 "config.yaml"
            start_path (str, optional): 搜索起始目录，默认为当前工作目录

        Returns:
            str or None: 找到则返回绝对路径，否则返回 None

        Example:
            path = Utils.find_file("config.yaml")
            if path:
                with open(path) as f: ...
        """
        logger = Utils.get_logger("FileFinder")

        # 默认从当前工作目录开始搜索
        if start_path is None:
            start_path = os.getcwd()

        start = Path(start_path).resolve()
        logger.debug(f"🔍 开始在 '{start}' 中搜索文件: '{filename}'")

        try:
            # 使用 pathlib 递归遍历（跨平台安全）
            for file_path in start.rglob(filename):
                if file_path.is_file():
                    abs_path = str(file_path.resolve())
                    logger.info(f"✅ 找到文件: {abs_path}")
                    return abs_path
        except PermissionError as e:
            logger.warning(f"⚠️ 权限不足，跳过某些目录: {e}")
        except Exception as e:
            logger.error(f"❌ 搜索过程中出错: {e}")

        logger.warning(f"❌ 未找到文件: '{filename}'")
        return None


# ==============================
# 装饰器：放在类外部（推荐！）
# ==============================

def capture_exceptions(test_func: Callable) -> Callable:
    """
    装饰器：为测试函数自动捕获异常、记录日志、保存截图（按模块组织）

    使用方式：
        from utils.toolkit import capture_exceptions

        @capture_exceptions
        def test_xxx(page):
            ...
    
    截图会自动保存到 screenshots/<module_name>/failed_<test_name>_<timestamp>.png
    """

    @functools.wraps(test_func)
    def wrapper(*args, **kwargs):
        # 尝试从参数中获取 page 对象
        page = None
        for arg in args:
            if isinstance(arg, Page):
                page = arg
                break
        if page is None:
            for value in kwargs.values():
                if isinstance(value, Page):
                    page = value
                    break

        logger = Utils.get_logger(test_func.__name__)
        try:
            return test_func(*args, **kwargs)
        except Exception as e:
            error_msg = f"❌ 测试 '{test_func.__name__}' 失败: {str(e)}"
            logger.error(error_msg)

            if page:
                # 自动提取模块名（从文件路径）
                test_module = ""
                try:
                    # 获取测试文件路径，例如 "TestCase/role/test_role_susscifl.py"
                    test_file = test_func.__code__.co_filename
                    # 提取模块名（倒数第二个目录名）
                    parts = Path(test_file).parts
                    if len(parts) >= 2:
                        # 找到 TestCase 后的第一个目录名作为模块名
                        for i, part in enumerate(parts):
                            if part == "TestCase" and i + 1 < len(parts):
                                test_module = parts[i + 1]
                                break
                except Exception:
                    pass
                
                screenshot_name = f"failed_{_test_proper_name(test_func.__name__)}"
                Utils.take_screenshot(page, screenshot_name, test_module)
            else:
                logger.warning("未找到 Page 对象，无法截图")

            raise  # 重新抛出异常

    return wrapper


def _test_proper_name(name: str) -> str:
    """辅助函数：生成安全的截图文件名"""
    return name.replace("[", "_").replace("]", "_").replace("::", "_")



# ================引入ai=======================
# API_KEY = os.getenv("DASHSCOPE_API_KEY", "sk-faf865cb62c44c57810569117fbfbf29")
# API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
#
#
# def image_to_base64(image_path: str) -> str:
#     """将本地图片转为 Base64"""
#     with open(image_path, "rb") as f:
#         encoded = base64.b64encode(f.read()).decode("utf-8")
#     ext = image_path.lower().split(".")[-1]
#     mime = "image/jpeg" if ext in ("jpg", "jpeg") else "image/png"
#     return f"data:{mime};base64,{encoded}"
#
#
# def ai_check_success(image_path: str) -> dict:
#     """
#     使用 AI 判断截图中是否包含“成功”提示
#
#     Args:
#         image_path: 截图路径
#
#     Returns:
#         dict: {"success": bool, "message": str}
#     """
#     image_url = image_to_base64(image_path)
#
#     headers = {
#         "Authorization": f"Bearer {API_KEY}",
#         "Content-Type": "application/json"
#     }
#
#     payload = {
#         "model": "qwen-vl-plus",
#         "messages": [
#             {
#                 "role": "user",
#                 "content": [
#                     {"image": image_url},
#                     {
#                         "text": "请判断页面上是否有‘成功’相关的提示信息（如：操作成功、创建成功、保存成功等）。如果有，请返回 true 并描述内容；如果没有，请返回 false。"}
#                 ]
#             }
#         ]
#     }
#
#     resp = requests.post(API_URL, headers=headers, json=payload)
#     if resp.status_code != 200:
#         raise RuntimeError(f"AI API error: {resp.text}")
#
#     result = resp.json()["choices"][0]["message"]["content"].strip()
#
#     # 解析 AI 回答
#     success = False
#     message = result
#
#     if "true" in result.lower() or "成功" in result:
#         success = True
#     elif "false" in result.lower() or "未找到" in result:
#         success = False
#
#     return {"success": success, "message": message}