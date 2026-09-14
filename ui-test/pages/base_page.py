# -*- coding: utf-8 -*-
"""
POM 页面对象基类：封装 Selenium 显式等待、输入、点击、断言辅助
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from config import WAIT_TIMEOUT


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, WAIT_TIMEOUT)

    # ---- 元素定位 ----
    def find(self, locator: tuple, timeout: int = WAIT_TIMEOUT):
        """等待元素可见并返回"""
        return WebDriverWait(self.driver, timeout).until(
            ec.visibility_of_element_located(locator), message=f"元素不可见: {locator}"
        )

    def find_all(self, locator: tuple, timeout: int = WAIT_TIMEOUT):
        WebDriverWait(self.driver, timeout).until(
            ec.presence_of_element_located(locator), message=f"元素不存在: {locator}"
        )
        return self.driver.find_elements(*locator)

    def wait_clickable(self, locator: tuple, timeout: int = WAIT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            ec.element_to_be_clickable(locator), message=f"元素不可点击: {locator}"
        )

    # ---- 操作 ----
    def input_text(self, locator: tuple, text: str):
        """输入文本：Ctrl+A 全选覆盖，避免 Element Plus 受控组件预填值导致拼接"""
        el = self.find(locator)
        el.send_keys(Keys.CONTROL, "a")
        el.send_keys(text)
        return el

    def click(self, locator: tuple):
        el = self.wait_clickable(locator)
        el.click()
        return el

    def get_text(self, locator: tuple) -> str:
        return self.find(locator).text.strip()

    def is_visible(self, locator: tuple, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                ec.visibility_of_element_located(locator)
            )
            return True
        except Exception:
            return False

    # ---- 页面状态 ----
    def current_url(self) -> str:
        return self.driver.current_url

    def title(self) -> str:
        return self.driver.title

    def screenshot(self, name: str):
        import os
        os.makedirs(os.path.dirname(name), exist_ok=True)
        self.driver.save_screenshot(name)
