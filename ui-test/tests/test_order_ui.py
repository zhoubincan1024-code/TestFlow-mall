# -*- coding: utf-8 -*-
"""
订单列表页 UI 用例（已登录）：表格数据与搜索
"""
from pages.home_page import HomePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def _open_order_list(driver):
    home = HomePage(driver)
    home.click_menu("订单")          # 展开一级菜单
    home.click_menu("订单列表")      # 点击子菜单
    WebDriverWait(driver, 10).until(
        lambda d: "oms/order" in d.current_url, message="应进入订单列表页"
    )


def test_order_table_has_seed_data(logged_in_driver):
    """订单列表表格应展示种子订单号 201809150101000001"""
    _open_order_list(logged_in_driver)
    body = logged_in_driver.find_element(By.TAG_NAME, "body").text
    assert "201809150101000001" in body, "订单表应含种子订单号"


def test_order_table_has_columns(logged_in_driver):
    """订单列表表头：订单编号、订单金额、订单状态"""
    _open_order_list(logged_in_driver)
    body = logged_in_driver.find_element(By.TAG_NAME, "body").text
    for col in ("订单编号", "订单金额", "订单状态"):
        assert col in body, f"订单表应含表头: {col}"
