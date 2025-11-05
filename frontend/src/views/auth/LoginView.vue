<!-- src/views/auth/LoginView.vue -->
<template>
  <v-container class="d-flex justify-center">
    <v-card class="pa-4" max-width="400">
      <v-card-title>Login</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleLogin">
          <v-text-field v-model="email" label="Email" required />
          <v-text-field v-model="password" type="password" label="Password" required />
          <v-btn type="submit" color="primary" :loading="auth.loading">Login</v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const auth = useAuthStore()
const email = ref('')
const password = ref('')

async function handleLogin() {
  await auth.login(email.value, password.value)
  if (auth.isAuthenticated) {
    router.push('/forms')
  }
}
</script>
