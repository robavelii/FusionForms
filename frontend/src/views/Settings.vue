<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 font-weight-bold mb-4">Settings</h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>Account Settings</v-card-title>
          <v-card-text>
            <v-form>
              <v-text-field
                v-model="userData.username"
                label="Username"
                variant="outlined"
                density="comfortable"
              />
              <v-text-field
                v-model="userData.email"
                label="Email"
                type="email"
                variant="outlined"
                density="comfortable"
              />
              <v-text-field
                v-model="userData.first_name"
                label="First Name"
                variant="outlined"
                density="comfortable"
              />
              <v-text-field
                v-model="userData.last_name"
                label="Last Name"
                variant="outlined"
                density="comfortable"
              />
              <v-btn color="primary" @click="saveSettings" :loading="saving">
                Save Changes
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>

        <v-card class="mt-4">
          <v-card-title>Change Password</v-card-title>
          <v-card-text>
            <v-form>
              <v-text-field
                v-model="passwordData.currentPassword"
                label="Current Password"
                type="password"
                variant="outlined"
                density="comfortable"
              />
              <v-text-field
                v-model="passwordData.newPassword"
                label="New Password"
                type="password"
                variant="outlined"
                density="comfortable"
              />
              <v-text-field
                v-model="passwordData.confirmPassword"
                label="Confirm New Password"
                type="password"
                variant="outlined"
                density="comfortable"
              />
              <v-btn color="primary" @click="changePassword" :loading="changingPassword">
                Change Password
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>Preferences</v-card-title>
          <v-card-text>
            <v-switch
              v-model="preferences.emailNotifications"
              label="Email Notifications"
              color="primary"
            />
            <v-switch
              v-model="preferences.marketingEmails"
              label="Marketing Emails"
              color="primary"
            />
            <v-btn color="primary" @click="savePreferences" :loading="savingPreferences" class="mt-4">
              Save Preferences
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useSnackbarStore } from '@/stores/snackbar'
import apiClient from '@/services/api'

const authStore = useAuthStore()
const snackbarStore = useSnackbarStore()

const saving = ref(false)
const changingPassword = ref(false)
const savingPreferences = ref(false)

const userData = ref({
  username: '',
  email: '',
  first_name: '',
  last_name: ''
})

const passwordData = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const preferences = ref({
  emailNotifications: true,
  marketingEmails: false
})

onMounted(() => {
  if (authStore.currentUser) {
    userData.value = {
      username: authStore.currentUser.username || '',
      email: authStore.currentUser.email || '',
      first_name: authStore.currentUser.first_name || '',
      last_name: authStore.currentUser.last_name || ''
    }
  }
})

async function saveSettings() {
  saving.value = true
  try {
    await apiClient.put('/accounts/profile/', userData.value)
    await authStore.fetchProfile()
    snackbarStore.success('Settings saved successfully')
  } catch (error: any) {
    snackbarStore.error(error.response?.data?.detail || 'Failed to save settings')
  } finally {
    saving.value = false
  }
}

async function changePassword() {
  if (passwordData.value.newPassword !== passwordData.value.confirmPassword) {
    snackbarStore.error('New passwords do not match')
    return
  }

  changingPassword.value = true
  try {
    await apiClient.post('/accounts/change-password/', {
      old_password: passwordData.value.currentPassword,
      new_password: passwordData.value.newPassword
    })
    snackbarStore.success('Password changed successfully')
    passwordData.value = {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
  } catch (error: any) {
    snackbarStore.error(error.response?.data?.detail || 'Failed to change password')
  } finally {
    changingPassword.value = false
  }
}

async function savePreferences() {
  savingPreferences.value = true
  try {
    // Save preferences to backend
    await apiClient.put('/accounts/preferences/', preferences.value)
    snackbarStore.success('Preferences saved successfully')
  } catch (error: any) {
    snackbarStore.error(error.response?.data?.detail || 'Failed to save preferences')
  } finally {
    savingPreferences.value = false
  }
}
</script>

<style scoped>
</style>

