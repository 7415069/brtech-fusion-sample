# 定制前端样例

本样例由独立 Python 后端和 Vue 3 前端组成。前端安装 `brtech-fusion` 插件并嵌入 `AdminLayout`，保留模型注解驱动的通用 CRUD 能力，同时提供自己的应用入口、路由和页面扩展位置。

公共配置、后端开发教程、初始化和权限说明见 [仓库 README](../README.md)。只需通用管理界面时，可使用 [不定制前端样例](../without_custom_frontend/README.md)。

## 目录与技术栈

```text
with_custom_frontend/
├── app_backend/
│   ├── main.py                   # 后端入口
│   ├── app/                      # 模型、CRUD、查询、服务、路由、配置
│   ├── fixtures/                 # 初始化数据与模板
│   ├── static/                   # npm run build 的输出目录
│   ├── .env
│   └── requirements.in / requirements.txt
└── app_frontend/
    ├── src/main.ts                # 安装 Pinia、Router、BrtechFusion
    ├── src/router/index.ts        # /console 路由及 All 兜底路由
    ├── src/views/console/Index.vue # 嵌入 AdminLayout
    ├── src/views/Login.vue        # 备用登录页面示例，当前未在路由中注册
    ├── src/stores/user.ts         # 用户状态示例
    ├── src/api/sample/index.ts    # 手写 API 封装示例
    ├── public/static/             # 图标、Logo、二维码资源
    ├── .env.development
    ├── .env.production
    ├── package.json
    └── vite.config.ts
```

后端要求 Python `>=3.11`。前端使用 Vue 3、TypeScript、Vue Router、Pinia、Element Plus、Vite 7；Node.js 要求为 `^20.19.0 || >=22.12.0`，与 `package.json` 一致。

## 依赖准备

后端 `requirements.in`、`requirements.txt` 引用本地 `brtech_fusion-2.0.0-py3-none-any.whl`；前端 `package.json` 引用本地 `brtech-fusion-2.0.0.tgz`。换机器需修改这些引用及相关锁文件，不能直接沿用开发者的绝对路径。

例如在前端目录执行以下命令，可设置实际 tgz 来源：

```bash
npm install /实际路径/brtech-fusion-2.0.0.tgz
```

后端 wheel 路径调整与 uv 依赖清单生成方式见仓库 README。前后端底座包应使用匹配版本。

## 方式一：构建前端，由后端统一提供服务

这种方式使用后端注入的运行时配置，适合确认完整集成效果和部署。

从仓库根目录执行，先构建前端：

```bash
cd with_custom_frontend/app_frontend
npm install
npm run build
```

构建会先执行 `vue-tsc -b` 类型检查，再由 Vite 打包，输出到 `../app_backend/static/`。然后启动后端：

```bash
cd ../app_backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdir -p var
python main.py
```

当前后端 `.env` 的端口为 `7654`，上下文与 UI 挂载路径均为根路径：

| 入口 | 当前地址 |
| --- | --- |
| 应用 | <http://127.0.0.1:7654/> |
| 登录 | <http://127.0.0.1:7654/console/login> |
| API 文档 | <http://127.0.0.1:7654/docs> |
| API 基址 | `http://127.0.0.1:7654/api/v1` |

初始账号 `root`、`admin` 的密码见 `app_backend/fixtures/02_A4User.json`。已初始化数据库中的信息优先于文件中初始值。

`vite.config.ts` 设置了 `emptyOutDir: true`，每次构建会清空后端 `static/` 再写入产物。要保留的前端静态文件应放到 `app_frontend/public/`；数据库、上传文件等持久数据不要存放在该输出目录。

如果未构建，后端可能回退到内置前端，因此“页面可以打开”并不能证明加载的是定制版本。应确认 `app_backend/static/index.html` 存在。

## 方式二：Vite 开发服务器联调

当前前端配置是：

```text
开发端口：5173
VITE_API_BASE_URL=/sample/api/v1
代理：/sample → http://127.0.0.1:9876
```

这些值对应后端 Python 默认配置，而后端当前 `.env` 使用端口 `7654` 和根路径。开始联调前必须选择一组一致的配置。

### 方案 A：保留现有 Vite 配置

在已安装依赖的 `app_backend` 目录，以进程环境变量覆盖 `.env`：

```bash
PORT=9876 CONTEXT_PATH=/sample UI_PATH=/frontend python main.py
```

另开终端，从 `app_frontend` 目录启动：

```bash
npm run dev
```

访问 <http://localhost:5173/console/login>。Vite 直接提供页面时，不会经过后端 HTML 配置注入；开发 API 使用 `.env.development` 的 `/sample/api/v1`，请求经 `/sample` 代理进入后端。

### 方案 B：保留当前后端 `.env`

将 `app_frontend/.env.development` 改为：

```dotenv
VITE_API_BASE_URL=/api/v1
```

将 `vite.config.ts` 中的代理调整为：

```typescript
proxy: {
  '/api': {
    target: 'http://127.0.0.1:7654',
    changeOrigin: true,
  },
},
```

