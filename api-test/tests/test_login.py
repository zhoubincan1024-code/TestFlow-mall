# -*- coding: utf-8 -*-
"""
登录接口测试：
- 正常登录（参数化：admin/test）
- 错误密码 / 不存在账号 / 空账号（参数化）
- 登录后获取用户信息
"""
import pytest

import config
from api import auth_api
from utils.http_client import parse_json

SUCCESS_CASES = [
    pytest.param(config.ADMIN_USERNAME, config.ADMIN_PASSWORD, "admin", id="admin-login"),
    pytest.param(config.TEST_USERNAME, config.TEST_PASSWORD, "test", id="test-login"),
]

FAIL_CASES = [
    pytest.param("admin", "123456", 500, id="wrong-password"),
    pytest.param("nouser", "123456", 404, id="not-exist-user"),
    pytest.param("", "", 404, id="empty-account"),
]


@pytest.mark.parametrize("username,password,expect_user", SUCCESS_CASES)
def test_login_success(client, username, password, expect_user):
    """正常登录应返回 code=200 且带 token"""
    body = auth_api.login(client, username, password)
    assert body.get("code") == 200, f"登录应成功，实际: {body}"
    assert body.get("data", {}).get("token"), "响应应包含 token"
    assert body.get("data", {}).get("tokenHead") == "Bearer ", "tokenHead 应为 Bearer "


@pytest.mark.parametrize("username,password,expect_code", FAIL_CASES)
def test_login_fail(client, username, password, expect_code):
    """异常登录应按业务码返回错误，且不返回 token"""
    body = auth_api.login(client, username, password)
    assert body.get("code") == expect_code, f"业务码应等于 {expect_code}，实际: {body}"
    assert body.get("token") is None and body.get("data") is None, "失败响应不应带 token"


def test_wrong_password_message(client):
    """错误密码提示语应明确"""
    body = auth_api.login(client, "admin", "123456")
    assert body.get("message") == "密码不正确", f"错误密码提示不符: {body}"


def test_get_admin_info(authed_client):
    """登录成功后通过 token 获取当前用户信息"""
    body = auth_api.get_admin_info(authed_client)
    assert body.get("code") == 200, f"获取用户信息失败: {body}"
    data = body.get("data", {})
    assert data.get("username") == "admin", f"用户名应为 admin: {data.get('username')}"
    assert data.get("menus"), "用户信息应包含菜单列表"
    assert data.get("roles"), "用户信息应包含角色列表"
