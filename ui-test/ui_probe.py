# -*- coding: utf-8 -*-
"""探查订单列表页表头"""
import time
import config
from pages.login_page import LoginPage
from pages.home_page import HomePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from utils.logger import get_logger
from conftest import _make_driver

logger = get_logger("probe")
d = _make_driver()
try:
    LoginPage(d).open().login(config.ADMIN_USERNAME, config.ADMIN_PASSWORD)
    WebDriverWait(d, config.WAIT_TIMEOUT).until(lambda x: "login" not in x.current_url)
    home = HomePage(d)
    home.click_menu("订单")
    home.click_menu("订单列表")
    WebDriverWait(d, 10).until(lambda x: "oms/order" in x.current_url)
    time.sleep(2)
    print("URL:", d.current_url)
    # 表头：el-table 的 th
    ths = d.find_elements(By.CSS_SELECTOR, ".el-table__header th")
    headers = [t.text.strip() for t in ths if t.text.strip()]
    print("TABLE HEADERS:", headers)
    # 第一行数据
    rows = d.find_elements(By.CSS_SELECTOR, ".el-table__body tr")
    if rows:
        print("FIRST ROW:", rows[0].text[:200])
finally:
    d.quit()
