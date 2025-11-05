import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/Register.vue'),
    meta: { guest: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/forms',
    name: 'Forms',
    component: () => import('@/views/forms/FormList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/forms/new',
    name: 'NewForm',
    component: () => import('@/views/forms/FormBuilder.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/forms/:id',
    name: 'FormDetail',
    component: () => import('@/views/forms/FormDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/forms/:id/edit',
    name: 'EditForm',
    component: () => import('@/views/forms/FormBuilder.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/forms/:id/submissions',
    name: 'FormSubmissions',
    component: () => import('@/views/forms/FormSubmissions.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/forms/:id/analytics',
    name: 'FormAnalytics',
    component: () => import('@/views/forms/FormAnalytics.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/forms/:id/preview',
    name: 'FormPreview',
    component: () => import('@/views/forms/FormPreview.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = authStore.isAuthenticated

  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    next('/login')
  } else if (to.matched.some(record => record.meta.guest) && isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
