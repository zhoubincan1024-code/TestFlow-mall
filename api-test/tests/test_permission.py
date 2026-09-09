# -*- coding: utf-8 -*-
"""
权限模块接口测试：后台用户、角色、菜单树、资源点 + RBAC 越权边界
- admin/test 为超级管理员（role 5），拥有全部资源点
- productAdmin 仅商品资源、orderAdmin 仅订单资源（RBAC 隔离验证）
"""
import config
from api import perm_api
from utils.http_client import parse_json


def test_admin_list(authed_client):
    """后台用户列表：共 8 个"""
    body = perm_api.list_admins(authed_client)
    assert body.get("code") == 200, f"用户列表失败: {body}"
    data = body.get("data", {})
    assert data.get("total", 0) == 8, f"后台用户应共 8 个: {data.get('total')}"
    names = [u.get("username") for u in data.get("list", [])]
    assert "admin" in names and "test" in names, f"用户列表应含 admin/test: {names}"


def test_role_list(authed_client):
    """角色列表：共 3 个角色"""
    body = perm_api.list_roles(authed_client)
    assert body.get("code") == 200, f"角色列表失败: {body}"
    data = body.get("data", {})
    assert data.get("total", 0) == 3, f"角色应共 3 个: {data.get('total')}"
    names = [r.get("name") for r in data.get("list", [])]
    assert "超级管理员" in names, f"角色应含超级管理员: {names}"
    assert "商品管理员" in names and "订单管理员" in names, f"角色应含商品/订单管理员: {names}"


def test_menu_tree(authed_client):
    """菜单树：一级节点 4 个（pms/oms/sms/ums 分组，title 为中文名）"""
    body = perm_api.get_menu_tree(authed_client)
    assert body.get("code") == 200, f"菜单树失败: {body}"
    nodes = body.get("data", [])
    assert nodes, "菜单树不应为空"
    titles = [n.get("title") for n in nodes]
    names = [n.get("name") for n in nodes]
    assert "商品" in titles, f"菜单树应含商品分组: {titles}"
    assert "订单" in titles, f"菜单树应含订单分组: {titles}"
    assert "pms" in names and "oms" in names, f"菜单 name 应为分组标识: {names}"


def test_menu_list_by_parent(authed_client):
    """一级菜单分页：parentId=0 共 4 个"""
    body = perm_api.list_menus_by_parent(authed_client, parent_id=0)
    assert body.get("code") == 200, f"菜单分页失败: {body}"
    assert body.get("data", {}).get("total", 0) == 4, "一级菜单应共 4 个"


def test_admin_role_is_super(authed_client):
    """admin 用户（id=3）绑定超级管理员角色"""
    body = perm_api.get_admin_roles(authed_client, admin_id=3)
    assert body.get("code") == 200, f"查询用户角色失败: {body}"
    roles = body.get("data", [])
    names = [r.get("name") for r in roles]
    assert "超级管理员" in names, f"admin 应绑定超级管理员: {names}"


def test_resource_list(authed_client):
    """资源权限点：共 31 条，覆盖商品/订单/营销/权限四类"""
    body = perm_api.list_resources(authed_client)
    assert body.get("code") == 200, f"资源列表失败: {body}"
    data = body.get("data", {})
    assert data.get("total", 0) == 31, f"资源应共 31 条: {data.get('total')}"
    urls = [r.get("url") for r in data.get("list", [])]
    assert "/product/**" in urls and "/order/**" in urls, "资源应含商品/订单权限点"
    assert "/coupon/**" in urls and "/admin/**" in urls, "资源应含营销/权限权限点"


def test_super_admin_full_access(authed_client):
    """超级管理员可访问商品/订单/营销/权限四类接口"""
    for path in ("/product/list", "/order/list", "/coupon/list", "/admin/list"):
        resp = authed_client.get(path, params={"pageNum": 1, "pageSize": 3})
        body = parse_json(resp)
        assert body.get("code") == 200, f"超级管理员访问 {path} 应 200，实际: {body}"


def test_product_admin_only_product_access(rbac_client_factory, product_admin_token):
    """商品管理员：/product/** 可访问，/order/**、/coupon/** 应 403"""
    c = rbac_client_factory(product_admin_token)
    ok = parse_json(c.get("/product/list", params={"pageNum": 1, "pageSize": 3}))
    assert ok.get("code") == 200, f"商品管理员访问商品应 200，实际: {ok}"
    for path in ("/order/list", "/coupon/list", "/admin/list"):
        denied = parse_json(c.get(path, params={"pageNum": 1, "pageSize": 3}))
        assert denied.get("code") == 403, f"商品管理员访问 {path} 应 403，实际: {denied}"
        assert "没有相关权限" in denied.get("message", ""), f"403 提示语不符: {denied}"


def test_order_admin_only_order_access(rbac_client_factory, order_admin_token):
    """订单管理员：/order/** 可访问，/product/**、/coupon/** 应 403"""
    c = rbac_client_factory(order_admin_token)
    ok = parse_json(c.get("/order/list", params={"pageNum": 1, "pageSize": 3}))
    assert ok.get("code") == 200, f"订单管理员访问订单应 200，实际: {ok}"
    for path in ("/product/list", "/coupon/list", "/admin/list"):
        denied = parse_json(c.get(path, params={"pageNum": 1, "pageSize": 3}))
        assert denied.get("code") == 403, f"订单管理员访问 {path} 应 403，实际: {denied}"
