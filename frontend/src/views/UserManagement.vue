<template>
  <v-container fluid class="pa-6">
    <v-row>
      <v-col cols="12">
        <div class="d-flex justify-space-between align-center mb-6">
          <div>
            <h1 class="text-h4 font-weight-bold mb-2">User Management</h1>
            <p class="text-subtitle-1 text-medium-emphasis">Manage users and their roles</p>
          </div>
          <v-btn
            color="primary"
            prepend-icon="mdi-account-plus"
            @click="openCreateDialog"
          >
            Create User
          </v-btn>
        </div>

        <!-- Users Table -->
        <v-card>
          <v-card-title>
            <v-text-field
              v-model="search"
              prepend-inner-icon="mdi-magnify"
              label="Search users"
              variant="outlined"
              density="compact"
              hide-details
              clearable
            />
          </v-card-title>

          <v-data-table
            :headers="headers"
            :items="users"
            :search="search"
            :loading="loading"
            class="elevation-1"
          >
            <template #item.role="{ item }">
              <v-chip
                :color="getRoleColor(item.role)"
                size="small"
                label
              >
                {{ getRoleLabel(item.role) }}
              </v-chip>
            </template>

            <template #item.is_active="{ item }">
              <v-icon
                :color="item.is_active ? 'success' : 'error'"
                size="small"
              >
                {{ item.is_active ? 'mdi-check-circle' : 'mdi-close-circle' }}
              </v-icon>
            </template>

            <template #item.actions="{ item }">
              <v-btn
                icon="mdi-pencil"
                size="small"
                variant="text"
                @click="openEditDialog(item)"
              />
              <v-btn
                icon="mdi-delete"
                size="small"
                variant="text"
                color="error"
                @click="confirmDelete(item)"
              />
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <!-- Create/Edit User Dialog -->
    <v-dialog v-model="dialog" max-width="600px" persistent>
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ dialogTitle }}</span>
        </v-card-title>

        <v-card-text>
          <v-form ref="userForm">
            <v-row>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="editedUser.first_name"
                  label="First Name"
                  :rules="[rules.required]"
                  variant="outlined"
                />
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="editedUser.last_name"
                  label="Last Name"
                  :rules="[rules.required]"
                  variant="outlined"
                />
              </v-col>
            </v-row>

            <v-text-field
              v-model="editedUser.username"
              label="Username"
              :rules="[rules.required]"
              variant="outlined"
              class="mb-2"
            />

            <v-text-field
              v-model="editedUser.email"
              label="Email"
              :rules="[rules.required, rules.email]"
              type="email"
              variant="outlined"
              class="mb-2"
            />

            <v-text-field
              v-model="editedUser.organization"
              label="Organization"
              :rules="[rules.required]"
              variant="outlined"
              class="mb-2"
            />

            <v-select
              v-model="editedUser.role"
              label="Role"
              :items="allRoles"
              :rules="[rules.required]"
              variant="outlined"
              class="mb-2"
            />

            <v-text-field
              v-if="!editMode"
              v-model="editedUser.password"
              label="Password"
              :rules="[rules.required, rules.passwordLength]"
              type="password"
              variant="outlined"
              class="mb-2"
            />

            <v-text-field
              v-if="!editMode"
              v-model="editedUser.password_confirm"
              label="Confirm Password"
              :rules="[rules.required, rules.passwordMatch]"
              type="password"
              variant="outlined"
              class="mb-2"
            />

            <v-switch
              v-model="editedUser.is_active"
              label="Active"
              color="primary"
              hide-details
            />
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn
            variant="text"
            @click="closeDialog"
          >
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            variant="elevated"
            :loading="saving"
            @click="saveUser"
          >
            {{ editMode ? 'Update' : 'Create' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title class="text-h5">Confirm Delete</v-card-title>
        <v-card-text>
          Are you sure you want to delete user <strong>{{ userToDelete?.username }}</strong>?
          This action cannot be undone.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="deleteDialog = false">Cancel</v-btn>
          <v-btn
            color="error"
            variant="elevated"
            :loading="deleting"
            @click="deleteUser"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import apiClient from '@/services/api'
import { useSnackbarStore } from '@/stores/snackbar'

const snackbarStore = useSnackbarStore()

// State
const users = ref<any[]>([])
const search = ref('')
const loading = ref(false)
const dialog = ref(false)
const deleteDialog = ref(false)
const editMode = ref(false)
const saving = ref(false)
const deleting = ref(false)
const userForm = ref()
const userToDelete = ref<any>(null)

// All roles including admin (only visible to admins)
const allRoles = [
  { title: 'Admin', value: 'admin' },
  { title: 'Form Designer', value: 'designer' },
  { title: 'Data Analyst', value: 'analyst' },
  { title: 'User', value: 'user' }
]

const defaultUser = {
  first_name: '',
  last_name: '',
  username: '',
  email: '',
  organization: '',
  role: 'user',
  password: '',
  password_confirm: '',
  is_active: true
}

const editedUser = reactive({ ...defaultUser })

// Table headers
const headers = [
  { title: 'Username', key: 'username', sortable: true },
  { title: 'Name', key: 'full_name', sortable: true },
  { title: 'Email', key: 'email', sortable: true },
  { title: 'Organization', key: 'organization', sortable: true },
  { title: 'Role', key: 'role', sortable: true },
  { title: 'Active', key: 'is_active', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
]

// Computed
const dialogTitle = computed(() => {
  return editMode.value ? 'Edit User' : 'Create New User'
})

// Validation rules
const rules = {
  required: (v: string) => !!v || 'This field is required',
  email: (v: string) => /.+@.+\..+/.test(v) || 'Email must be valid',
  passwordLength: (v: string) => !v || v.length >= 8 || 'Password must be at least 8 characters',
  passwordMatch: (v: string) => v === editedUser.password || 'Passwords do not match'
}

// Methods
function getRoleColor(role: string) {
  const colors: Record<string, string> = {
    admin: 'error',
    designer: 'primary',
    analyst: 'success',
    user: 'secondary'
  }
  return colors[role] || 'secondary'
}

function getRoleLabel(role: string) {
  const labels: Record<string, string> = {
    admin: 'Admin',
    designer: 'Form Designer',
    analyst: 'Data Analyst',
    user: 'User'
  }
  return labels[role] || role
}

async function fetchUsers() {
  loading.value = true
  try {
    const response = await apiClient.get('/accounts/users/')
    users.value = response.data.map((user: any) => ({
      ...user,
      full_name: `${user.first_name || ''} ${user.last_name || ''}`.trim() || '-'
    }))
  } catch (error: any) {
    snackbarStore.error('Failed to load users')
    console.error('Error fetching users:', error)
  } finally {
    loading.value = false
  }
}

function openCreateDialog() {
  editMode.value = false
  Object.assign(editedUser, defaultUser)
  dialog.value = true
}

function openEditDialog(user: any) {
  editMode.value = true
  Object.assign(editedUser, {
    ...user,
    password: '',
    password_confirm: ''
  })
  dialog.value = true
}

function closeDialog() {
  dialog.value = false
  Object.assign(editedUser, defaultUser)
  userForm.value?.resetValidation()
}

async function saveUser() {
  const { valid } = await userForm.value.validate()
  if (!valid) return

  saving.value = true
  try {
    if (editMode.value) {
      // Update user
      const updateData = {
        first_name: editedUser.first_name,
        last_name: editedUser.last_name,
        username: editedUser.username,
        email: editedUser.email,
        organization: editedUser.organization,
        role: editedUser.role,
        is_active: editedUser.is_active
      }
      await apiClient.put(`/accounts/users/${editedUser.id}/`, updateData)
      snackbarStore.success('User updated successfully')
    } else {
      // Create user
      await apiClient.post('/accounts/users/', editedUser)
      snackbarStore.success('User created successfully')
    }
    closeDialog()
    fetchUsers()
  } catch (error: any) {
    const errorMsg = error.response?.data?.message || 
                     error.response?.data?.error || 
                     'Failed to save user'
    snackbarStore.error(errorMsg)
    console.error('Error saving user:', error)
  } finally {
    saving.value = false
  }
}

function confirmDelete(user: any) {
  userToDelete.value = user
  deleteDialog.value = true
}

async function deleteUser() {
  if (!userToDelete.value) return

  deleting.value = true
  try {
    await apiClient.delete(`/accounts/users/${userToDelete.value.id}/`)
    snackbarStore.success('User deleted successfully')
    deleteDialog.value = false
    userToDelete.value = null
    fetchUsers()
  } catch (error: any) {
    snackbarStore.error('Failed to delete user')
    console.error('Error deleting user:', error)
  } finally {
    deleting.value = false
  }
}

// Lifecycle
onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
:deep(.v-data-table) {
  border-radius: 8px;
}

:deep(.v-data-table-header) {
  background-color: rgba(var(--v-theme-surface-variant), 1);
}
</style>

