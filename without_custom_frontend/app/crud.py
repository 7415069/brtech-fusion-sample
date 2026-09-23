# /app/crud.py
"""
数据访问层 (CRUD) — 演示 CRUD 基类的使用

不需要任何业务逻辑，继承即用。
"""
from brtech_backend.core.crud import StringPKeyCrud, StringPKeyRecurseCrud

from .models import SampleNormalModel, SampleRecurseModel


class SampleNormalCrud(StringPKeyCrud[SampleNormalModel]):
    """普通模型 CRUD"""
    pass


class SampleRecurseCrud(StringPKeyRecurseCrud[SampleRecurseModel]):
    """递归模型 CRUD（自动处理树形结构）"""
    pass
