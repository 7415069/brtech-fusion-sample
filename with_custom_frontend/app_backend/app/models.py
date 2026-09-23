# /app/models.py
"""
brtech 底座二次开发 - 数据模型样例

本文件包含两个示例模型，字段名以注解类型命名，不含任何业务语义：
  1. SampleNormalModel   — 普通模型 (StringPKeyModel)
  2. SampleRecurseModel   — 递归树模型 (StringPKeyRecurseModel)

每个字段的 prop 直接反映其演示的注解/组件类型，方便作为拷贝模板使用。
"""
from typing import Annotated

from sqlalchemy import String, Integer, Text, DateTime, JSON
from sqlmodel import Field as SQLModelField

from brtech_backend.core.annotations import (
  FieldOption, UIComponent, DataOption,
  Action, StandardAdd, StandardEdit, StandardDetail, StandardDelete,
  ui_config, EnableQuery, QueryType, Dictionary, StoreType,
)
from brtech_backend.core.enums import ActionType, PayloadLocation
from brtech_backend.core.extra.sqlmodel_extra import ExtraSQLModelField
from brtech_backend.core.models import StringPKeyModel, StringPKeyRecurseModel


# =============================================================
# 模型一：普通模型 — 演示各种字段注解
# =============================================================

@ui_config(
    module_name="普通模型样例",
    action_column_width=280,
    layout=[
      # 按组件类型分组展示
      "string_field", "int_field", "select_field", "date_field",
      FieldOption(prop="lob_string_field", span=24),
      "switch_field", "color_field",
      FieldOption(prop="treeselect_field", span=12),
      FieldOption(prop="tag_field", span=12),
      FieldOption(prop="image_field", span=12),
      FieldOption(prop="json_field", span=12),
      # 系统字段（通常隐藏）
      FieldOption(prop="create_person", table_show=False, add_show=False, edit_show=False, search_show=False, detail_show=False, span=6),
      FieldOption(prop="create_timestamp", table_show=False, add_show=False, edit_show=False, search_show=False, span=6),
      FieldOption(prop="update_person", table_show=False, add_show=False, edit_show=False, search_show=False, detail_show=False, span=6),
      FieldOption(prop="update_timestamp", table_show=False, add_show=False, edit_show=False, search_show=False, span=6),
      FieldOption(prop="remark", span=24),
    ],
    page_actions=[StandardAdd(dialog_width="900px")],
    row_actions=[
      StandardDetail(dialog_width="900px"),
      StandardEdit(dialog_width="900px"),
      StandardDelete(),
      Action(
          code="sample_custom_action", label="自定义操作", icon="View",
          type=ActionType.API,
          api_url="/normal/customAction/{modelId}",
          method="POST",
          payload_location=PayloadLocation.PATH,
      ),
    ],
)
class SampleNormalModel(StringPKeyModel, table=True):
  """普通模型 — 演示 StringPKeyModel 及常用注解组合"""
  __tablename__ = "sample_normal"

  # ── 字符串输入框 ──
  string_field: Annotated[
    str | None,
    FieldOption(table_show=True, add_show=True, edit_show=True, detail_show=True,
                search_show=True, required=True, search_required=False,
                span=12, column_width=300, search_span=9,
                component=UIComponent.INPUT),
    EnableQuery(query_type=QueryType.LIKE),
  ] = SQLModelField(
      description="字符串字段 (INPUT + LIKE 查询)",
      sa_type=String, max_length=256, nullable=False,
      sa_column_kwargs={"name": "string_field", "comment": "字符串字段"},
  )

  # ── 大文本 / 富文本 ──
  lob_string_field: Annotated[
    str | None,
    FieldOption(table_show=False, add_show=True, edit_show=True, detail_show=True,
                search_show=False, required=False,
                component=UIComponent.TEXTAREA, component_props={"rows": 3}),
  ] = SQLModelField(
      description="大文本字段 (RICH_TEXT / TEXTAREA)",
      sa_type=Text, nullable=True,
      sa_column_kwargs={"name": "lob_string_field", "comment": "大文本字段"},
  )

  # ── 数字输入框 ──
  int_field: Annotated[
    int | None,
    FieldOption(table_show=True, add_show=True, edit_show=True, detail_show=True,
                search_show=True, required=False, search_required=False,
                span=8, search_span=6,
                component=UIComponent.INPUT_NUMBER,
                component_props={"min": 0, "max": 999999}),
    EnableQuery(query_type=QueryType.EQ),
  ] = SQLModelField(
      description="整数字段 (INPUT_NUMBER)",
      sa_type=Integer, nullable=True,
      sa_column_kwargs={"name": "int_field", "comment": "整数字段"},
  )

  # ── 下拉选择 (字典翻译) ──
  select_field: Annotated[
    str | None,
    FieldOption(table_show=True, add_show=True, edit_show=True, detail_show=True,
                search_show=True, required=True, search_required=False,
                span=8, search_span=4,
                component=UIComponent.SELECT),
    Dictionary(store_type=StoreType.DICTIONARY_VALUE,
               dictionary_type="sample_select_type",
               display_field_name="select_field_display"),
    EnableQuery(query_type=QueryType.EQ),
  ] = SQLModelField(
      default="option_1",
      description="下拉选择字段 (SELECT + Dictionary 翻译)",
      sa_type=String, max_length=36, nullable=False,
      sa_column_kwargs={"name": "select_field", "comment": "下拉选择字段"},
  )
  select_field_display: Annotated[
    str | None,
    FieldOption(table_show=False, add_show=False, edit_show=False, detail_show=False, search_show=False),
  ] = ExtraSQLModelField(description="下拉选择字段显示值", sa_column_exclude=True)

  # ── 开关 ──
  switch_field: Annotated[
    str | None,
    FieldOption(table_show=True, add_show=True, edit_show=True, detail_show=True,
                search_show=True, required=False, search_required=False,
                span=6, search_span=4,
                component=UIComponent.SWITCH),
    Dictionary(store_type=StoreType.DICTIONARY_VALUE,
               dictionary_type="yes_no",
               display_field_name="switch_field_display"),
    EnableQuery(query_type=QueryType.EQ),
  ] = SQLModelField(
      default="0",
      description="开关字段 (SWITCH + yes_no 字典)",
      sa_type=String, max_length=4, nullable=False,
      sa_column_kwargs={"name": "switch_field", "comment": "开关字段"},
  )
  switch_field_display: Annotated[
    str | None,
    FieldOption(table_show=False, add_show=False, edit_show=False,
                detail_show=False, search_show=False),
  ] = ExtraSQLModelField(description="开关字段显示值", sa_column_exclude=True)

  # ── 日期选择 ──
  date_field: Annotated[
    str | None,
    FieldOption(table_show=True, add_show=True, edit_show=True, detail_show=True,
                search_show=True, required=False, search_required=False,
                span=8, search_span=5,
                component=UIComponent.DATE_PICKER,
                component_props=FieldOption.DatePickerComponentProps(type="date")),
  ] = SQLModelField(
      description="日期字段 (DATE_PICKER + 范围查询)",
      sa_type=DateTime, nullable=True,
      sa_column_kwargs={"name": "date_field", "comment": "日期字段"},
  )

  # ── 图片上传 ──
  image_field: Annotated[
    str | None,
    FieldOption(table_show=False, add_show=True, edit_show=True, detail_show=True,
                search_show=False,
                component=UIComponent.IMAGE,
                component_props=FieldOption.UploadComponentProps(
                    accept="image/*", max_size=10, limit=1,
                )),
  ] = SQLModelField(
      description="图片字段 (IMAGE / UPLOAD)",
      sa_type=String, max_length=256, nullable=True,
      sa_column_kwargs={"name": "image_field", "comment": "图片字段"},
  )

  # ── 树选择 (引用递归模型) ──
  tree_select_field: Annotated[
    str | None,
    FieldOption(table_show=True, add_show=True, edit_show=True, detail_show=True,
                search_show=True, required=False, search_required=False,
                span=8, search_span=6,
                component=UIComponent.TREE_SELECT,
                data_option=DataOption(
                    model_cls="SampleRecurseModel",
                    lazy_load=True, method="POST",
                    path="/recurse/query/all",
                    label_field="label", value_field="model_id",
                )),
    EnableQuery(query_type=QueryType.EQ),
  ] = SQLModelField(
      description="树选择字段 (TREE_SELECT，引用递归模型)",
      sa_type=String, max_length=36, nullable=True,
      sa_column_kwargs={"name": "tree_select_field", "comment": "树选择字段"},
  )

  # ── JSON 编辑器 ──
  json_field: Annotated[
    list | None,
    FieldOption(table_show=False, add_show=True, edit_show=True, detail_show=True,
                search_show=False,
                component=UIComponent.JSON_EDITOR,
                component_props={"rows": 6}),
  ] = SQLModelField(
      default=None,
      description="JSON 字段 (JSON_EDITOR)",
      sa_type=JSON, nullable=True,
      sa_column_kwargs={"name": "json_field", "comment": "JSON 字段"},
  )

  # ── 颜色选择 ──
  color_field: Annotated[
    str | None,
    FieldOption(table_show=True, add_show=True, edit_show=True, detail_show=True,
                search_show=False, required=False, span=6,
                component=UIComponent.COLOR_PICKER,
                component_props=FieldOption.ColorPickerComponentProps(
                    showAlpha=True, colorFormat="hex", style={"width": "32px"},
                )),
  ] = SQLModelField(
      description="颜色字段 (COLOR_PICKER)",
      sa_type=String, max_length=32, nullable=True,
      sa_column_kwargs={"name": "color_field", "comment": "颜色字段"},
  )

  # ── 标签输入 ──
  tag_field: Annotated[
    list[str] | None,
    FieldOption(table_show=False, add_show=True, edit_show=True, detail_show=True,
                search_show=False,
                component=UIComponent.INPUT_TAG),
  ] = SQLModelField(
      default=None,
      description="标签字段 (TAG_INPUT)",
      sa_type=JSON, nullable=True,
      sa_column_kwargs={"name": "tag_field", "comment": "标签字段"},
  )


