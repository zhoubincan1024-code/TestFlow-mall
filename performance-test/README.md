# performance-test 性能测试模块（M6）

JMeter 性能测试：登录并发 50 / 商品列表并发 100 / 混合 8:2，指标 TPS / P95 / 错误率。

## 运行方式

```powershell
$env:JAVA_HOME = "C:\Program Files\Java\jdk-17"
& "C:\Users\zhoub\tools\apache-jmeter-5.6.3\bin\jmeter.bat" -n `
  -t mall_perf.jmx -l results.jtl -e -o report `
  -j C:\Users\zhoub\tools\jmeter_run.log
```

- JMeter 5.6.3 从阿里云镜像下载（archive.apache.org 直连极慢）：
  `https://mirrors.aliyun.com/apache/jmeter/binaries/apache-jmeter-5.6.3.zip`
- 修改场景参数（线程数/循环数）编辑 `C:\Users\zhoub\tools\gen_jmx.py` 后重新生成 JMX。

## 场景设计

| 场景 | 线程 | 循环 | 请求 |
|---|---|---|---|
| 登录并发50 | 50 | 10 | 仅登录（稳态 TPS） |
| 商品列表并发100 | 100 | 5 | 仅一次控制器登录 + 商品列表 |
| 混合8:2 | 80 + 20 | 10 / 5 | 登录组纯登录；商品组登录取 token + 商品列表 |

- token 关联：登录响应 `$.data.token` 由 JSON 提取器存入 `login_token`，商品请求头 `Authorization: Bearer ${login_token}`。
- 断言：响应体包含 `"code":200`（mall 业务码，HTTP 200 不代表业务成功）。

## 踩坑记录

1. **JMX 加载 ClassCastException（HeaderManager cannot be cast to HashTree）**
   HeaderManager / 断言 / 提取器必须放在 sampler 节点的 `<hashTree>` 子节点层，且每个子节点后跟独立空 `<hashTree/>`；不能放在 sampler 元素内部，也不能与 sampler 平级。
2. **登录 415（Unsupported Media Type）**
   登录请求必须显式配置 `Content-Type: application/json` 请求头（postBodyRaw 原始 body 不会自动带 JSON 头）。
3. **循环控制器嵌套问题**
   循环控制器（LoopController）嵌在线程组循环内时样本量不符合预期（100×5×3 只出 300），简化结构：登录用"仅一次控制器（OnceOnlyController）"，被测请求直接作为线程组循环子节点。
4. **MySQL 认证（Public Key Retrieval is not allowed）**
   MySQL 服务重启后 caching_sha2_password 认证缓存清空导致后端 8080 起不来：
   ```sql
   ALTER USER 'mall'@'localhost' IDENTIFIED WITH mysql_native_password BY 'mall123456';
   FLUSH PRIVILEGES;
   ```
5. **JMeter 需要显式 JAVA_HOME**：`$env:JAVA_HOME = "C:\Program Files\Java\jdk-17"`。

## 结果

最终轮：2020 样本 / 0 错误 / 总 TPS 102.42
- 登录 P95 77ms（目标 <500ms ✅），商品 P95 8~9ms（✅）
- 登录 TPS 48.42~78.44（目标 ≥50，场景1 差 3.2% 含 ramp 开销）
- 商品 TPS 25.52（目标 ≥100 未达，瓶颈分析见 `../docs/性能测试报告.md` 第 4 节）

## 优化复测（2026-09-09）

商品列表 100 并发持续负载（ramp 5s × 循环 20 = 2000 样本）：

| 配置 | 商品 TPS | avg | P95 |
|---|---|---|---|
| 默认（基线） | 37~51 | 4~6s | ~7s |
| 连接池 200 + 日志降级（保留） | **89.32** | **973ms** | **1643ms** |
| Lettuce pool（已回退） | 14 | 6.4s | ~9s |

- 优化：Druid 连接池 20→200 + 日志级别降级（SQL DEBUG、WebLogAspect 全量 JSON 日志关闭），通过 `mall-overrides.yml` 外部覆盖，无需重新打包
- 瓶颈：jstack 证实 100 并发下全部线程阻塞于 `LettuceConnectionFactory.doInLock`（Lettuce 共享连接全局锁），JWT 过滤器每请求 1~2 次 Redis 操作被串行化；免认证 actuator 接口 100 并发 TPS 295 佐证
- 剩余优化属代码层：换 Jedis / 正确配置 Lettuce 连接池 / 减少 JWT 过滤器 Redis 调用 / 商品列表加 Redis 缓存
- 启动命令（带优化配置）：`java -jar mall-admin.jar --spring.config.additional-location=file:C:\Users\zhoub\tools\mall-overrides.yml`
