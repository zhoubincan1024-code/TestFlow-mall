# -*- coding: utf-8 -*-
"""
接口鉴权测试：未登录 / 无效 token 访问受保护接口应返回业务码 401
"""
from utils.http_client import ApiClient, parse_json


def test_no_token_access_401(client):
    """未携带 token 访问商品列表应返回 code=401"""
    resp = client.get("/product/list", params={"pageNum": 1, "pageSize": 3})
    body = parse_json(resp)
    assert body.get("code") == 401, f"未登录应返回 401，实际: {body}"
    assert "暂未登录" in body.get("message", ""), "提示语应说明未登录"


def test_invalid_token_access_401(base_url):
    """携带无效 token 访问商品列表应返回 code=401"""
    c = ApiClient(base_url)
    c.set_token("invalid.token.xyz")
    resp = c.get("/product/list", params={"pageNum": 1, "pageSize": 3})
    body = parse_json(resp)
    assert body.get("code") == 401, f"无效 token 应返回 401，实际: {body}"


def test_valid_token_access_200(authed_client):
    """携带有效 token 访问商品列表应返回 code=200"""
    resp = authed_client.get("/product/list", params={"pageNum": 1, "pageSize": 3})
    body = parse_json(resp)
    assert body.get("code") == 200, f"有效 token 应返回 200，实际: {body}"
