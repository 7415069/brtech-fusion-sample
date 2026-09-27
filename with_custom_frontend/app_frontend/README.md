# 样例定制前端

Vue 3 + TypeScript + Vite 应用，通过 `brtech-fusion` 插件使用底座管理界面。

完整安装、联调、路由与发布说明见 [定制前端样例 README](../README.md)，公共后端说明见 [仓库 README](../../README.md)。

## 环境与安装

Node.js 要求：`^20.19.0 || >=22.12.0`。

`package.json` 当前引用开发机上的本地 `brtech-fusion-2.0.0.tgz`，换机器需先更新路径和锁文件：

```bash
npm install /实际路径/brtech-fusion-2.0.0.tgz
npm install
```

## 常用命令

```bash
npm run dev       # Vite 开发服务
npm run build     # 类型检查并构建到 ../app_backend/static
npm run preview   # 本地构建预览
npm run lint      # 自动修复，会修改文件
npm run format    # 格式化 src，会修改文件
```

构建会清空输出目录。静态源文件放在 `public/` 中，不要直接维护输出目录中的文件。

## 关键配置

- 开发入口通常为 `http://localhost:5173/console/login`。
- `src/main.ts` 的路由前缀、登录页、首页分别是 `/console`、`/console/login`、`/console`。
- `src/router/index.ts` 的通用管理兜底路由名称为 `All`。
- API 开发基址为 `/sample/api/v1`，Vite 代理 `/sample` 到 `http://127.0.0.1:9876`。
- 后端当前 `.env` 使用 `7654` 和根路径，必须按上级 README 中的联调方案对齐。
- 后端托管构建产物时，会注入运行时配置；当前后端登录地址为 `http://127.0.0.1:7654/console/login`。
- 手写 API 示例仍有 `/normal`、`/recurse` 旧前缀，使用前应对齐后端 `/sampleNormal`、`/sampleRecurse`。
