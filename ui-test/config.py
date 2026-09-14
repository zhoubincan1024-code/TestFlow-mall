# -*- coding: utf-8 -*-
"""UI 自动化测试环境配置（被测前端 mall-admin-web，Vite dev server）"""
import os

FRONTEND_URL = os.getenv("MALL_WEB_URL", "http://localhost:5173")
LOGIN_URL = f"{FRONTEND_URL}/#/login"

# 登录账号（与接口层一致）
ADMIN_USERNAME = os.getenv("MALL_ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("MALL_ADMIN_PASS", "macro123")

# 浏览器配置
HEADLESS = os.getenv("UI_HEADLESS", "1") == "1"
BROWSER_WIDTH = 1440
BROWSER_HEIGHT = 900
WAIT_TIMEOUT = 15  # 秒，显式等待

# 截图目录（失败用例自动截图）
SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")
