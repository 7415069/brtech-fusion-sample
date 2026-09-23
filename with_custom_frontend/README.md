# brtech 底座二次开发指南

本文档以 `with_custom_frontend` 样例项目为载体，说明如何基于 **brtech-fusion（博然低代码底座）** 进行业务系统的二次开发。

---

## 目录

- [开发流程概览](#开发流程概览)
- [第一步：定义数据模型 (models.py)](#第一步定义数据模型-modelspy)
- [第二步：定义 CRUD (crud.py)](#第二步定义-crud-crudpy)
- [第三步：定义查询模型 (schemas.py)](#第三步定义查询模型-schemaspy)
- [第四步：定义 Service (services.py)](#第四步定义-service-servicespy)
- [第五步：定义 Router (routers.py)](#第五步定义-router-routerspy)
- [第六步：注册到应用入口 (main.py)](#第六步注册到应用入口-mainpy)
- [启动运行](#启动运行)
- [前端集成](#前端集成)
- [翻车急救](#翻车急救)

---

## 开发流程概览

在 brtech 底座上开发一个业务模块，只需 5 步：

```
① 定义 Model  →  ② 定义 Crud  →  ③ 定义 Query  →  ④ 定义 Service  →  ⑤ 定义 Router
```

底座自动完成：数据库建表 → RESTful API 注册 → UI 配置生成 → 权限体系接入。

从头到尾只需要编写 Python 代码，**不需要写一行前端代码** 就能得到一个完整的后台管理界面。

---

## 第一步：定义数据模型 (models.py)

### 模型基类

| 用途 | 基类 | 表特征 |
|------|------|--------|
| 普通业务表 | `StringPKeyModel` | 主键为雪花 ID（字符串） |
| 树形结构表 | `StringPKeyRecurseModel` | 自带 `parent_id` 字段，支持递归 |
| 自增主键表 | `IntegerPKeyModel` | 主键为自增整数 |

### 字段注解

```python
from typing import Annotated
from brtech_backend.core.annotations import (
    FieldOption, UIComponent, EnableQuery, QueryType,
    Dictionary, StoreType, DataOption,
)
from sqlmodel import Field as SQLModelField

class YourModel(StringPKeyModel, table=True):
    __tablename__ = "your_table"

    field_name: Annotated[
        str | None,
        FieldOption(                          # UI 配置
            table_show=True,                   # 表格列
            add_show=True, edit_show=True,     # 新增/编辑表单
            search_show=True,                  # 搜索栏
            span=12,                           # 表单布局列数 (1-24)
            component=UIComponent.INPUT,       # 前端组件
        ),
        EnableQuery(query_type=QueryType.LIKE),  # 搜索方式
    ] = SQLModelField(
        description="字段说明",
        sa_type=String, max_length=255, nullable=False,
    )
```

### 可用组件一览

| 组件 | 用途 | 注解 |
|------|------|------|
| `UIComponent.INPUT` | 文本输入 | `EnableQuery(QueryType.LIKE)` |
| `UIComponent.TEXTAREA` | 多行文本 | 适合备注类字段 |
| `UIComponent.RICH_TEXT` | 富文本编辑器 | 适合大段 HTML 内容 |
| `UIComponent.INPUT_NUMBER` | 数字输入 | `component_props={"min": 0}` |
| `UIComponent.SELECT` | 下拉选择 | + `Dictionary` 字典翻译 |
| `UIComponent.SWITCH` | 开关 | + `yes_no` 字典显示"是/否" |
| `UIComponent.DATE_PICKER` | 日期选择 | `EnableQuery(QueryType.DATE_RANGE)` |
| `UIComponent.IMAGE` | 图片上传 | `component_props=UploadComponentProps(...)` |
| `UIComponent.UPLOAD` | 文件上传 | 同上 |
| `UIComponent.TREE_SELECT` | 树形选择 | + `DataOption` 指定数据源 |
| `UIComponent.JSON_EDITOR` | JSON 编辑器 | 适合存储配置类数据 |
| `UIComponent.COLOR_PICKER` | 颜色选择 | 支持透明度 |
| `UIComponent.TAG_INPUT` | 标签输入 | 存储为 JSON 数组 |
| `UIComponent.SELECT_V2` | 增强下拉 | 支持远程搜索 |

### 字典翻译

```python
select_field: Annotated[
    str | None,
    FieldOption(component=UIComponent.SELECT),
    Dictionary(
        store_type=StoreType.DICTIONARY_VALUE,  # 值存字典表
        dictionary_type="your_dict_type",         # 字典类型编码
        display_field_name="select_field_display",  # 自动生成的显示字段名
    ),
] = ...

# 显示字段（无需存数据库）
select_field_display: Annotated[
    str, FieldOption(table_show=False)
] = ExtraSQLModelField(sa_column_exclude=True)
```

### 关联数据源（下拉/树选择引用其他模型）

```python
ref_id: Annotated[
    str | None,
    FieldOption(
        component=UIComponent.TREE_SELECT,
        data_option=DataOption(
            model_cls="YourReferencedModel",   # 引用的模型类名（字符串）
            lazy_load=True,                     # 懒加载
            path="/prefix/query/all",           # 数据接口路径
            label_field="name",                 # 显示字段
            value_field="model_id",             # 值字段
        ),
    ),
] = SQLModelField(...)
```

### 页面配置

```python
from brtech_backend.core.annotations import (
    ui_config, Action, StandardAdd, StandardEdit,
    StandardDetail, StandardDelete,
)

@ui_config(
    module_name="你的模块名称",     # 前端菜单和标题
    action_column_width=280,
    layout=[                       # 表单布局
        "field1", "field2",
        FieldOption(prop="long_field", span=24),
        # 系统字段通常隐藏
        FieldOption(prop="create_timestamp", table_show=False, add_show=False, ...),
    ],
    page_actions=[StandardAdd()],  # 列表页顶部按钮
    row_actions=[                  # 行操作按钮
        StandardDetail(),
        StandardEdit(),
        StandardDelete(),
        Action(code="custom", label="自定义", icon="View",
               type=ActionType.API, api_url="/prefix/action/{modelId}",
               method="POST", payload_location=PayloadLocation.PATH),
    ],
)
class YourModel(StringPKeyModel, table=True):
    ...
```

### 递归模型特殊配置

```python
@ui_config(
    tree_table=True,     # 树形表格
    load_uri="/query/all",
    load_lazy=True,      # 懒加载
    table_layout=["name"],  # 树形表格只显示名称列
)
class YourTreeModel(StringPKeyRecurseModel, table=True):
    ...
```

---

## 第二步：定义 CRUD (crud.py)

```python
from brtech_backend.core.crud import StringPKeyCrud, StringPKeyRecurseCrud

class YourCrud(StringPKeyCrud[YourModel]):
    """数据访问层 — 继承即用，无需任何代码"""
    pass

class YourTreeCrud(StringPKeyRecurseCrud[YourTreeModel]):
    """递归模型 CRUD — 自动处理树形结构的增删改查"""
    pass
```

如需要自定义查询方法，直接在此编写 SQLAlchemy 语句。

---

## 第三步：定义查询模型 (schemas.py)

```python
class YourQuery(StringPKeyQuery[YourModel]):
    """查询模型 — 按需重写 custom_spec 实现复杂搜索"""

    # 新增自定义查询字段
    mixed_keyword: str | None = Field(default=None)

    def __init__(self, /, **data):
        super().__init__(**data)
        self._skip_fields.add("mixed_keyword")  # 不让底座自动处理

    def custom_spec(self, stmt, model):
        # 先调用父类（处理 EnableQuery 注解的字段）
        stmt = super().custom_spec(stmt, model)
        # 再添加自定义条件
        if self.mixed_keyword:
            stmt = stmt.where(or_(
                model.field1.like(f"%{self.mixed_keyword}%"),
                model.field2.like(f"%{self.mixed_keyword}%"),
            ))
        return stmt

    def apply_sorting(self, stmt, model):
        return stmt.order_by(desc(getattr(model, 'create_timestamp')))
```

---

## 第四步：定义 Service (services.py)

```python
class YourService(StringPKeyWithDictionaryService[
    YourModel, YourCrud, YourQuery
]):
    """业务逻辑层 — 生命周期钩子 + 自定义方法"""

    # --- 生命周期钩子 ---
    async def pre_create(self, user_id, model):
        await super().pre_create(user_id, model)
        # 创建前：设默认值、做校验
        if not model.status:
            model.status = "active"

    async def post_create(self, user_id, model):
        await super().post_create(user_id, model)
        # 创建后：发通知、写日志、触发异步任务

    async def pre_update(self, user_id, old_model, new_model, update_fields: set):
        await super().pre_update(user_id, old_model, new_model, update_fields)
        # 更新前：校验唯一性等

    async def pre_delete(self, user_id, model):
        await super().pre_delete(user_id, model)
        # 删除前：级联清理等

    # --- 自定义业务方法（由 router 调用）---
    async def some_business_logic(self, user_id, model_id) -> str | None:
        model = await self.get(user_id, model_id)
        return str(model) if model else None
```

---

## 第五步：定义 Router (routers.py)

```python
from brtech_backend.core.routers import RouterMeta, Public, RouteKey

@Public(RouteKey.FIND_BATCH)   # 标记 find_batch 接口允许匿名访问
@RouterMeta(
    prefix="/your-prefix",
    tags=["你的标签"],
    module_name="你的模块名称",   # 需与 @ui_config 一致
)
class YourRouter(StringPKeyWithDictionaryRouter[
    YourModel, YourCrud, YourQuery, YourService
]):
    """
    路由层 — 自动注册全部 CRUD 接口
    如需自定义 API，重写 _register_routes
    """
    def _register_routes(self):
        super()._register_routes()

        @self.router.post("/customAction/{model_id}", ...)
        async def custom_action(
            model_id: str = Path(...),
            service: YourService = Depends(self._get_service),
            auth_context: AuthContext = Depends(self.user_dependency),
        ):
            result = await service.some_business_logic(
                auth_context.user_id, model_id)
            return RestResponse.success(data=result)
```

### 自动注册的 API

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/{prefix}/add` | 新增 |
| POST | `/{prefix}/delete` | 删除 |
| POST | `/{prefix}/update` | 修改 |
| POST | `/{prefix}/find/{id}` | 单条查询 |
| POST | `/{prefix}/find/batch` | 批量查询 |
| POST | `/{prefix}/query/page` | 分页查询 |
| POST | `/{prefix}/query/all` | 查询全部 |
| POST | `/{prefix}/excel/import` | Excel 导入 |
| POST | `/{prefix}/excel/export` | Excel 导出 |

---

## 第六步：注册到应用入口 (main.py)

```python
from app.config import your_app_settings
from app.routers import your_router_classes

# 1. 覆盖默认配置
install_all_settings(your_app_settings)

# 2. 创建 Application，在 prepare 中注册路由
class YourApplication(Application):
    def prepare(self):
        super().prepare()
        # ... 注册系统模块 ...
        self.router_classes.extend(your_router_classes)  # ← 注册业务路由

creator = YourApplication(app_settings)
app = creator.get_app()
```

---

## 启动运行

### 后端

```bash
pip install -r requirements.txt
python main.py
```

服务默认运行在 http://localhost:9876，API 文档在 `/{context_path}{api_prefix}/docs`。

### 前端

```bash
npm install
npm run dev
```

前端开发服务器默认运行在 http://localhost:5173，`vite.config.ts` 中配置了 `/sample` 路径的反代到后端。

---

## 前端集成

前端安装 `brtech-fusion` 插件后：

```typescript
// main.ts
app.use(BrtechFusion, {
  apiPrefix: import.meta.env.VITE_API_BASE_URL,
  routePrefix: '/admin',
  loginPath: '/admin/login',
  homePath: '/admin',
})
```

管理后台直接使用底座 `AdminLayout` 组件，所有 CRUD 界面由后端的 `@ui_config` / `FieldOption` 注解驱动，前端 **无需为每个模块编写表格和表单代码**。

调用后端 API 示例：

```typescript
import {request} from 'brtech-fusion'

const {data} = await request.post('/your-prefix/query/page', {
  page: 1, size: 20, /* 查询条件 */
})
```

---

## 翻车急救

| 现象 | 原因 | 解决 |
|------|------|------|
| 启动报 `table xxx already exists` | 模型变更后表已存在 | 删表重建，或加 `__table_args__ = {"extend_existing": True}` |
| 前端显示空白 | API 路径不对 | 检查 `.env` 的 `VITE_API_BASE_URL` 是否与服务端 `CONTEXT_PATH + API_PREFIX` 一致 |
| 下拉选字典没数据 | 字典类型未初始化 | 检查 `fixtures/01_dictionary.json` 是否包含对应类型 |
| 登录提示"用户不存在" | Fixtures 未注入 | 首次启动后检查数据库 `a4_user` 表是否有数据 |
| Permission denied | OSS 配置不对 | 检查 `OSS_ENDPOINT / ACCESS_KEY / SECRET_KEY` |