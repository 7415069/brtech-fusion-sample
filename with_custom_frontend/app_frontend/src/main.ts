import {createApp} from 'vue'
import {createPinia} from 'pinia'
import App from '@/App.vue'
import router from '@/router'

// 1. 引入底座插件 (包含 ElementPlus, AdminLayout, VersatileCrud 等)
import BrtechFusion from 'brtech-fusion'
// 2. 引入聚合样式
import 'brtech-fusion/style'

const app = createApp(App)

// 3. 状态管理
app.use(createPinia())

// 4. 路由
app.use(router)

// 5. 安装底座
app.use(BrtechFusion, {
  apiPrefix: import.meta.env.VITE_API_BASE_URL,
  routePrefix: '/admin',
  loginPath: '/admin/login',
  homePath: '/admin',
})

app.mount('#app')
