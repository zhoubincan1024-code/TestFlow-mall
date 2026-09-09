# -*- coding: utf-8 -*-
"""登录/用户信息接口封装"""
from utils.http_client import ApiClient, parse_json


def login(client: ApiClient, username: str, password: str) -> dict:
    """POST /admin/login 登录，返回响应体 dict"""
    resp = client.post("/admin/login", json={"username": username, "password": password})
    return parse_json(resp)


def get_admin_info(client: ApiClient) -> dict:
    """GET /admin/info 获取当前登录用户信息"""
    resp = client.get("/admin/info")
    return parse_json(resp)
