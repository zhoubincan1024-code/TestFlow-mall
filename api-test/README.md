# TestFlow-Mall 接口自动化测试框架

基于 **Pytest + Requests** 的 mall 电商后台接口自动化测试框架。

## 目录结构

```text
api-test/
├── config.py            # 环境配置（BASE_URL、登录账号、数据库）
├── conftest.py          # Pytest fixtures（session、token、RBAC 账号）+ Allure 自动装饰
├── pytest.ini           # Pytest 配置
├── requirements.txt     # 依赖
├── api/                 # 接口对象封装（auth / product / order / market / perm）
├── utils/               # 通用工具（日志、HTTP 封装、数据库断言 db.py）
├── tests/               # 测试用例（login / product / order / market / permission / db_consistency / auth）
└── logs/                # 运行日志（api_test.log，滚动）
```

## 快速开始

```bash
cd api-test
pip install -r requirements.txt
pytest                          # 运行全部用例
pytest tests/test_login.py -v   # 运行单个文件
pytest -k "login"               # 按关键字过滤
pytest --html=../reports/api_test_report.html   # 生成 HTML 报告
```

## 核心机制

| 机制 | 实现 |
|---|---|
| Token 关联 | `conftest.py` 中 `admin_token` fixture（session 级）登录 admin/macro123 获取 token，`authed_client` 自动携带 |
| 请求封装 | `utils/http_client.py` 统一组装 URL/请求头/超时，并记录每次请求日志 |
| 日志 | `utils/logger.py` 控制台 INFO + 文件 DEBUG（logs/api_test.log，1MB 滚动保留 5 份） |
| 参数化 | 登录成功/失败用例使用 `@pytest.mark.parametrize` 数据驱动 |
| 数据库一致性 | `utils/db.py`（PyMySQL）统计表行数并与接口分页 total 交叉断言；列表接口过滤逻辑删除（delete_status=0） |
| RBAC 越权测试 | productAdmin/orderAdmin 独立 token，验证跨模块访问返回业务码 403 |
| 断言口径 | mall 统一返回 HTTP 200 + 业务码（`code` 字段）：200 成功 / 401 未登录或路径不存在 / 403 无权限 / 404 账号不存在 / 500 密码错误 |

## 用例清单（41 条）

| 文件 | 条数 | 覆盖内容 |
|---|---|---|
| test_login.py | 7 | 正常登录（admin/test 参数化）、错误密码/不存在账号/空账号、admin/info |
| test_product.py | 6 | 商品列表、名称搜索、分类筛选、品牌、商品分类（/list/0）、商品类型 |
| test_order.py | 4 | 订单列表、订单号查询、状态筛选、订单详情 |
| test_market.py | 4 | 秒杀活动（/flash/list）、优惠券（/coupon/list）、广告（/home/advertise/list）、人气推荐 |
| test_permission.py | 9 | 用户/角色/菜单树/菜单分页/admin 角色/资源点 + 超级管理员全访问、商品管理员/订单管理员越权 403 |
| test_db_consistency.py | 8 | 商品/订单/用户/分类/优惠券/广告/角色/资源 接口 total == DB COUNT |
| test_auth.py | 3 | 无 token 401、无效 token 401、有效 token 200 |

## 被测系统要求

- mall-admin 后端运行在 `http://localhost:8080`（含 MySQL + Redis）
- 数据库已导入 `mall.sql` 种子数据（商品 20 / 订单 48 / 用户 8 / 分类 6 / 优惠券 5 / 广告 11，均为未逻辑删除口径）
- 营销/权限接口路径以 `mall-admin-web/src/apis` 前端源码为准（如 `/flash/list` 而非 `/sms/flashPromotion/list`、`/menu/treeList`）

## M8：Allure 报告 + GitHub Actions CI

### 本地生成 Allure 报告

```bash
cd api-test
pip install -r requirements.txt
python -m pytest --alluredir=allure-results --clean-alluredir -q
# 生成静态报告（Windows 已下载 allure CLI）
& "C:\Users\zhoub\tools\allure-2.30.0\bin\allure.bat" generate allure-results -o reports\allure-report --clean
```

Allure 报告特性：按模块（登录/商品/订单/营销/权限/数据库一致性）分层的 epic → feature 结构，无需修改任何用例文件（由 `conftest.py` 的 `pytest_collection_modifyitems` 自动装饰）。

### GitHub Actions 自动回归

- Workflow：`.github/workflows/api-ci.yml`
- 触发：`api-test/**` 或 workflow 变更 push / PR；支持 `workflow_dispatch` 手动触发
- 流程：起 MySQL 8 / Redis 7 容器 → 检出被测系统 mall（**锁定 commit `0504e86b`**）→ 导入 `mall.sql` 种子数据 → 构建并启动 mall-admin → 执行 41 条用例（含数据库一致性断言）→ Allure 报告上传为 artifact
- 关键点：种子数据已验证与本地基线一致；后端启动用命令行参数覆盖 `spring.datasource.*`（JDBC URL 加 `allowPublicKeyRetrieval=true`）；JDK 17 + Maven 依赖缓存
