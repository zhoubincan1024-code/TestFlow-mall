# -*- coding: utf-8 -*-
"""
数据库一致性测试：接口分页 total 与数据库 COUNT 交叉核对
（覆盖测试计划中"数据库层 PyMySQL 一致性校验"）
"""
import config
from api import market_api, order_api, perm_api, product_api
from utils.db import assert_count_matches


def test_product_total_matches_db(authed_client):
    """商品总数一致：接口 total == pms_product 未删除(delete_status=0)行数（种子含 18 条逻辑删除）"""
    body = product_api.list_products(authed_client, page_num=1, page_size=1)
    assert_count_matches("pms_product", body.get("data", {}).get("total", 0), "delete_status=0")


def test_order_total_matches_db(authed_client):
    """订单总数一致：接口 total == oms_order 未删除(delete_status=0)行数（种子含 17 条逻辑删除）"""
    body = order_api.list_orders(authed_client, page_num=1, page_size=1)
    assert_count_matches("oms_order", body.get("data", {}).get("total", 0), "delete_status=0")


def test_admin_total_matches_db(authed_client):
    """后台用户总数一致：接口 total == ums_admin 行数"""
    body = perm_api.list_admins(authed_client, page_num=1, page_size=1)
    assert_count_matches("ums_admin", body.get("data", {}).get("total", 0))


def test_level1_category_matches_db(authed_client):
    """一级分类数一致：接口 total == parent_id=0 分类数"""
    body = product_api.list_product_categories(authed_client, parent_id=0, page_num=1, page_size=1)
    assert_count_matches("pms_product_category", body.get("data", {}).get("total", 0), "parent_id=0")


def test_coupon_total_matches_db(authed_client):
    """优惠券总数一致：接口 total == sms_coupon 行数"""
    body = market_api.list_coupons(authed_client, page_num=1, page_size=1)
    assert_count_matches("sms_coupon", body.get("data", {}).get("total", 0))


def test_advertise_total_matches_db(authed_client):
    """广告总数一致：接口 total == sms_home_advertise 行数"""
    body = market_api.list_advertises(authed_client, page_num=1, page_size=1)
    assert_count_matches("sms_home_advertise", body.get("data", {}).get("total", 0))


def test_role_total_matches_db(authed_client):
    """角色总数一致：接口 total == ums_role 行数"""
    body = perm_api.list_roles(authed_client, page_num=1, page_size=1)
    assert_count_matches("ums_role", body.get("data", {}).get("total", 0))


def test_resource_total_matches_db(authed_client):
    """资源权限点数一致：接口 total == ums_resource 行数"""
    body = perm_api.list_resources(authed_client, page_num=1, page_size=1)
    assert_count_matches("ums_resource", body.get("data", {}).get("total", 0))
