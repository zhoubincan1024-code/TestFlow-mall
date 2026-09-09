# -*- coding: utf-8 -*-
"""营销模块接口封装：秒杀活动、优惠券、首页广告、人气推荐（路径以 mall-admin-web apis 为准）"""
from utils.http_client import ApiClient, parse_json


def list_flash_promotions(client: ApiClient, page_num: int = 1, page_size: int = 100) -> dict:
    """GET /flash/list 秒杀活动列表（实测 1 条：双11特卖）"""
    resp = client.get("/flash/list", params={"pageNum": page_num, "pageSize": page_size})
    return parse_json(resp)


def list_coupons(client: ApiClient, page_num: int = 1, page_size: int = 100, **params) -> dict:
    """GET /coupon/list 优惠券列表（实测 5 条，多已过期为种子数据时效）"""
    query = {"pageNum": page_num, "pageSize": page_size}
    query.update({k: v for k, v in params.items() if v is not None})
    resp = client.get("/coupon/list", params=query)
    return parse_json(resp)


def list_advertises(client: ApiClient, page_num: int = 1, page_size: int = 100) -> dict:
    """GET /home/advertise/list 首页轮播广告列表（实测 11 条）"""
    resp = client.get("/home/advertise/list", params={"pageNum": page_num, "pageSize": page_size})
    return parse_json(resp)


def list_recommend_products(client: ApiClient, page_num: int = 1, page_size: int = 100) -> dict:
    """GET /home/recommendProduct/list 人气推荐列表（实测 5 条）"""
    resp = client.get("/home/recommendProduct/list", params={"pageNum": page_num, "pageSize": page_size})
    return parse_json(resp)
