# -*- coding: utf-8 -*-
"""
TestFlow-Mall 接口自动化测试框架 - 环境配置
被测系统：mall 电商后台（本地部署）
"""
import os

# 被测系统基础地址（mall-admin 后端）
BASE_URL = os.getenv("MALL_BASE_URL", "http://localhost:8080")

# 登录账号
ADMIN_USERNAME = os.getenv("MALL_ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("MALL_ADMIN_PASS", "macro123")
TEST_USERNAME = os.getenv("MALL_TEST_USER", "test")
TEST_PASSWORD = os.getenv("MALL_TEST_PASS", "123456")
PRODUCT_ADMIN_USER = os.getenv("MALL_PRODUCT_ADMIN_USER", "productAdmin")
PRODUCT_ADMIN_PASS = os.getenv("MALL_PRODUCT_ADMIN_PASS", "123456")
ORDER_ADMIN_USER = os.getenv("MALL_ORDER_ADMIN_USER", "orderAdmin")
ORDER_ADMIN_PASS = os.getenv("MALL_ORDER_ADMIN_PASS", "123456")

# 数据库配置（一致性断言用）
DB_HOST = os.getenv("MALL_DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("MALL_DB_PORT", "3306"))
DB_USER = os.getenv("MALL_DB_USER", "mall")
DB_PASSWORD = os.getenv("MALL_DB_PASS", "mall123456")
DB_NAME = os.getenv("MALL_DB_NAME", "mall")

# 请求配置
TIMEOUT = 15  # 秒
