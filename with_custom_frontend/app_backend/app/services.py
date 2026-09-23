# /app/services.py
"""
业务逻辑层 (Service) — 演示 Service 基类的生命周期钩子

pre_create / post_create / pre_update / post_update / pre_delete / post_delete
等钩子可用于数据校验、自动填充、级联操作等。
"""
from brtech_backend.core.services import StringPKeyRecurseService, StringPKeyService
from brtech_backend.dictionary.services import StringPKeyWithDictionaryService

from .crud import SampleNormalCrud, SampleRecurseCrud
from .models import SampleNormalModel, SampleRecurseModel
from .schemas import SampleNormalQuery, SampleRecurseQuery


class SampleNormalService(StringPKeyWithDictionaryService[
    SampleNormalModel, SampleNormalCrud, SampleNormalQuery
]):
    """普通模型 Service — 演示生命周期钩子和自定义业务方法"""

    async def pre_create(self, user_id: str, model: SampleNormalModel) -> None:
        """创建前：为 select_field 设默认值"""
        await super().pre_create(user_id, model)
        if not model.select_field:
            model.select_field = "option_1"

    async def custom_action(self, user_id: str, model_id: str) -> str | None:
        """自定义业务方法 — 可由 API 路由调用"""
        model = await self.get(user_id, model_id)
        if not model:
            return None
        preview = (model.lob_string_field or "")[:200]
        return preview if preview else f"string_field = {model.string_field}"


class SampleRecurseService(StringPKeyWithDictionaryService[
    SampleRecurseModel, SampleRecurseCrud, SampleRecurseQuery
]):
    """递归模型 Service — 演示编码唯一性校验"""

    async def pre_create(self, user_id: str, model: SampleRecurseModel) -> None:
        """创建前：校验 code 全局唯一"""
        await super().pre_create(user_id, model)
        if model.code:
            existing = await self.query_all(user_id, SampleRecurseQuery(code=model.code))
            if existing:
                from fastapi import HTTPException
                raise HTTPException(status_code=400, detail=f"编码 '{model.code}' 已存在")

    async def pre_update(self, user_id: str, old_model: SampleRecurseModel,
                         new_model: SampleRecurseModel,
                         update_fields: set[str]) -> None:
        """更新前：校验 code 唯一（排除自身）"""
        await super().pre_update(user_id, old_model, new_model, update_fields)
        if "code" in update_fields and new_model.code:
            existing = await self.query_all(user_id, SampleRecurseQuery(code=new_model.code))
            for item in existing:
                if item.model_id != old_model.model_id:
                    from fastapi import HTTPException
                    raise HTTPException(status_code=400, detail=f"编码 '{new_model.code}' 已被其他节点使用")
