import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/leads',
    name: 'Leads',
    component: () => import('@/views/LeadsView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/chats',
    name: 'Chats',
    component: () => import('@/views/ChatsView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/calendar',
    name: 'Calendar',
    component: () => import('@/views/CalendarView.vue'),
    meta: { requiresAuth: true }
  },
  // Fallback for login (placeholder)
  {
    path: '/login',
    name: 'Login',
    component: () => Promise.resolve({ template: '<div class="p-8 text-center"><h1>Login Page (Placeholder)</h1></div>' }),
    meta: { requiresAuth: false }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router