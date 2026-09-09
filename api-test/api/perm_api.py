# -*- coding: utf-8 -*-
"""权限模块接口封装：后台用户、角色、菜单、资源（路径以 mall-admin-web apis 为准）"""
from utils.http_client import ApiClient, parse_json


def list_admins(client: ApiClient, page_num: int = 1, page_size: int = 100) -> dict:
    """GET /admin/list 后台用户列表（实测 8 个）"""
    resp = client.get("/admin/list", params={"pageNum": page_num, "pageSize": page_size})
    return parse_json(resp)


def list_roles(client: ApiClient, page_num: int = 1, page_size: int = 100) -> dict:
    """GET /role/list 分页角色列表（实测 3 个：商品管理员/订单管理员/超级管理员）"""
    resp = client.get("/role/list", params={"pageNum": page_num, "pageSize": page_size})
    return parse_json(resp)


def list_all_roles(client: ApiClient) -> dict:
    """GET /role/listAll 全部角色（返回数组）"""
    resp = client.get("/role/listAll")
    return parse_json(resp)


def get_menu_tree(client: ApiClient) -> dict:
    """GET /menu/treeList 菜单树（返回数组，一级节点 4 个）"""
    resp = client.get("/menu/treeList")
    return parse_json(resp)


def list_menus_by_parent(client: ApiClient, parent_id: int = 0, page_num: int = 1, page_size: int = 100) -> dict:
    """GET /menu/list/{parentId} 按上级菜单分页查询（parentId=0 一级菜单 4 个）"""
    resp = client.get(f"/menu/list/{parent_id}", params={"pageNum": page_num, "pageSize": page_size})
    return parse_json(resp)


def get_admin_roles(client: ApiClient, admin_id: int) -> dict:
    """GET /admin/role/{id} 用户绑定的角色（返回数组）"""
    resp = client.get(f"/admin/role/{admin_id}")
    return parse_json(resp)


def list_resources(client: ApiClient, page_num: int = 1, page_size: int = 100) -> dict:
    """GET /resource/list 资源权限点列表（实测 31 条）"""
    resp = client.get("/resource/list", params={"pageNum": page_num, "pageSize": page_size})
    return parse_json(resp)
