import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores'
import { usePermissions } from '@/composables/usePermissions'

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
    component: () => import('@/views/auth/LoginView.vue'),
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/RegisterView.vue'),
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
    meta: { 
      requiresAuth: true,
      requiresPermission: 'canCreateForm' // Only admin and designer
    }
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
    meta: { 
      requiresAuth: true,
      requiresPermission: 'canEditForm' // Only admin and designer
    }
  },
  {
    path: '/forms/:id/submissions',
    name: 'FormSubmissions',
    component: () => import('@/views/forms/FormSubmissions.vue'),
    meta: { 
      requiresAuth: true,
      requiresPermission: 'canViewSubmissions' // All authenticated users
    }
  },
  {
    path: '/forms/:id/analytics',
    name: 'FormAnalytics',
    component: () => import('@/views/forms/FormAnalytics.vue'),
    meta: { 
      requiresAuth: true,
      requiresPermission: 'canViewAnalytics' // All authenticated users
    }
  },
  {
    path: '/forms/:id/preview',
    name: 'FormPreview',
    component: () => import('@/views/forms/FormPreview.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/users',
    name: 'UserManagement',
    component: () => import('@/views/UserManagement.vue'),
    meta: { 
      requiresAuth: true,
      requiresPermission: 'canManageUsers' // Admin only
    }
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

// Navigation guard with role-based access control
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = authStore.isAuthenticated
  
  // Check if route requires authentication
  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    next('/login')
    return
  }
  
  // Check if route is for guests only (login/register)
  if (to.matched.some(record => record.meta.guest) && isAuthenticated) {
    next('/dashboard')
    return
  }
  
  // Check role-based permissions
  if (isAuthenticated && to.matched.some(record => record.meta.requiresPermission)) {
    const { hasPermission } = usePermissions()
    const requiredPermission = to.meta.requiresPermission as string
    
    if (!hasPermission(requiredPermission as any)) {
      // User doesn't have required permission, redirect to dashboard
      next('/dashboard')
      return
    }
  }
  
  // Legacy admin check (for backwards compatibility)
  if (to.matched.some(record => record.meta.requiresAdmin)) {
    const isSuperAdmin = authStore.isSuperAdmin
    const isAdmin = authStore.isAdmin
    if (!isSuperAdmin && !isAdmin) {
      next('/dashboard')
      return
    }
  }
  
  next()
})

export default router
