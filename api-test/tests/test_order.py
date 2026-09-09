# -*- coding: utf-8 -*-
"""
订单模块接口测试：订单列表、订单详情
"""
from api import order_api


def test_order_list_default(authed_client):
    """订单列表默认分页：共 48 条，第一页 10 条"""
    body = order_api.list_orders(authed_client, page_num=1, page_size=10)
    assert body.get("code") == 200, f"订单列表失败: {body}"
    data = body.get("data", {})
    assert data.get("total", 0) >= 48, f"订单总数应 >= 48: {data.get('total')}"
    assert len(data.get("list", [])) == 10, "第一页应返回 10 条"


def test_order_list_search_by_order_sn(authed_client):
    """按订单编号精确查询"""
    body = order_api.list_orders(authed_client, order_sn="201809150101000001")
    assert body.get("code") == 200, f"订单查询失败: {body}"
    items = body.get("data", {}).get("list", [])
    assert items, "应返回匹配订单"
    assert items[0].get("orderSn") == "201809150101000001", "订单编号应匹配"


def test_order_list_filter_by_status(authed_client):
    """按订单状态筛选（状态码来自订单列表实际值）"""
    first = order_api.list_orders(authed_client, page_num=1, page_size=10)
    first_items = first.get("data", {}).get("list", [])
    assert first_items, "订单数据不应为空"
    status = first_items[0].get("status")
    body = order_api.list_orders(authed_client, status=status)
    assert body.get("code") == 200
    filtered = body.get("data", {}).get("list", [])
    assert filtered, "筛选结果不应为空"
    assert all(item.get("status") == status for item in filtered), "筛选结果状态应一致"


def test_order_detail(authed_client):
    """订单详情：返回完整订单信息"""
    body = order_api.get_order_detail(authed_client, order_id=12)
    assert body.get("code") == 200, f"订单详情失败: {body}"
    data = body.get("data", {})
    assert data.get("orderSn") == "201809150101000001", f"订单号不符: {data.get('orderSn')}"
    assert data.get("memberUsername") == "test", f"下单用户应为 test: {data.get('memberUsername')}"
    assert data.get("totalAmount") is not None, "应包含订单金额"
