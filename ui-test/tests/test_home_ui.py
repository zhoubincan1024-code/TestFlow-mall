# -*- coding: utf-8 -*-
"""
后台首页与导航 UI 用例（已登录）
- 注意：商品列表页 #/pms/product 存在 BUG-001（路由渲染异常），本文件不进入该页面
"""
from pages.home_page import HomePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def test_sidebar_has_module_groups(logged_in_driver):
    """侧边栏应展示首页/商品/订单/营销/权限五大模块"""
    home = HomePage(logged_in_driver)
    for name in ("首页", "商品", "订单", "营销", "权限"):
        assert home.is_menu_visible(name), f"侧边栏缺少菜单: {name}"


def test_dashboard_cards(logged_in_driver):
    """首页看板卡片：今日订单总数、今日销售总额"""
    home = HomePage(logged_in_driver)
    body = home.body_text()
    assert "今日订单总数" in body, f"看板应显示今日订单总数: {body[:300]}"
    assert "今日销售总额" in body, f"看板应显示今日销售总额: {body[:300]}"
    assert "待处理事务" in body, f"看板应显示待处理事务: {body[:300]}"


def test_navigate_to_order_page(logged_in_driver):
    """展开订单-点击订单列表：进入 #/oms/order"""
    home = HomePage(logged_in_driver)
    home.click_menu("订单")          # 展开一级菜单
    home.click_menu("订单列表")      # 点击子菜单
    WebDriverWait(logged_in_driver, 10).until(
        lambda d: "oms/order" in d.current_url, message="应跳转到订单列表页"
    )
    assert "oms/order" in logged_in_driver.current_url


def test_navigate_to_coupon_page(logged_in_driver):
    """展开营销-点击优惠券列表：进入 #/sms/coupon"""
    home = HomePage(logged_in_driver)
    home.click_menu("营销")           # 展开一级菜单
    home.click_menu("优惠券列表")     # 点击子菜单
    WebDriverWait(logged_in_driver, 10).until(
        lambda d: "sms/coupon" in d.current_url, message="应跳转到优惠券页"
    )
    assert "sms/coupon" in logged_in_driver.current_url
