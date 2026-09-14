# TestFlow — Mall 电商系统软件测试作品集

[![API 接口自动化回归](https://github.com/zhoubincan1024-code/TestFlow-mall/actions/workflows/api-ci.yml/badge.svg)](https://github.com/zhoubincan1024-code/TestFlow-mall/actions/workflows/api-ci.yml)

> 一个面向 2026 软件测试校招的端到端测试实战项目：从本地部署、功能用例设计、接口/UI 自动化、性能测试到 CI/CD，完整复刻企业级测试交付链路。

---

## 项目概览

| 项 | 内容 |
|---|---|
| 被测系统 | [macrozheng/mall](https://github.com/macrozheng/mall) 电商后台（Spring Boot 3.5 / JDK 17）+ mall-admin-web（Vue3 + Element Plus） |
| 测试对象 | 后台管理系统（商品 / 订单 / 营销 / 权限四大模块） |
| 技术栈 | Python 3.12 · Pytest · Requests · Selenium 4 · PyMySQL · JMeter 5.6 · GitHub Actions · Allure |
| CI 流水线 | 每次 push 自动在云端起 MySQL8 + Redis7 容器 → 锁定被测系统 commit → 构建启动 → 执行 41 条接口用例 → 生成 Allure 报告 |

## 里程碑（M1–M8）

| 阶段 | 内容 | 产出 |
|---|---|---|
| M1 | 本地部署与环境基线 | `本地部署说明.md`（MySQL 认证修复 / bcprov 签名修复） |
| M2 | 功能模块分析 + 测试计划 + 缺陷发现 | `docs/功能模块分析.md`、`docs/测试计划.md`、BUG-001 |
| M3 | 功能测试用例设计 | `test-data/功能测试用例.xlsx`（100 条，含缺陷复现用例） |
| M4 | 接口自动化框架 | `api-test/`（41 条：Token 关联 / RBAC 越权 / 数据库一致性） |
| M5 | UI 自动化框架 | `ui-test/`（Selenium + POM，10 条） |
| M6 | 性能测试与调优实战 | `docs/性能测试报告.md`（jstack 定位 Lettuce 共享连接锁瓶颈） |
| M7 | 测试总结报告 | `docs/测试总结报告.md`（M1–M6 全链路串联） |
| M8 | CI/CD | `.github/workflows/api-ci.yml` + Allure 报告 artifact |

## 关键数据

- 接口自动化：**41/41 通过**（本地 + 云端 CI 双环境验证）
- UI 自动化：**10/10 通过**
- 性能压测：2020 样本 / 0 错误 / 总 TPS 102.42
- 性能优化：商品列表 TPS 37~51 → **89.32**（+75%~140%），根因定位到 `LettuceConnectionFactory.doInLock` 全局 ReentrantLock
- 缺陷发现：BUG-001（商品列表前端路由渲染异常），含三层定位法与缺陷用例化

## 目录结构

```
TestFlow-mall/
├── .github/workflows/api-ci.yml   # GitHub Actions CI 流水线
├── api-test/                     # 接口自动化框架（Pytest + Allure）
│   ├── api/                      #   API 封装
│   ├── tests/                    #   41 条用例（登录/商品/订单/营销/权限）
│   ├── utils/                    #   DB 断言 / 日志
│   ├── conftest.py               #   Token 关联 + Allure 标签
│   └── requirements.txt
├── ui-test/                      # UI 自动化（Selenium + POM）
├── docs/
│   ├── 测试计划.md
│   ├── 功能模块分析.md
│   ├── 测试总结报告.md
│   └── 性能测试报告.md
├── test-data/
│   └── 功能测试用例.xlsx          # 100 条功能用例
└── README.md
```

## CI 状态徽章

本仓库根 README 顶部已嵌入 GitHub Actions 状态徽章，打开 Actions 页面可查看每次运行的 Allure 报告 artifact（`allure-report` 与 `allure-results` 两个产物）。

> 注：当前仓库为私有，徽章在 GitHub 页面内可见；转公开后徽章将对外可访问。
