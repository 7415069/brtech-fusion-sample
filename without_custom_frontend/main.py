# /main.py
"""
brtech 底座二次开发 - 应用入口

本文件演示：
  - 如何创建 Application 实例
  - 如何注册业务路由
  - 如何集成底座提供的模块（4A权限、字典、审计日志、任务、支付等）
  - 如何配置 OSS 存储
"""
import logging
from brtech_backend import get_session_maker
from brtech_backend.a4.routers import (
    A4UserRouter, A4RoleRouter, A4FuncPermissionRouter, A4DataPermissionRouter,
    A4RoleUserRouter, A4RoleFuncPermissionRouter, A4RoleDataPermissionRouter, A4RoleUserActionRouter,
)
from brtech_backend.a4.scanner import A4PermissionScanner
from brtech_backend.core.application import Application
from brtech_backend.core.config import app_settings
from brtech_backend.core.config import install_all_settings
from brtech_backend.core.routers import Public
from brtech_backend.core.storage import MinioStorageClient, StorageProvider
from brtech_backend.dictionary.routers import DictionaryRouter, DictionaryRouteKey
from brtech_backend.logger.middlewares import OperateLogMiddleware
from brtech_backend.logger.routers import a4_logger_router_classes
from brtech_backend.payment.routers import payment_router_classes
from brtech_backend.task.routers import TaskRecordRouter
from brtech_backend.ui.routers import ui_router_classes
from typing import Any

from app.config import sample_app_settings
from app.routers import sample_router_classes

Public(DictionaryRouteKey.QUERY_BY_TYPES)(DictionaryRouter)

logger = logging.getLogger("application")


class SampleApplication(Application):
    """样例 Application"""

    def __init__(self, settings: Any, router_classes=None, **kwargs):
        install_all_settings(sample_app_settings)
        super().__init__(settings, router_classes, **kwargs)

    def prepare(self):
        super().prepare()

        StorageProvider.set(MinioStorageClient(
            endpoint=app_settings.OSS_ENDPOINT,
            access_key=app_settings.OSS_ACCESS_KEY,
            secret_key=app_settings.OSS_SECRET_KEY,
            bucket_name=app_settings.OSS_BUCKET_NAME,
            secure=app_settings.OSS_SECURE,
        ))

        self.app.add_middleware(OperateLogMiddleware)

        # 系统模块路由
        self.router_classes.append(DictionaryRouter)
        self.router_classes.extend(a4_logger_router_classes)
        self.router_classes.extend([
            A4UserRouter, A4RoleRouter,
            A4FuncPermissionRouter, A4DataPermissionRouter,
            A4RoleUserRouter, A4RoleFuncPermissionRouter, A4RoleDataPermissionRouter, A4RoleUserActionRouter
        ])
        self.router_classes.extend(payment_router_classes)
        self.router_classes.extend(ui_router_classes)
        self.router_classes.extend([TaskRecordRouter])

        # 业务模块路由
        self.router_classes.extend(sample_router_classes)

    async def on_startup(self):
        await super().on_startup()
        session_maker = get_session_maker()
        async with session_maker() as db:
            logger.info(">>> [System] 正在自动同步接口权限...")
            await A4PermissionScanner.sync_to_db(self.app, db, self.api_prefix)


creator = SampleApplication(app_settings)
app = creator.get_app()

if __name__ == "__main__":
    creator.run(app_str="main:app", reload_dirs=["app"], reload=False)
