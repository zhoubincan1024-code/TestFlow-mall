# -*- coding: utf-8 -*-
"""登录页 POM：mall-admin-web normal/login/index.vue"""
from selenium.webdriver.common.by import By

from config import LOGIN_URL
from pages.base_page import BasePage

USERNAME_INPUT = (By.CSS_SELECTOR, 'input[name="username"]')
PASSWORD_INPUT = (By.CSS_SELECTOR, 'input[name="password"]')
LOGIN_BUTTON = (By.XPATH, '//button[contains(@class,"el-button--primary") and contains(.,"登录")]')
FORM_ERROR = (By.CSS_SELECTOR, ".el-form-item__error")
TITLE = (By.CSS_SELECTOR, "h2.login-title")


class LoginPage(BasePage):
    def open(self):
        self.driver.get(LOGIN_URL)
        self.wait.until(lambda d: "login" in d.current_url)
        return self

    def login(self, username: str, password: str):
        self.input_text(USERNAME_INPUT, username)
        self.input_text(PASSWORD_INPUT, password)
        self.click(LOGIN_BUTTON)
        return self

    def is_on_login_page(self) -> bool:
        return "login" in self.current_url()

    def get_form_error(self, timeout: int = 6) -> str:
        """等待并返回表单校验错误消息（EP 校验消息异步渲染）"""
        from selenium.webdriver.support.ui import WebDriverWait
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: any(e.text for e in d.find_elements(*FORM_ERROR))
            )
        except Exception:
            pass
        els = self.driver.find_elements(*FORM_ERROR)
        return " | ".join(e.text for e in els if e.text)

    def has_login_button(self) -> bool:
        return self.is_visible(LOGIN_BUTTON)
