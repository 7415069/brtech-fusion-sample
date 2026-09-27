# /app/routers.py
"""
API 路由层 — 演示 Router 基类及自定义路由

自动提供: add / delete / update / find / query/page / query/all / excel/import / excel/export
通过 _register_routes 可添加自定义 API 端点。
"""
from brtech_backend.core.enums import OperateType
from brtech_backend.core.routers import (
    StringPKeyRecurseRouter, StringPKeyRouter,
    RouterMeta, Public, RouteKey,
)
from brtech_backend.core.schemas import RestResponse
from brtech_backend.core.security import AuthContext
from brtech_backend.dictionary.routers import StringPKeyWithDictionaryRouter
from fastapi import Depends, Path

from .crud import SampleNormalCrud, SampleRecurseCrud
from .models import SampleNormalModel, SampleRecurseModel
from .schemas import SampleNormalQuery, SampleRecurseQuery
from .services import SampleNormalService, SampleRecurseService


@Public(RouteKey.FIND_BATCH)
@RouterMeta(prefix="/sampleNormal", tags=["样例 - 普通模型"], module_name="普通模型样例")
class SampleNormalRouter(StringPKeyWithDictionaryRouter[
    SampleNormalModel, SampleNormalCrud, SampleNormalQuery, SampleNormalService
]):
    """普通模型 Router — 演示如何添加自定义 API"""

    def _register_routes(self):
        super()._register_routes()

        @self.router.post(
            "/customAction/{model_id}",
            summary="自定义操作示例",
            openapi_extra=self._operation("自定义操作", OperateType.OTHER),
        )
        async def custom_action(
            model_id: str = Path(..., description="模型 ID"),
            service: SampleNormalService = Depends(self._get_service),
            auth_context: AuthContext = Depends(self.user_dependency),
        ):
            result = await service.custom_action(auth_context.user_id, model_id)
            return RestResponse.success(data=result)


@RouterMeta(prefix="/sampleRecurse", tags=["样例 - 递归模型"], module_name="递归模型样例")
class SampleRecurseRouter(StringPKeyRecurseRouter[
    SampleRecurseModel, SampleRecurseCrud, SampleRecurseQuery, SampleRecurseService
]):
    """递归模型 Router — 自动支持树形操作"""
    pass


sample_router_classes = [
    SampleNormalRouter,
    SampleRecurseRouter,
]
