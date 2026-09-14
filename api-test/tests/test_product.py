# -*- coding: utf-8 -*-
"""
商品模块接口测试：商品列表、搜索、品牌、分类、类型
"""
from api import product_api


def test_product_list_default(authed_client):
    """商品列表默认分页：共 20 条，第一页 10 条"""
    body = product_api.list_products(authed_client, page_num=1, page_size=10)
    assert body.get("code") == 200, f"商品列表失败: {body}"
    data = body.get("data", {})
    assert data.get("total", 0) >= 20, f"商品总数应 >= 20: {data.get('total')}"
    assert len(data.get("list", [])) == 10, "第一页应返回 10 条"


def test_product_list_search_by_name(authed_client):
    """按商品名称搜索：结果应包含关键字"""
    body = product_api.list_products(authed_client, keyword="华为")
    assert body.get("code") == 200, f"搜索失败: {body}"
    items = body.get("data", {}).get("list", [])
    assert items, "应返回匹配商品"
    assert all("华为" in (item.get("name") or "") for item in items), "所有结果名称应含关键字"


def test_product_list_filter_by_category(authed_client):
    """按分类筛选（手机数码一级分类，parentId=0 返回真实分类 ID）"""
    # 取一级分类列表拿到真实分类 ID
    cates = product_api.list_product_categories(authed_client, parent_id=0)
    cate_list = cates.get("data", {}).get("list", [])
    target = next((c for c in cate_list if "手机" in (c.get("name") or "")), None)
    assert target, "应存在手机数码分类"
    body = product_api.list_products(authed_client, product_category_id=target["id"])
    assert body.get("code") == 200
    assert body.get("data", {}).get("total", 0) >= 0


def test_brand_list(authed_client):
    """品牌列表：应返回品牌数据"""
    body = product_api.list_brands(authed_client)
    assert body.get("code") == 200, f"品牌列表失败: {body}"
    items = body.get("data", {}).get("list", [])
    assert items, "品牌列表不应为空"
    names = [i.get("name") for i in items]
    assert "小米" in names, f"品牌列表应含小米: {names}"


def test_product_category_list(authed_client):
    """商品分类列表（parentId=0 一级分类）：共 6 条，应含服装、手机数码"""
    body = product_api.list_product_categories(authed_client, parent_id=0)
    assert body.get("code") == 200, f"分类列表失败: {body}"
    data = body.get("data", {})
    assert data.get("total") == 6, f"一级分类应共 6 条: {data.get('total')}"
    names = [c.get("name") for c in data.get("list", [])]
    assert "服装" in names, f"分类列表应含服装: {names}"
    assert "手机数码" in names, f"分类列表应含手机数码: {names}"


def test_product_attr_category_list(authed_client):
    """商品类型列表：应返回类型数据"""
    body = product_api.list_product_attrs(authed_client)
    assert body.get("code") == 200, f"类型列表失败: {body}"
    items = body.get("data", {}).get("list", [])
    assert items, "商品类型列表不应为空"
