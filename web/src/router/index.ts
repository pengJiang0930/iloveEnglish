import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue')
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/Register.vue')
    },
    {
      path: '/',
      component: () => import('@/components/Layout/index.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'Home',
          component: () => import('@/views/Home.vue'),
          meta: { title: '首页' }
        },
        {
          path: 'word-book',
          name: 'WordBook',
          component: () => import('@/views/wordBook/index.vue'),
          meta: { title: '词书管理' }
        },
        {
          path: 'word',
          name: 'Word',
          component: () => import('@/views/word/index.vue'),
          meta: { title: '单词管理' }
        },
        {
          path: 'memory-tip',
          name: 'MemoryTip',
          component: () => import('@/views/memoryTip/index.vue'),
          meta: { title: 'AI速记管理' }
        },
        {
          path: 'user',
          name: 'User',
          component: () => import('@/views/user/index.vue'),
          meta: { title: '用户管理' }
        }
      ]
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const isAuthenticated = !!userStore.token

  if (to.meta.requiresAuth && !isAuthenticated) {
    // 需要认证但未登录，跳转到登录页
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if ((to.name === 'Login' || to.name === 'Register') && isAuthenticated) {
    // 已登录但访问登录/注册页，跳转到首页
    next({ name: 'Home' })
  } else {
    next()
  }
})

export default router
