# -*- coding: utf-8 -*-
"""商品模块接口封装：商品列表、品牌、分类、类型"""
from utils.http_client import ApiClient, parse_json


def list_products(client: ApiClient, page_num: int = 1, page_size: int = 10, **params) -> dict:
    """GET /product/list 商品列表，支持 keyword/productCategoryId/brandId/publishStatus 等筛选"""
    query = {"pageNum": page_num, "pageSize": page_size}
    query.update({k: v for k, v in params.items() if v is not None})
    resp = client.get("/product/list", params=query)
    return parse_json(resp)


def list_brands(client: ApiClient, page_num: int = 1, page_size: int = 100) -> dict:
    """GET /brand/list 品牌列表"""
    resp = client.get("/brand/list", params={"pageNum": page_num, "pageSize": page_size})
    return parse_json(resp)


def list_product_categories(client: ApiClient, parent_id: int = 0, page_num: int = 1, page_size: int = 100) -> dict:
    """GET /productCategory/list/{parentId} 商品分类列表（parentId=0 为一级分类，实测返回 6 条）"""
    resp = client.get(f"/productCategory/list/{parent_id}", params={"pageNum": page_num, "pageSize": page_size})
    return parse_json(resp)


def list_product_attrs(client: ApiClient, page_num: int = 1, page_size: int = 100) -> dict:
    """GET /productAttribute/category/list 商品类型列表"""
    resp = client.get("/productAttribute/category/list", params={"pageNum": page_num, "pageSize": page_size})
    return parse_json(resp)
