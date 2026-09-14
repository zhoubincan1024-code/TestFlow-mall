# -*- coding: utf-8 -*-
"""
HTTP 请求封装：
- 统一拼接 base_url、组装请求头（Content-Type / Authorization）
- 每次请求记录日志（方法、路径、状态码、耗时、响应摘要）
- Token 由外部注入（conftest 中登录获取）
"""
import time

import requests

from config import BASE_URL, TIMEOUT
from utils.logger import get_logger

logger = get_logger("http")


class ApiClient:
    """mall-admin 后端 API 客户端"""

    def __init__(self, base_url: str = BASE_URL, token: str = None):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.session = requests.Session()

    @property
    def headers(self) -> dict:
        h = {"Content-Type": "application/json"}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    def set_token(self, token: str):
        self.token = token

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}" if path.startswith("/") else f"{self.base_url}/{path}"
        kwargs.setdefault("headers", self.headers)
        kwargs.setdefault("timeout", TIMEOUT)

        start = time.time()
        resp = self.session.request(method, url, **kwargs)
        cost_ms = round((time.time() - start) * 1000)

        # 响应摘要：JSON 截断到 200 字符
        try:
            summary = resp.text[:200]
        except Exception:
            summary = "<binary>"
        logger.info("[%s %s] -> %d | %dms | %s", method.upper(), path, resp.status_code, cost_ms, summary)
        return resp

    def get(self, path: str, **kwargs) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self.request("DELETE", path, **kwargs)


def parse_json(resp: requests.Response) -> dict:
    """解析统一响应体，返回 dict；非 JSON 时记录日志"""
    try:
        return resp.json()
    except ValueError:
        logger.error("响应非 JSON: %s", resp.text[:200])
        return {}
