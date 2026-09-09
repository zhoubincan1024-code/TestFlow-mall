# -*- coding: utf-8 -*-
"""订单模块接口封装：订单列表、订单详情"""
from utils.http_client import ApiClient, parse_json


def list_orders(client: ApiClient, page_num: int = 1, page_size: int = 10, **params) -> dict:
    """GET /order/list 订单列表，支持 orderSn/receiverKeyword/status/orderType 等筛选"""
    query = {"pageNum": page_num, "pageSize": page_size}
    query.update({k: v for k, v in params.items() if v is not None})
    resp = client.get("/order/list", params=query)
    return parse_json(resp)


def get_order_detail(client: ApiClient, order_id: int) -> dict:
    """GET /order/{id} 订单详情"""
    resp = client.get(f"/order/{order_id}")
    return parse_json(resp)
