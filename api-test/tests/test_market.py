# -*- coding: utf-8 -*-
"""
营销模块接口测试：秒杀活动、优惠券、首页广告、人气推荐
（路径以 mall-admin-web/src/apis 为准：/flash/list、/coupon/list、/home/advertise/list）
"""
from api import market_api


def test_flash_promotion_list(authed_client):
    """秒杀活动列表：共 1 条（双11特卖）"""
    body = market_api.list_flash_promotions(authed_client)
    assert body.get("code") == 200, f"秒杀活动列表失败: {body}"
    data = body.get("data", {})
    assert data.get("total", 0) >= 1, f"秒杀活动应 >= 1 条: {data.get('total')}"
    names = [a.get("title") for a in data.get("list", [])]
    assert "双11" in "".join(names), f"应含双11特卖活动: {names}"


def test_coupon_list(authed_client):
    """优惠券列表：共 5 条（多已过期为种子数据时效，非缺陷）"""
    body = market_api.list_coupons(authed_client)
    assert body.get("code") == 200, f"优惠券列表失败: {body}"
    data = body.get("data", {})
    assert data.get("total", 0) == 5, f"优惠券应共 5 条: {data.get('total')}"
    assert data.get("list"), "优惠券列表不应为空"
    assert "name" in data.get("list", [{}])[0], "优惠券应包含名称字段"


def test_advertise_list(authed_client):
    """首页广告列表：共 11 条"""
    body = market_api.list_advertises(authed_client)
    assert body.get("code") == 200, f"广告列表失败: {body}"
    data = body.get("data", {})
    assert data.get("total", 0) == 11, f"广告应共 11 条: {data.get('total')}"
    names = [a.get("name") for a in data.get("list", [])]
    assert any("电影" in n for n in names), f"种子广告应含电影推荐: {names}"


def test_recommend_product_list(authed_client):
    """人气推荐列表：共 5 条"""
    body = market_api.list_recommend_products(authed_client)
    assert body.get("code") == 200, f"人气推荐失败: {body}"
    data = body.get("data", {})
    assert data.get("total", 0) == 5, f"人气推荐应共 5 条: {data.get('total')}"
    assert data.get("list"), "人气推荐列表不应为空"
