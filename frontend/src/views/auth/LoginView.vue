<template>
  <v-container fluid class="auth-container">
    <v-row align="center" justify="center" style="min-height: 100vh;">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card elevation="8" class="pa-4">
          <v-card-title class="text-center">
            <div class="d-flex flex-column align-center mb-4">
              <v-icon size="64" color="primary" class="mb-2">mdi-form-select</v-icon>
              <h1 class="text-h4 font-weight-bold">FusionForms</h1>
              <p class="text-subtitle-1 text-medium-emphasis mt-2">Sign in to your account</p>
            </div>
          </v-card-title>
          
          <v-card-text>
            <v-form ref="loginForm" @submit.prevent="handleLogin">
              <v-text-field
                v-model="formData.email"
                label="Email"
                prepend-inner-icon="mdi-account"
                :rules="[rules.required]"
                variant="outlined"
                class="mb-2"
              />
              
              <v-text-field
                v-model="formData.password"
                :type="showPassword ? 'text' : 'password'"
                label="Password"
                prepend-inner-icon="mdi-lock"
                :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :rules="[rules.required]"
                variant="outlined"
                @click:append-inner="showPassword = !showPassword"
                class="mb-2"
              />

              <v-alert
                v-if="errorMessage"
                type="error"
                variant="tonal"
                class="mb-4"
                closable
                @click:close="errorMessage = ''"
              >
                {{ errorMessage }}
              </v-alert>

              <v-btn
                type="submit"
                color="primary"
                size="large"
                block
                :loading="loading"
                class="mb-4"
              >
                Sign In
              </v-btn>

              <div class="text-center">
                <p class="text-body-2">
                  Don't have an account?
                  <router-link to="/register" class="text-primary text-decoration-none">
                    Sign up
                  </router-link>
                </p>
              </div>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useSnackbarStore } from '@/stores/snackbar'

const router = useRouter()
const authStore = useAuthStore()
const snackbarStore = useSnackbarStore()

const loginForm = ref()
const showPassword = ref(false)
const loading = ref(false)
const errorMessage = ref('')

const formData = reactive({
  email: '',
  password: ''
})

const rules = {
  required: (v: string) => !!v || 'This field is required'
}

async function handleLogin() {
  const { valid } = await loginForm.value.validate()
  
  if (!valid) return

  loading.value = true
  errorMessage.value = ''

  try {
    await authStore.login(formData)
    snackbarStore.success('Login successful!')
    router.push('/dashboard')
  } catch (error: any) {
    errorMessage.value = error.response?.data?.message || 'Invalid email or password'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-container {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}
</style>
