# -*- coding: utf-8 -*-
"""
UI 测试全局 fixtures：
- driver：headless Chrome（webdriver-manager 自动管理 chromedriver），失败自动截图
- logged_in_driver：登录后的浏览器实例
"""
import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import config
from pages.login_page import LoginPage
from utils.logger import get_logger

logger = get_logger("ui")


def _make_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    if config.HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--window-size={config.BROWSER_WIDTH},{config.BROWSER_HEIGHT}")
    options.add_argument("--lang=zh-CN")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


@pytest.fixture(scope="function")
def driver():
    """每用例独立浏览器实例，失败自动截图到 ui-test/screenshots/"""
    d = _make_driver()
    yield d
    d.quit()


@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """登录 admin/macro123 后的浏览器实例"""
    LoginPage(driver).open().login(config.ADMIN_USERNAME, config.ADMIN_PASSWORD)
    # 等待跳转离开登录页
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    WebDriverWait(driver, config.WAIT_TIMEOUT).until(
        lambda d: "login" not in d.current_url, message="登录后未跳转出登录页"
    )
    logger.info("已登录: %s, url=%s", config.ADMIN_USERNAME, driver.current_url)
    return driver


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """失败用例自动截图"""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver is not None:
            os.makedirs(config.SCREENSHOT_DIR, exist_ok=True)
            path = os.path.join(config.SCREENSHOT_DIR, f"{item.name}.png")
            try:
                driver.save_screenshot(path)
                logger.info("失败截图已保存: %s", path)
            except Exception:
                pass
