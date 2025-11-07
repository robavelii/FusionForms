<template>
  <v-container fluid class="auth-container">
    <v-row align="center" justify="center" style="min-height: 100vh;">
      <v-col cols="12" sm="10" md="8" lg="6">
        <v-card elevation="8" class="pa-4">
          <v-card-title class="text-center">
            <div class="d-flex flex-column align-center mb-4">
              <v-icon size="64" color="primary" class="mb-2">mdi-form-select</v-icon>
              <h1 class="text-h4 font-weight-bold">FusionForms</h1>
              <p class="text-subtitle-1 text-medium-emphasis mt-2">Create your account</p>
            </div>
          </v-card-title>
          
          <v-card-text>
            <v-form ref="registerForm" @submit.prevent="handleRegister">
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="formData.first_name"
                    label="First Name"
                    prepend-inner-icon="mdi-account"
                    :rules="[rules.required]"
                    variant="outlined"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="formData.last_name"
                    label="Last Name"
                    prepend-inner-icon="mdi-account"
                    :rules="[rules.required]"
                    variant="outlined"
                  />
                </v-col>
              </v-row>

              <v-text-field
                v-model="formData.username"
                label="Username"
                prepend-inner-icon="mdi-account-circle"
                :rules="[rules.required, rules.minLength]"
                variant="outlined"
                hint="At least 3 characters"
                persistent-hint
                class="mb-2"
              />
              
              <v-text-field
                v-model="formData.email"
                label="Email"
                prepend-inner-icon="mdi-email"
                :rules="[rules.required, rules.email]"
                variant="outlined"
                type="email"
                class="mb-2"
              />

              <v-text-field
                v-model="formData.organization"
                label="Organization"
                prepend-inner-icon="mdi-office-building"
                :rules="[rules.required]"
                variant="outlined"
                hint="Your company or organization name"
                persistent-hint
                class="mb-2"
              />

              <v-select
                v-model="formData.role"
                label="Role"
                prepend-inner-icon="mdi-account-badge"
                :items="availableRoles"
                :rules="[rules.required]"
                variant="outlined"
                hint="Select your role"
                persistent-hint
                class="mb-2"
              />
              
              <v-text-field
                v-model="formData.password"
                :type="showPassword ? 'text' : 'password'"
                label="Password"
                prepend-inner-icon="mdi-lock"
                :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :rules="[rules.required, rules.passwordLength]"
                variant="outlined"
                hint="At least 8 characters"
                persistent-hint
                @click:append-inner="showPassword = !showPassword"
                class="mb-2"
              />

              <v-text-field
                v-model="formData.password_confirm"
                :type="showConfirmPassword ? 'text' : 'password'"
                label="Confirm Password"
                prepend-inner-icon="mdi-lock-check"
                :append-inner-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :rules="[rules.required, rules.passwordMatch]"
                variant="outlined"
                @click:append-inner="showConfirmPassword = !showConfirmPassword"
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
                Sign Up
              </v-btn>

              <div class="text-center">
                <p class="text-body-2">
                  Already have an account?
                  <router-link to="/login" class="text-primary text-decoration-none font-weight-medium">
                    Sign in
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

const registerForm = ref()
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const loading = ref(false)
const errorMessage = ref('')

// Available roles (excluding admin - admins can only be created by other admins)
const availableRoles = [
  { title: 'Form Designer', value: 'designer' },
  { title: 'Data Analyst', value: 'analyst' },
  { title: 'Viewer', value: 'viewer' }
]

const formData = reactive({
  first_name: '',
  last_name: '',
  username: '',
  email: '',
  organization: '',
  role: 'viewer', // Default role
  password: '',
  password_confirm: ''
})

const rules = {
  required: (v: string) => !!v || 'This field is required',
  minLength: (v: string) => v.length >= 3 || 'Username must be at least 3 characters',
  email: (v: string) => /.+@.+\..+/.test(v) || 'Email must be valid',
  passwordLength: (v: string) => v.length >= 8 || 'Password must be at least 8 characters',
  passwordMatch: (v: string) => v === formData.password || 'Passwords do not match'
}

async function handleRegister() {
  const { valid } = await registerForm.value.validate()
  
  if (!valid) return

  loading.value = true
  errorMessage.value = ''

  try {
    await authStore.register({
      first_name: formData.first_name,
      last_name: formData.last_name,
      username: formData.username,
      email: formData.email,
      organization: formData.organization,
      role: formData.role,
      password: formData.password,
      password_confirm: formData.password_confirm
    })
    snackbarStore.success('Registration successful! Welcome to FusionForms!')
    router.push('/dashboard')
  } catch (error: any) {
    // Handle various error formats from the backend
    if (error.response?.data) {
      const errorData = error.response.data
      if (typeof errorData === 'string') {
        errorMessage.value = errorData
      } else if (errorData.message) {
        errorMessage.value = errorData.message
      } else if (errorData.error) {
        errorMessage.value = errorData.error
      } else if (errorData.detail) {
        errorMessage.value = errorData.detail
      } else {
        // Handle field-specific errors
        const fieldErrors = []
        for (const [field, errors] of Object.entries(errorData)) {
          if (Array.isArray(errors)) {
            fieldErrors.push(`${field}: ${errors.join(', ')}`)
          } else {
            fieldErrors.push(`${field}: ${errors}`)
          }
        }
        errorMessage.value = fieldErrors.join('\n') || 'Registration failed. Please try again.'
      }
    } else {
      errorMessage.value = error.message || 'Registration failed. Please try again.'
    }
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

:deep(.v-field__input) {
  padding-top: 8px;
  padding-bottom: 8px;
}
</style>
