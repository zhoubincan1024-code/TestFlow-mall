# TestFlow-Mall UI 自动化测试框架

基于 **Selenium + POM（Page Object Model）** 的 mall 电商后台 UI 自动化测试框架，浏览器为 Chrome（headless）。

## 目录结构

```text
ui-test/
├── config.py          # 环境配置（前端地址、账号、浏览器、超时）
├── conftest.py        # fixtures：driver（失败自动截图）、logged_in_driver（已登录会话）
├── pytest.ini
├── pages/             # POM 页面对象
│   ├── base_page.py   # 基类：显式等待、输入/点击/断言辅助
│   ├── login_page.py  # 登录页（input[name=username/password]、登录按钮、表单校验）
│   └── home_page.py   # 布局页（侧边栏菜单导航）
├── tests/             # 10 条用例（login 4 / home 4 / order 2）
├── screenshots/       # 失败用例自动截图
└── logs/              # 运行日志
```

## 运行

```bash
cd ui-test
pip install selenium webdriver-manager
pytest                          # 全部用例（约 1 分钟）
pytest tests/test_login_ui.py   # 单文件
pytest --html=../reports/ui_test_report.html --self-contained-html
```

前置条件：后端（8080）、Redis（6379）、前端 dev server（5173）均在运行，数据库已导入种子数据。

## 用例清单（10 条）

| 文件 | 条数 | 覆盖内容 |
|---|---|---|
| test_login_ui.py | 4 | 登录成功跳转、错误密码停留、短密码表单校验、未登录访问重定向 |
| test_home_ui.py | 4 | 侧边栏五大模块、看板卡片（今日订单总数/销售总额）、导航到订单列表、导航到优惠券 |
| test_order_ui.py | 2 | 订单表种子数据、表头字段 |

## 关键工程点

| 问题 | 处理 |
|---|---|
| Element Plus 受控输入框 | `clear()` 不触发 v-model 更新导致值拼接（adminadmin），改用 **Ctrl+A 全选覆盖** |
| EP 表单校验异步渲染 | 错误消息用显式等待后再读取 |
| 折叠菜单 | 子菜单导航前先点击一级菜单展开（订单→订单列表、营销→优惠券列表） |
| 环境不稳定 | 后端进程曾中途退出导致"Network Error"，重启后恢复——记录为环境风险 |
| BUG-001 | 商品列表页 `#/pms/product` 前端路由渲染异常（已知缺陷），UI 用例暂不进入该页面，后续可写缺陷复现用例 |
