<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useTheme } from '@/composables/useTheme'
import Snackbar from '@/components/shared/Snackbar.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const { isDark, toggleTheme } = useTheme()

const drawer = ref(true)
const rail = ref(false)

const isAuthenticated = computed(() => authStore.isAuthenticated)
const currentUser = computed(() => authStore.currentUser)
const isSuperAdmin = computed(() => authStore.isSuperAdmin)
const isAdmin = computed(() => authStore.isAdmin)

// Navigation item type
interface NavigationItem {
  title: string
  icon: string
  to: string
  disabled?: boolean
}

// Navigation items (computed to show/hide based on role)
const navigationItems = computed((): NavigationItem[] => {
  const items: NavigationItem[] = [
    {
      title: 'Dashboard',
      icon: 'mdi-view-dashboard',
      to: '/dashboard'
    },
    {
      title: 'Forms',
      icon: 'mdi-file-document-multiple',
      to: '/forms'
    }
  ]
  
  // Add admin-only items
  if (isSuperAdmin.value || isAdmin.value) {
    items.push({
      title: 'Users',
      icon: 'mdi-account-multiple',
      to: '/users'
    })
  }
  
  // Analytics - show for all authenticated users (can be per-form or global)
  items.push({
    title: 'Analytics',
    icon: 'mdi-chart-line',
    to: '/analytics'
  })
  
  // Settings - show for all authenticated users
  items.push({
    title: 'Settings',
    icon: 'mdi-cog',
    to: '/settings'
  })
  
  return items
})

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

// Hide navigation on auth pages and public pages
const hideNavigation = computed(() => {
  return route.meta.guest || route.path.includes('/preview') || !isAuthenticated.value
})

onMounted(async () => {
  if (isAuthenticated.value && !currentUser.value) {
    try {
      await authStore.fetchProfile()
    } catch (error) {
      console.error('Failed to fetch user profile:', error)
    }
  }
})
</script>

<template>
  <v-app>
    <!-- Navigation Drawer -->
    <v-navigation-drawer
      v-if="!hideNavigation"
      v-model="drawer"
      :rail="rail"
      permanent
      elevation="1"
      @click="rail = false"
    >
      <!-- User Profile Section -->
      <v-list-item
        class="pa-3"
        :prepend-avatar="`https://ui-avatars.com/api/?name=${currentUser?.username || 'User'}&background=3b82f6&color=fff`"
        :title="currentUser?.username || 'User'"
        :subtitle="currentUser?.email || ''"
        nav
      >
        <template #append>
          <v-btn
            :icon="rail ? 'mdi-chevron-right' : 'mdi-chevron-left'"
            variant="text"
            size="small"
            @click.stop="rail = !rail"
          />
        </template>
      </v-list-item>

      <v-divider class="mb-2" />

      <!-- Navigation Items -->
      <v-list density="comfortable" nav class="px-2">
        <v-list-item
          v-for="item in navigationItems"
          :key="item.title"
          :prepend-icon="item.icon"
          :title="item.title"
          :to="item.to"
          :disabled="item.disabled"
          :value="item.title"
          rounded="lg"
          class="mb-1"
        />
      </v-list>

      <!-- Logout Button at Bottom -->
      <template #append>
        <div class="pa-3">
          <v-divider class="mb-3" />
          <v-btn
            block
            variant="tonal"
            color="error"
            prepend-icon="mdi-logout"
            @click="handleLogout"
          >
            <span v-if="!rail">Logout</span>
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>

    <!-- App Bar -->
    <v-app-bar
      v-if="!hideNavigation"
      elevation="0"
      color="surface"
      border="b"
    >
      <v-app-bar-nav-icon
        v-if="!drawer"
        @click="drawer = !drawer"
      />
      
      <v-toolbar-title class="d-flex align-center">
        <v-icon size="32" color="primary" class="mr-2">mdi-form-select</v-icon>
        <span class="text-h6 font-weight-bold">FusionForms</span>
      </v-toolbar-title>

      <v-spacer />

      <!-- Theme Toggle -->
      <v-tooltip location="bottom">
        <template #activator="{ props }">
          <v-btn
            v-bind="props"
            :icon="isDark ? 'mdi-weather-sunny' : 'mdi-weather-night'"
            variant="text"
            @click="toggleTheme"
          />
        </template>
        <span>{{ isDark ? 'Light Mode' : 'Dark Mode' }}</span>
      </v-tooltip>

      <!-- Notifications -->
      <v-tooltip location="bottom">
        <template #activator="{ props }">
          <v-btn
            v-bind="props"
            icon="mdi-bell-outline"
            variant="text"
          />
        </template>
        <span>Notifications</span>
      </v-tooltip>

      <!-- User Menu -->
      <v-menu>
        <template #activator="{ props }">
          <v-btn
            v-bind="props"
            icon="mdi-account-circle"
            variant="text"
          />
        </template>
        <v-list>
          <v-list-item prepend-icon="mdi-account" @click="router.push('/profile')">
            <v-list-item-title>Profile</v-list-item-title>
          </v-list-item>
          <v-list-item prepend-icon="mdi-cog" @click="router.push('/settings')">
            <v-list-item-title>Settings</v-list-item-title>
          </v-list-item>
          <v-divider />
          <v-list-item prepend-icon="mdi-logout" @click="handleLogout">
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <!-- Main Content -->
    <v-main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </v-main>

    <!-- Global Snackbar -->
    <Snackbar />
  </v-app>
</template>

<style scoped>
/* Page Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Main Content Styling */
.main-content {
  background-color: rgb(var(--v-theme-background));
  min-height: 100vh;
}

/* Navigation Drawer Custom Styling */
:deep(.v-navigation-drawer) {
  border-right: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}

/* Active Navigation Item */
:deep(.v-list-item--active) {
  background-color: rgba(var(--v-theme-primary), 0.12) !important;
  color: rgb(var(--v-theme-primary));
}

:deep(.v-list-item--active .v-icon) {
  color: rgb(var(--v-theme-primary));
}

/* Hover effect for navigation items */
:deep(.v-list-item:not(.v-list-item--disabled):hover) {
  background-color: rgba(var(--v-theme-primary), 0.08);
}

/* App Bar Styling */
:deep(.v-app-bar) {
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}
</style>
