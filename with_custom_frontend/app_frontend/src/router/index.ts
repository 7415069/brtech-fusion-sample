// src/router/index.ts
/**
 * brtech 底座 - 前端路由配置示例
 *
 * 演示：
 *   - 基础路由设置（登录页、管理后台）
 *   - 使用 getUiBasePath() 获取 base path
 *   - 管理后台使用 brtech-fusion 的 AdminLayout
 */
import { createRouter, createWebHistory } from 'vue-router'
import { getUiBasePath } from 'brtech-fusion'

const router = createRouter({
  history: createWebHistory(getUiBasePath()),
  routes: [
    {
      path: '/',
      redirect: '/console',
    },
    {
      path: '/login',
      redirect: '/console/login',
    },
    {
      path: '/console/:pathMatch(.*)*',
      name: 'All',
      component: () => import('@/views/console/Index.vue'),
      meta: { title: '管理控制台', requiresAuth: true },
    },
  ],
})

export default router
