# -*- coding: utf-8 -*-
"""
数据库连接与断言辅助（PyMySQL）：
- 接口返回的分页 total 与数据库 COUNT 做一致性核对
- 所有查询只读，不修改数据
"""
import pymysql

import config
from utils.logger import get_logger

logger = get_logger("db")


def get_connection():
    """建立数据库连接（只读查询）"""
    return pymysql.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )


def count(table: str, where: str = "") -> int:
    """统计表行数：count('pms_product') / count('pms_product_category', 'parent_id=0')"""
    sql = f"SELECT COUNT(*) AS c FROM {table}"
    if where:
        sql += f" WHERE {where}"
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            row = cur.fetchone()
            return int(row["c"])
    finally:
        conn.close()


def assert_count_matches(table: str, api_total: int, where: str = ""):
    """断言接口 total 与数据库行数一致，并记录日志"""
    db_total = count(table, where)
    logger.info("一致性核对: %s(WHERE %s) DB=%d vs API=%d", table, where or "-", db_total, api_total)
    assert db_total == api_total, f"数据一致性失败: {table} 数据库 {db_total} 条 != 接口 {api_total} 条"