分别执行后端 `python main.py` 与前端 `npm run dev`，访问同一个 Vite 登录地址。环境文件或 Vite 配置修改后需重启开发服务器。

两种方案二选一即可；不要同时保留不匹配的 API 基址和代理规则。Vite 端口如被占用，以终端打印的地址为准。

## 路由与插件配置

当前 `src/main.ts` 使用：

```typescript
app.use(BrtechFusion, {
  apiPrefix: import.meta.env.VITE_API_BASE_URL,
  routePrefix: '/console',
  loginPath: '/console/login',
  homePath: '/console',
})
```

`src/router/index.ts` 的主要配置为：

```typescript
const router = createRouter({
  history: createWebHistory(getUiBasePath()),
  routes: [
    { path: '/', redirect: '/console' },
    { path: '/login', redirect: '/console/login' },
    {
      path: '/console/:pathMatch(.*)*',
      name: 'All',
      component: () => import('@/views/console/Index.vue'),
      meta: { title: '管理控制台', requiresAuth: true },
    },
  ],
})
```

这段代码为关键配置摘录，导入语句见源文件。通用 CRUD 兜底路由名称保留为 `All`，它是当前 `AdminLayout` 的约定。不要仅为更换名称改为 `Admin` 或 `Console`，否则可能进入自定义子路由渲染分支，表现为菜单正常但内容空白。

`src/views/console/Index.vue` 仅嵌入 `<AdminLayout/>`。当前登录由底座处理，`src/views/Login.vue` 没有注册为当前登录路由。

### 三种路径不要混淆

| 路径 | 示例 | 作用 |
| --- | --- | --- |
| UI 部署基址 | `/sample/frontend` | `getUiBasePath()` 使用的浏览器路由 base |
| 前端页面路由 | `/console/business/sampleNormal` | 由路由前缀和菜单层级构成 |
| 后端 API | `/sample/api/v1/sampleNormal/query/page` | 由后端上下文、API 前缀与模块路由构成 |

后端托管构建产物时会注入 `window.__APP_CONFIG__`，API 基址优先使用后端运行时配置；不要只检查前端 `.env.production`。使用 Python 默认路径时，完整登录地址为 `http://127.0.0.1:9876/sample/frontend/console/login`。

## 自定义界面与 API

- 通用 CRUD：优先修改后端 `@ui_config` 和字段注解，不必创建每个模块的 Vue 页面。
- 品牌资源：修改 `public/static/`，然后重新构建。
- 独立页面：创建 Vue 组件并在 Vue Router 中显式注册。
- 管理布局中的自定义页面：按 `AdminLayout` 的子路由模式配置对应组件，同时保留通用 CRUD 兜底能力。

菜单中的 `component` 字符串不会自动导入仓库中的 Vue 文件。增加自定义页面需要同时考虑前端路由、菜单路径以及权限配置。

调用接口使用底座 `request`，它负责使用配置的 API 基址，例如：

```typescript
import { request } from 'brtech-fusion'

const response = await request.post('/sampleNormal/query/page', {
  page: 1,
  size: 20,
})
```

请求与响应字段以运行中的 OpenAPI 为准。传入模块相对路径即可，不要再次手动拼接 `/api/v1`。

现有 `src/api/sample/index.ts` 是手写封装参考，仍使用 `/normal`、`/recurse`，与后端 `/sampleNormal`、`/sampleRecurse` 不一致；使用前需对齐。后端 `models.py` 中自定义按钮也保留旧前缀。JSON 字段名应根据接口核对，尤其是树选择字段。文档更新未修改这些代码。

## 前端常用命令

在 `app_frontend` 执行：

| 命令 | 作用 |
| --- | --- |
| `npm install` | 安装依赖 |
| `npm run dev` | 启动 Vite 开发服务 |
| `npm run build` | 类型检查并构建到后端 static |
| `npm run preview` | 本地预览构建产物；不等同于后端托管和配置注入 |
| `npm run lint` | ESLint 检查并自动修复，会修改文件 |
| `npm run format` | 格式化 src，会修改文件 |

## 发布和排错

先构建前端，再发布 `app_backend` 的代码、完整 `static/`、fixtures、依赖及目标环境配置。正式访问由后端或正确配置的反向代理提供，不能把 `npm run dev` 当作发布步骤。

| 现象 | 优先检查 |
| --- | --- |
| npm 找不到 brtech-fusion | tgz 地址与 package-lock 中的本地引用 |
| 开发服务器 API 连接失败 | 是否把后端 7654 与 Vite 9876 配置混用 |
| 登录后内容为空 | `All` 路由名称、模块接口响应和浏览器控制台 |
| 修改 Vue 后后端页面没变 | 是否重新构建到正在运行的后端 static，必要时重启并刷新缓存 |
| 定制页面路径 404 | 是否显式注册 Vue 路由，代理是否支持 SPA 页面回退 |
| 构建后静态文件消失 | `emptyOutDir` 会清空输出目录，应把源资源放 public |

后端配置、权限、数据初始化、数据库迁移和 PEX 打包的限制见 [仓库 README](../README.md)。
