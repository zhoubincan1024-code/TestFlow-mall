# -*- coding: utf-8 -*-
"""后台首页/布局 POM：侧边栏菜单、看板卡片"""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage

# 侧边栏菜单项（el-menu-item / el-sub-menu，按文本定位）
MENU_ITEM = lambda text: (By.XPATH, f'//*[contains(@class,"el-menu-item") or contains(@class,"el-sub-menu")]//span[text()="{text}"]')
# 菜单项容器（点击用）
MENU_ITEM_BOX = lambda text: (By.XPATH, f'//*[contains(@class,"el-menu-item") or contains(@class,"el-sub-menu__title")][.//span[text()="{text}"]]')

# 顶部导航用户区
NAVBAR_USER = (By.CSS_SELECTOR, ".navbar .el-dropdown, .navbar [class*=el-dropdown]")


class HomePage(BasePage):
    """登录后的后台布局页（侧边栏 + 顶栏）"""

    def click_menu(self, text: str):
        """点击侧边栏菜单（一级或子菜单）"""
        self.click(MENU_ITEM_BOX(text))
        return self

    def is_menu_visible(self, text: str) -> bool:
        return self.is_visible(MENU_ITEM(text))

    def body_text(self) -> str:
        return self.driver.find_element(By.TAG_NAME, "body").text

    def is_on_layout(self) -> bool:
        """登录后应进入布局页（非 login 路由）"""
        return "login" not in self.current_url()
