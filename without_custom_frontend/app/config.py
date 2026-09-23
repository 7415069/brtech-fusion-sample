# /app/config.py
"""
brtech 底座二次开发 - 应用配置

继承 AppSettings 按需重写默认配置。
可通过环境变量或 .env 文件覆盖。
"""
from brtech_backend.core.config import AppSettings


class SampleAppSettings(AppSettings):
    """样例应用配置

    此配置继承 AppSettings 的所有默认字段，
    可按需覆盖：
      - 应用元信息 (TITLE, DESCRIPTION, VERSION)
      - 数据库连接 (DATABASE_URL)
      - JWT 密钥 (JWT_SECRET_KEY)
      - OSS 存储 (OSS_ENDPOINT, OSS_ACCESS_KEY, ...)
      - 功能开关 (ENABLE_CAPTCHA, AI_ENABLE, ...)
    """
    # --- 应用信息 ---
    TITLE: str = "博然低代码平台 - 二次开发样例"
    LOGO: str = "static/favicon.svg"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "基于 博然低代码平台 进行二次开发的样例项目 - API 文档"

    LOGIN_TITLE: str = "欢迎使用"
    LOGIN_SUBTITLE: str = TITLE
    LOGIN_LOGO: str = LOGO

    # --- 功能开关 ---
    ENABLE_CAPTCHA: bool = False
    ENABLE_REGISTER: bool = True
    ENABLE_FORGOT_PASSWORD: bool = True

    # --- 主题 ---
    THEME_NAME: str = "light"
    THEME_PRIMARY_COLOR: str = ""
    THEME_BORDER_RADIUS: str = "10px"
    COPYRIGHT: str = "© 2026 博然低代码平台"
    ICP_CODE: str = ""

    # --- 邮件 ---
    MAIL_ENABLE: bool = True
    MAIL_SERVER: str = "smtp.163.com"
    MAIL_PORT: int = 465
    MAIL_USERNAME: str = ""
    MAIL_FROM_NAME: str = "brtech-sample"

    # --- 网络 ---
    PORT: int = 9876

    # --- 日志 ---
    LOG_LEVEL: str = "INFO"

    # --- 路径 ---
    CONTEXT_PATH: str = "/sample"
    UI_PATH: str = "/frontend"
    API_PREFIX: str = "/api/v1"
    ROOT_PATH: str = ""
    INIT_DATA_DIR: str = "fixtures"

    # --- OSS 存储 (MinIO / S3) ---
    OSS_ENDPOINT: str = "localhost:9000"
    OSS_ACCESS_KEY: str = "root"
    OSS_SECRET_KEY: str = ""
    OSS_BUCKET_NAME: str = "sample-bucket"
    OSS_SECURE: bool = False

    # --- 数据库 ---
    # SQLite (开发)
    DATABASE_URL: str = "sqlite+aiosqlite:///var/sample.db"
    # PostgreSQL (生产)
    # DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/sample"

    JWT_SECRET_KEY: str = "change-me-to-a-random-secret"

    # --- AI 功能 ---
    AI_ENABLE: bool = False

    # --- 支付 ---
    ENABLE_WALLET_PAYMENT: bool = False
    ENABLE_MOCK_PAYMENT: bool = False

    # --- 权限 ---
    ENABLE_DATA_PERMISSION_VALIDATION: bool = True
    ENABLE_FUNC_PERMISSION_VALIDATION: bool = True


sample_app_settings = SampleAppSettings()
