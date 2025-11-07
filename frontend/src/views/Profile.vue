<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 font-weight-bold mb-4">Profile</h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-text class="text-center">
            <v-avatar size="120" class="mb-4">
              <v-img
                :src="`https://ui-avatars.com/api/?name=${userData.username || 'User'}&background=3b82f6&color=fff&size=120`"
                :alt="userData.username"
              />
            </v-avatar>
            <h2 class="text-h5">{{ userData.username || 'User' }}</h2>
            <p class="text-subtitle-1 text-medium-emphasis">{{ userData.email }}</p>
            <v-chip :color="getRoleColor(userData.role)" class="mt-2">
              {{ userData.role || 'User' }}
            </v-chip>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>Profile Information</v-card-title>
          <v-card-text>
            <v-form>
              <v-text-field
                v-model="userData.username"
                label="Username"
                variant="outlined"
                density="comfortable"
                readonly
              />
              <v-text-field
                v-model="userData.email"
                label="Email"
                type="email"
                variant="outlined"
                density="comfortable"
                readonly
              />
              <v-text-field
                v-model="userData.first_name"
                label="First Name"
                variant="outlined"
                density="comfortable"
                readonly
              />
              <v-text-field
                v-model="userData.last_name"
                label="Last Name"
                variant="outlined"
                density="comfortable"
                readonly
              />
              <v-btn color="primary" @click="router.push('/settings')">
                Edit Profile
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const userData = ref({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  role: ''
})

onMounted(async () => {
  if (!authStore.currentUser) {
    await authStore.fetchProfile()
  }
  if (authStore.currentUser) {
    userData.value = {
      username: authStore.currentUser.username || '',
      email: authStore.currentUser.email || '',
      first_name: authStore.currentUser.first_name || '',
      last_name: authStore.currentUser.last_name || '',
      role: authStore.currentUser.role || ''
    }
  }
})

function getRoleColor(role: string) {
  const colors: Record<string, string> = {
    super_admin: 'error',
    admin: 'warning',
    designer: 'info',
    analyst: 'success',
    viewer: 'default'
  }
  return colors[role] || 'default'
}
</script>

<style scoped>
</style>