# =============================================================
# 模型二：递归模型 — 树形结构
# =============================================================

@ui_config(
    module_name="递归模型样例",
    search_span=8,
    tree_table=True,
    load_uri="/query/all",
    load_lazy=True,
    action_column_width=200,
    layout=[
      "label", "code", "sort_order",
      FieldOption(prop="parent_id", label="父节点", show=True, table_show=False,
                  span=12, search_span=8,
                  component=UIComponent.TREE_SELECT,
                  data_option=DataOption(
                      lazy_load=True, method="POST",
                      path="/query/all",
                      label_field="label", value_field="model_id",
                  )),
      FieldOption(prop="create_person", table_show=False, add_show=False, edit_show=False, search_show=False, detail_show=False, span=6),
      FieldOption(prop="create_timestamp", table_show=False, add_show=False, edit_show=False, search_show=False, span=6),
      FieldOption(prop="update_person", table_show=False, add_show=False, edit_show=False, search_show=False, detail_show=False, span=6),
      FieldOption(prop="update_timestamp", table_show=False, add_show=False, edit_show=False, search_show=False, span=6),
      FieldOption(prop="remark", span=24),
    ],
    table_layout=["label"],
    page_actions=[StandardAdd(dialog_width="600px")],
    row_actions=[
      StandardDetail(dialog_width="600px"),
      StandardEdit(dialog_width="600px"),
      StandardDelete(),
    ],
)
class SampleRecurseModel(StringPKeyRecurseModel, table=True):
  """递归模型 — 演示 StringPKeyRecurseModel 树形结构"""
  __tablename__ = "sample_recurse"

  label: Annotated[
    str | None,
    FieldOption(table_show=True, add_show=True, edit_show=True, detail_show=True,
                search_show=True, required=True, search_required=False,
                span=12, search_span=8,
                component=UIComponent.INPUT),
    EnableQuery(query_type=QueryType.LIKE),
  ] = SQLModelField(
      description="节点名称",
      sa_type=String, max_length=128, nullable=False,
      sa_column_kwargs={"name": "label", "comment": "节点名称"},
  )

  code: Annotated[
    str | None,
    FieldOption(table_show=True, add_show=True, edit_show=True, detail_show=True,
                search_show=True, required=True, search_required=False,
                span=8, search_span=6,
                component=UIComponent.INPUT),
    EnableQuery(query_type=QueryType.EQ),
  ] = SQLModelField(
      description="节点编码 (唯一)",
      sa_type=String, max_length=64, nullable=False,
      sa_column_kwargs={"name": "code", "comment": "节点编码"},
  )

  sort_order: Annotated[
    int | None,
    FieldOption(table_show=True, add_show=True, edit_show=True, detail_show=True,
                search_show=False, required=False,
                component=UIComponent.INPUT_NUMBER,
                component_props={"min": 0}),
  ] = SQLModelField(
      default=0,
      description="排序号",
      sa_type=Integer, nullable=False,
      sa_column_kwargs={"name": "sort_order", "comment": "排序号"},
  )
