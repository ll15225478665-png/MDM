#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MDM 测试日志记录工具
支持分级日志（INFO/WARNING/ERROR）、模块化分类、上下文信息记录
"""
import os
import sys
import logging
from datetime import datetime
from pathlib import Path


class TestLogger:
    """测试日志管理器"""
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup_logger()
        return cls._instance
    
    def _setup_logger(self):
        """配置日志记录器（按模块分文件）"""
        self._logger = logging.getLogger("MDM_TEST")
        self._logger.setLevel(logging.DEBUG)
        
        # 避免重复添加 handler
        if self._logger.handlers:
            return
        
        # 创建日志目录
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # 日志文件名（带时间戳 + 全局日志）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"test_{timestamp}.log"
        
        # 文件 Handler（详细日志 - 全局）
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            "%(asctime)s [%(levelname)-8s] %(name)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_format)
        
        # 控制台 Handler（简洁输出）
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%H:%M:%S"
        )
        console_handler.setFormatter(console_format)
        
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)
        
        self.log_file = str(log_file)
        self.module_loggers = {}  # 存储各模块的 logger
    
    def info(self, msg):
        """记录信息日志"""
        self._logger.info(msg)
    
    def warning(self, msg):
        """记录警告日志"""
        self._logger.warning(msg)
    
    def error(self, msg, exc_info=False):
        """记录错误日志"""
        self._logger.error(msg, exc_info=exc_info)
    
    def debug(self, msg):
        """记录调试日志"""
        self._logger.debug(msg)
    
    def step(self, step_num, description):
        """记录测试步骤"""
        self._logger.info(f"[步骤 {step_num}] {description}")
    
    def assertion(self, description, expected, actual, passed=True):
        """记录断言结果"""
        status = "✅ PASS" if passed else "❌ FAIL"
        msg = f"{status} | {description}\n  期望: {expected}\n  实际: {actual}"
        if passed:
            self._logger.info(msg)
        else:
            self._logger.error(msg)
    
    def navigation(self, url, title=""):
        """记录页面导航"""
        title_info = f" ({title})" if title else ""
        self._logger.info(f"🔗 导航到: {url}{title_info}")
    
    def element_action(self, action, element_name, visible=True):
        """记录元素操作"""
        visibility = "可见" if visible else "不可见"
        self._logger.debug(f"🖱️  {action} [{element_name}] ({visibility})")
    
    def screenshot_saved(self, path, reason=""):
        """记录截图保存"""
        reason_info = f" - {reason}" if reason else ""
        self._logger.info(f"📸 截图已保存: {path}{reason_info}")
    
    def get_log_file(self):
        """获取日志文件路径"""
        return self.log_file
    
    def get_module_logger(self, module_name: str):
        """
        获取模块专属的 logger（自动保存到独立文件）
        
        Args:
            module_name: 模块名（如 "role", "user", "device"）
        
        Returns:
            logging.Logger: 模块专属 logger
        """
        if module_name in self.module_loggers:
            return self.module_loggers[module_name]
        
        # 创建模块专属日志文件
        log_dir = Path("logs") / module_name
        log_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        module_log_file = log_dir / f"{module_name}_{timestamp}.log"
        
        # 创建模块 logger
        module_logger = logging.getLogger(f"MDM_TEST.{module_name}")
        module_logger.setLevel(logging.DEBUG)
        
        # 文件 Handler
        file_handler = logging.FileHandler(module_log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            "%(asctime)s [%(levelname)-8s] %(name)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_format)
        
        module_logger.addHandler(file_handler)
        module_logger.propagate = False  # 不传播到根 logger
        
        self.module_loggers[module_name] = module_logger
        self.info(f"📝 模块 '{module_name}' 日志文件: {module_log_file}")
        
        return module_logger


# 全局实例
logger = TestLogger()


# pytest 集成
def pytest_configure(config):
    """pytest 配置钩子"""
    # 将 logger 注入到 config
    config.test_logger = logger
    logger.info("=" * 80)
    logger.info("🚀 MDM Web UI 自动化测试启动")
    logger.info("=" * 80)


def pytest_runtest_logreport(report):
    """测试运行日志钩子"""
    if report.when == "call":
        if report.passed:
            logger.info(f"✅ 测试通过: {report.nodeid} ({report.duration:.2f}s)")
        elif report.failed:
            logger.error(f"❌ 测试失败: {report.nodeid} ({report.duration:.2f}s)")
            if hasattr(report, "longrepr"):
                logger.error(f"   错误详情: {str(report.longrepr)[:500]}")


def pytest_sessionfinish(session, exitstatus):
    """测试会话结束钩子"""
    test_logger = getattr(session.config, "test_logger", None)
    if test_logger:
        test_logger.info("=" * 80)
        test_logger.info(f"🏁 测试会话结束 - 退出码: {exitstatus}")
        test_logger.info(f"📄 完整日志文件: {test_logger.get_log_file()}")
        test_logger.info("=" * 80)
