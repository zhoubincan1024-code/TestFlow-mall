# -*- coding: utf-8 -*-
"""
Pytest 全局 fixtures：
- base_url / client：无 token 客户端
- admin_token：session 级登录 admin 获取 token（Token 关联）
- authed_client：携带 admin token 的客户端

Allure 增强（零侵入）：
pytest_collection_modifyitems 按测试模块自动设置 epic/feature/story 与中文标题，
41 条用例无需逐个添加装饰器即可在 Allure 报告中呈现模块化结构。
"""
import allure
import pytest

import config
from api import auth_api
from utils.http_client import ApiClient
from utils.logger import get_logger

logger = get_logger("conftest")

MODULE_MAP = {
    "test_login": ("接口测试", "登录与认证"),
    "test_auth": ("接口测试", "鉴权与权限"),
    "test_product": ("接口测试", "商品模块"),
    "test_order": ("接口测试", "订单模块"),
    "test_market": ("接口测试", "营销模块"),
    "test_permission": ("接口测试", "权限管理"),
    "test_db_consistency": ("接口测试", "数据库一致性"),
}


def pytest_collection_modifyitems(items):
    """按模块归属自动设置 Allure epic/feature/story 与标题"""
    for item in items:
        module_name = item.module.__name__.split(".")[-1]
        if module_name in MODULE_MAP:
            epic, feature = MODULE_MAP[module_name]
            allure.dynamic.epic(epic)
            allure.dynamic.feature(feature)
            allure.dynamic.story(feature)
        name = item.name.replace("test_", "").replace("_", " ")
        allure.dynamic.title(name)


@pytest.fixture(scope="session")
def base_url() -> str:
    return config.BASE_URL


@pytest.fixture(scope="session")
def client() -> ApiClient:
    """无 token 的客户端（登录接口、未登录鉴权场景使用）"""
    return ApiClient(config.BASE_URL)


@pytest.fixture(scope="session")
def admin_token(client: ApiClient) -> str:
    """前置登录：admin/macro123 获取 token，供所有接口用例复用"""
    body = auth_api.login(client, config.ADMIN_USERNAME, config.ADMIN_PASSWORD)
    assert body.get("code") == 200, f"登录失败: {body}"
    token = body.get("data", {}).get("token")
    assert token, "登录响应缺少 token"
    logger.info("获取 admin token 成功")
    return token


@pytest.fixture(scope="session")
def authed_client(client: ApiClient, admin_token: str) -> ApiClient:
    """携带 admin token 的客户端"""
    c = ApiClient(config.BASE_URL)
    c.set_token(admin_token)
    return c


def _login_token(client: ApiClient, username: str, password: str, label: str) -> str:
    body = auth_api.login(client, username, password)
    assert body.get("code") == 200, f"{label} 登录失败: {body}"
    token = body.get("data", {}).get("token")
    assert token, f"{label} 登录响应缺少 token"
    return token


@pytest.fixture(scope="session")
def product_admin_token(client: ApiClient) -> str:
    """商品管理员（productAdmin/123456，仅 /product/** 等商品资源权限）"""
    return _login_token(client, config.PRODUCT_ADMIN_USER, config.PRODUCT_ADMIN_PASS, "productAdmin")


@pytest.fixture(scope="session")
def order_admin_token(client: ApiClient) -> str:
    """订单管理员（orderAdmin/123456，仅 /order/** 等订单资源权限）"""
    return _login_token(client, config.ORDER_ADMIN_USER, config.ORDER_ADMIN_PASS, "orderAdmin")


@pytest.fixture(scope="session")
def rbac_client_factory():
    """根据 token 生成携带认证的客户端（RBAC 越权用例）"""
    def factory(token: str) -> ApiClient:
        c = ApiClient(config.BASE_URL)
        c.set_token(token)
        return c
    return factory
