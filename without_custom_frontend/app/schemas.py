# /app/schemas.py
"""
查询模型 (Query) — 演示自定义查询逻辑

EnableQuery 注解可覆盖 80% 的搜索需求；当需要多字段联合搜索、
范围搜索等复杂逻辑时，通过继承 Query 基类并重写 custom_spec 实现。
"""
from brtech_backend.core.annotations import FieldOption
from brtech_backend.core.models import M
from brtech_backend.core.schemas import StringPKeyRecurseQuery, StringPKeyQuery
from pydantic import Field
from sqlalchemy import Select, asc, desc, or_
from typing import Annotated, Any

from .models import SampleNormalModel, SampleRecurseModel


class SampleNormalQuery(StringPKeyQuery[SampleNormalModel]):
    """
    普通模型查询 — 演示 custom_spec 多字段混合搜索

    新增 mixed_keyword 字段：自动在所有字符串字段上执行 LIKE 搜索。
    """
    mixed_keyword: Annotated[
        str | None,
        FieldOption(show=False, search_show=True, search_span=8),
    ] = Field(default=None, description="多字段混合搜索关键词")

    def __init__(self, /, **data: Any) -> None:
        super().__init__(**data)
        self._skip_fields.add("mixed_keyword")

    def custom_spec(self, stmt: Select, model: type[SampleNormalModel]) -> Select:
        """自定义查询：关键词同时在 string_field 和 lob_string_field 中搜索"""
        stmt = super().custom_spec(stmt, model)
        if self.mixed_keyword:
            kw = f"%{self.mixed_keyword}%"
            stmt = stmt.where(or_(
                model.string_field.like(kw),
                model.lob_string_field.like(kw),
            ))
        return stmt

    def apply_sorting(self, stmt: Select, model: type[M]) -> Select:
        """默认按创建时间降序"""
        return stmt.order_by(desc(getattr(model, 'create_timestamp')))


class SampleRecurseQuery(StringPKeyRecurseQuery[SampleRecurseModel]):
    """递归模型查询 — 演示递归查询基类"""

    def apply_sorting(self, stmt: Select, model: type[M]) -> Select:
        """按 sort_order 升序"""
        return stmt.order_by(asc(getattr(model, 'sort_order')))
