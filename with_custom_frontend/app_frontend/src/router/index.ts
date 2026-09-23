// src/router/index.ts
/**
 * brtech 底座 - 前端路由配置示例
 *
 * 演示：
 *   - 基础路由设置（登录页、管理后台）
 *   - 使用 getUiBasePath() 获取 base path
 *   - 管理后台使用 brtech-fusion 的 AdminLayout
 */
import {createRouter, createWebHistory} from 'vue-router'
import {getUiBasePath} from 'brtech-fusion'

const router = createRouter({
  history: createWebHistory(getUiBasePath()),
  routes: [
    {
      path: '/',
      redirect: '/admin',
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue'),
      meta: {title: '用户登录'}
    },
    {
      // 管理后台 - 所有 /admin/* 路由由 brtech-fusion 的 AdminLayout 处理
      path: '/admin/:pathMatch(.*)*',
      name: 'Admin',
      component: () => import('@/views/admin/Index.vue'),
      meta: {title: '管理后台', requiresAuth: true}
    },
  ]
})

export default router
