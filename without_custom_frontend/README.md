# 不定制前端样例

本样例直接使用 brtech-fusion Python 包内置的管理前端。新增业务模块时主要编写 Python 模型、查询、服务与路由，通过注解生成通用表格和表单，通过 fixtures 配置菜单及权限，无需安装 Node.js。

完整的公共配置、后端分层开发教程、初始化说明和排错表见 [仓库 README](../README.md)。需要自行编写 Vue 页面时，参考 [定制前端样例](../with_custom_frontend/README.md)。

## 目录

```text
without_custom_frontend/
├── main.py              # Application、存储、模块注册、权限同步
├── app/
│   ├── config.py        # 默认配置
│   ├── models.py        # 普通模型、递归模型及 UI 注解
│   ├── crud.py          # 数据访问
│   ├── schemas.py       # 查询与排序
│   ├── services.py      # 默认值、唯一性检查、自定义业务
│   └── routers.py       # /sampleNormal、/sampleRecurse
├── fixtures/            # 初始化数据、字典 Excel 模板
├── static/              # favicon.svg、logo.svg
├── .env                 # 本地配置覆盖
├── requirements.in      # 底座 wheel 来源
├── requirements.txt     # 后端依赖清单
└── build_pex.sh          # 打包参考脚本
```

## 安装和启动

要求 Python 3.11 或更高版本，并准备当前样例使用的 `brtech_fusion-2.0.0-py3-none-any.whl`。先将 `requirements.in`、`requirements.txt` 中的本地 wheel 地址改为实际地址；详细方式见仓库 README。

从仓库根目录执行：

```bash
cd without_custom_frontend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdir -p var
python main.py
```

务必从本目录启动，使 `.env`、`fixtures/`、`static/` 和 `var/sample.db` 被正确定位。

当前 `.env` 配置了 `PORT=7654`、`CONTEXT_PATH=/`、`UI_PATH=/`：

- 界面：<http://127.0.0.1:7654/>
- API 文档：<http://127.0.0.1:7654/docs>
- API 基址：`http://127.0.0.1:7654/api/v1`

登录路由由底座内置前端管理，从界面根地址进入即可。初始账号为 `root`、`admin`，密码在 `fixtures/02_A4User.json`；已初始化数据库中的密码可能已经被修改。

若没有 `.env` 和进程环境变量覆盖，Python 默认端口为 `9876`，界面地址为 `http://127.0.0.1:9876/sample/frontend/`，文档为 `http://127.0.0.1:9876/sample/docs`。

## 界面从哪里来

底座检查当前工作目录的 `static/index.html`：

- 不存在时，使用 Python 包内置的前端入口和 assets；品牌资源可优先使用本地覆盖文件。
- 存在时，使用本地完整前端产物。

本样例的 `static/` 仅提供 `favicon.svg`、`logo.svg` 等品牌覆盖资源，不需要放入 Vue 构建产物。修改品牌图标可替换相应文件；应用标题、登录文案、主题等通过 `app/config.py` 或 `.env` 中的相关配置调整。

如果包内也没有前端入口，应检查安装的 wheel 是否包含内置静态资源。

## 增加业务模块

1. 在 `app/models.py` 定义模型及 `@ui_config`、`FieldOption`、`EnableQuery` 等注解。
2. 在 `app/crud.py` 定义匹配模型类型的 CRUD 类。
3. 在 `app/schemas.py` 定义查询类，需要复杂搜索时扩展 `custom_spec`。
4. 在 `app/services.py` 实现业务校验或生命周期钩子。
5. 在 `app/routers.py` 定义 Router，并加入 `sample_router_classes`。
6. 配置菜单的 `api_prefix`、字典、角色权限及按钮关联。
7. 重启服务，检查初始化和权限同步日志，使用目标角色验证页面和接口。

当前普通模型路由为 `/sampleNormal`，递归模型为 `/sampleRecurse`。例如当前配置下，分页查询接口为 `POST /api/v1/sampleNormal/query/page`。

`models.py` 的自定义按钮目前仍引用旧前缀 `/normal/customAction/{modelId}`。使用该扩展示例时应与实际 `/sampleNormal` 路由对齐；本次仅更新文档，未修改业务代码。

## 功能验证

- 普通模型：新增、编辑、详情、删除、关键词搜索、字典显示。
- 递归模型：父子节点、排序、编码重复校验、树选择关联。
- 权限：角色对应的菜单、按钮、接口和数据访问范围。
- 图片：先配置可用的 MinIO，再测试上传和读取。
- 注册、找回密码、支付：按启用功能准备邮件或支付服务。

服务入口已注册字典、4A 权限、日志、支付、UI 和任务模块，但外部服务仍需独立配置。

## 发布

部署本目录的后端代码、依赖、目标环境 `.env`、`fixtures/` 和 `static/`，保留数据库数据目录，执行 `python main.py`。不需要构建前端。入口关闭了自动重载，Python 修改后需重启。

`build_pex.sh` 需要先调整固定临时路径和 PEX 参数续行；它会清理构建目录并复制 `.env`。打包限制及发布包启动目录要求见 [仓库发布说明](../README.md#发布与运行维护)。
