# TestFlow-Mall

Mall 电商系统**软件测试作品集项目**：以开源电商系统 macrozheng/mall 后台（Spring Boot 3.5 / JDK 17 + Vue3 前端）为被测对象，覆盖测试全链路。

## 里程碑（M1-M8）

| 阶段 | 内容 | 交付物 |
|---|---|---|
| M1 | 本地部署与验证 | `本地部署说明.md` |
| M2 | 功能模块分析 + 测试计划 V1.0 | `docs/功能模块分析.md`、`docs/测试计划.md`（发现 BUG-001） |
| M3 | 100 条功能测试用例 | `test-data/功能测试用例.xlsx` |
| M4 | 接口自动化（41/41 通过） | `api-test/` + Allure 报告 |
| M5 | UI 自动化（10/10 通过） | `ui-test/` |
| M6 | 性能测试与调优（jstack 定位 Lettuce 锁瓶颈） | `docs/性能测试报告.md`、`performance-test/` |
| M7 | 测试总结报告 | `docs/测试总结报告.md` |
| M8 | Allure 报告 + GitHub Actions CI | `.github/workflows/api-ci.yml` |

## 项目亮点

- **缺陷定位方法论**：BUG-001 前端路由渲染异常，三层定位法锁定 vue-router 层；
- **性能调优实战**：100 并发下商品接口 TPS 37-51 → 89.32（连接池+日志优化），jstack 线程栈定位 Lettuce 共享连接全局锁（代码层瓶颈），附对照实验证据；
- **CI 全链路**：GitHub Actions 一键回归（MySQL/Redis 容器 + 锁定 commit 被测系统 + 41 条接口断言 + Allure 报告）。

> 注：`mall/`、`mall-admin-web/` 为被测系统源码（独立开源仓库），未纳入本仓库。
