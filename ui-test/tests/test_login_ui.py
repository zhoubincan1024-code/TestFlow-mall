# -*- coding: utf-8 -*-
"""
登录页 UI 用例
"""
import config
from pages.home_page import HomePage
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By


def test_login_success_redirect(driver):
    """正确账号密码登录：跳转离开登录页，进入后台布局"""
    LoginPage(driver).open().login(config.ADMIN_USERNAME, config.ADMIN_PASSWORD)
    home = HomePage(driver)
    from selenium.webdriver.support.ui import WebDriverWait
    WebDriverWait(driver, config.WAIT_TIMEOUT).until(
        lambda d: "login" not in d.current_url, message="登录成功未跳转"
    )
    assert home.is_on_layout(), f"应进入后台布局，当前 URL: {driver.current_url}"
    # 侧边栏应出现业务菜单
    assert home.is_menu_visible("首页"), "侧边栏应显示首页菜单"
    assert home.is_menu_visible("商品"), "侧边栏应显示商品菜单"


def test_login_wrong_password_stay(driver):
    """错误密码：停留登录页，不跳转"""
    page = LoginPage(driver).open().login("admin", "123456")
    from selenium.webdriver.support.ui import WebDriverWait
    import time
    time.sleep(1)  # 等待请求返回
    assert page.is_on_login_page(), f"错误密码应停留登录页: {driver.current_url}"
    assert "login" in driver.current_url


def test_login_short_password_validate(driver):
    """密码不足 3 位：表单校验提示，不发起登录"""
    page = LoginPage(driver).open().login("admin", "12")
    err = page.get_form_error()
    assert "密码不能小于3位" in err, f"应提示密码不能小于3位: {err!r}"
    assert page.is_on_login_page(), "校验失败应停留登录页"


def test_unauth_access_home_redirect(driver):
    """未登录直接访问后台首页：跳转登录页"""
    driver.get(f"{config.FRONTEND_URL}/#/home")
    from selenium.webdriver.support.ui import WebDriverWait
    WebDriverWait(driver, config.WAIT_TIMEOUT).until(
        lambda d: "login" in d.current_url, message="未登录访问应被重定向到登录页"
    )
    assert "login" in driver.current_url, f"应跳转登录页: {driver.current_url}"
