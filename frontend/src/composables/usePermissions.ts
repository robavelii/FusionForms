import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

/**
 * Role-Based Access Control (RBAC) Composable
 * 
 * Provides permission checks based on user roles:
 * - admin: Full access to everything
 * - designer: Can create/edit forms, view analytics
 * - analyst: Can view analytics and submissions
 * - viewer: Read-only access to forms and analytics
 */

export type UserRole = 'super_admin' | 'admin' | 'designer' | 'analyst' | 'viewer'

interface PermissionConfig {
  canCreateForm: UserRole[]
  canEditForm: UserRole[]
  canDeleteForm: UserRole[]
  canViewAnalytics: UserRole[]
  canViewSubmissions: UserRole[]
  canEditSubmissions: UserRole[]
  canDeleteSubmissions: UserRole[]
  canManageUsers: UserRole[]
  canManageWebhooks: UserRole[]
  canExportData: UserRole[]
  canPublishForm: UserRole[]
  canDuplicateForm: UserRole[]
}

// Permission configuration based on backend permissions
const PERMISSIONS: PermissionConfig = {
  // Form creation: admin and designer only
  canCreateForm: ['super_admin', 'admin', 'designer'],
  
  // Form editing: admin and designer only
  canEditForm: ['super_admin', 'admin', 'designer'],
  
  // Form deletion: admin and designer only
  canDeleteForm: ['super_admin', 'admin', 'designer'],
  
  // Analytics: all authenticated users can view (but only their own forms, or all for admins)
  canViewAnalytics: ['super_admin', 'admin', 'designer', 'analyst', 'viewer'],
  
  // Submissions: all authenticated users can view (but only their own forms, or all for admins)
  canViewSubmissions: ['super_admin', 'admin', 'designer', 'analyst', 'viewer'],
  
  // Submission editing: admin and designer only
  canEditSubmissions: ['super_admin', 'admin', 'designer'],
  
  // Submission deletion: admin and designer only
  canDeleteSubmissions: ['super_admin', 'admin', 'designer'],
  
  // User management: admin only
  canManageUsers: ['super_admin', 'admin'],
  
  // Webhook management: admin and designer only
  canManageWebhooks: ['super_admin', 'admin', 'designer'],
  
  // Data export: admin, designer, and analyst
  canExportData: ['super_admin', 'admin', 'designer', 'analyst'],
  
  // Form publishing: admin and designer only
  canPublishForm: ['super_admin', 'admin', 'designer'],
  
  // Form duplication: admin and designer only
  canDuplicateForm: ['super_admin', 'admin', 'designer']
}

export function usePermissions() {
  const authStore = useAuthStore()
  
  const currentRole = computed<UserRole | null>(() => {
    return (authStore.currentUser?.role as UserRole) || null
  })
  
  const isSuperAdmin = computed(() => currentRole.value === 'super_admin')
  const isAdmin = computed(() => currentRole.value === 'admin')
  const isDesigner = computed(() => currentRole.value === 'designer')
  const isAnalyst = computed(() => currentRole.value === 'analyst')
  const isViewer = computed(() => currentRole.value === 'viewer')
  
  // Check if user has a specific permission
  function hasPermission(permission: keyof PermissionConfig): boolean {
    if (!currentRole.value) return false
    return PERMISSIONS[permission].includes(currentRole.value)
  }
  
  // Check if user has any of the specified roles
  function hasAnyRole(...roles: UserRole[]): boolean {
    if (!currentRole.value) return false
    return roles.includes(currentRole.value)
  }
  
  // Check if user has all of the specified roles (useful for admin checks)
  function hasAllRoles(...roles: UserRole[]): boolean {
    if (!currentRole.value) return false
    return roles.every(role => role === currentRole.value)
  }
  
  // Permission checks
  const canCreateForm = computed(() => hasPermission('canCreateForm'))
  const canEditForm = computed(() => hasPermission('canEditForm'))
  const canDeleteForm = computed(() => hasPermission('canDeleteForm'))
  const canViewAnalytics = computed(() => hasPermission('canViewAnalytics'))
  const canViewSubmissions = computed(() => hasPermission('canViewSubmissions'))
  const canEditSubmissions = computed(() => hasPermission('canEditSubmissions'))
  const canDeleteSubmissions = computed(() => hasPermission('canDeleteSubmissions'))
  const canManageUsers = computed(() => hasPermission('canManageUsers'))
  const canManageWebhooks = computed(() => hasPermission('canManageWebhooks'))
  const canExportData = computed(() => hasPermission('canExportData'))
  const canPublishForm = computed(() => hasPermission('canPublishForm'))
  const canDuplicateForm = computed(() => hasPermission('canDuplicateForm'))
  
  return {
    // Current role info
    currentRole,
    isSuperAdmin,
    isAdmin,
    isDesigner,
    isAnalyst,
    isViewer,
    
    // Permission checks
    hasPermission,
    hasAnyRole,
    hasAllRoles,
    
    // Specific permissions
    canCreateForm,
    canEditForm,
    canDeleteForm,
    canViewAnalytics,
    canViewSubmissions,
    canEditSubmissions,
    canDeleteSubmissions,
    canManageUsers,
    canManageWebhooks,
    canExportData,
    canPublishForm,
    canDuplicateForm
  }
}

