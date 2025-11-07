<template>
  <div class="form-list">
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-title class="d-flex align-center">
              <span>My Forms</span>
              <v-spacer />
              <v-btn 
                v-if="canCreateForm"
                color="primary" 
                prepend-icon="mdi-plus" 
                @click="createNewForm"
              >
                New Form
              </v-btn>
            </v-card-title>
            <v-card-text>
              <v-data-table
                :headers="headers"
                :items="forms"
                :loading="loading"
                @click:row="openForm"
              >
                <template #item.status="{ item }">
                  <v-chip :color="getStatusColor(item.status)">
                    {{ item.status }}
                  </v-chip>
                </template>

                <template #item.created_at="{ item }">
                  {{ formatDate(item.created_at) }}
                </template>

                <template #item.actions="{ item }">
                  <v-btn 
                    v-if="canEditForm"
                    icon="mdi-pencil" 
                    size="small" 
                    variant="text" 
                    @click.stop="editForm(item.id)" 
                  />
                  <v-btn 
                    icon="mdi-eye" 
                    size="small" 
                    variant="text" 
                    @click.stop="previewForm(item.id)" 
                  />
                  <v-btn 
                    v-if="canViewAnalytics"
                    icon="mdi-chart-bar" 
                    size="small" 
                    variant="text" 
                    @click.stop="viewAnalytics(item.id)" 
                  />
                  <v-btn 
                    v-if="canDuplicateForm"
                    icon="mdi-content-copy" 
                    size="small" 
                    variant="text" 
                    @click.stop="duplicateFormItem(item.id)" 
                  />
                  <v-btn 
                    v-if="canDeleteForm"
                    icon="mdi-delete" 
                    size="small" 
                    variant="text" 
                    color="error" 
                    @click.stop="deleteForm(item.id)" 
                  />
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useFormsStore } from '@/stores/forms'
import { usePermissions } from '@/composables/usePermissions'
import type { Form } from '@/types/formTypes'

// Router
const router = useRouter()

// Pinia store
const formsStore = useFormsStore()

// Permissions
const { 
  canCreateForm, 
  canEditForm, 
  canDeleteForm, 
  canViewAnalytics,
  canDuplicateForm 
} = usePermissions()

// Reactive headers
const headers = ref([
  { title: 'Title', key: 'title' },
  { title: 'Status', key: 'status' },
  { title: 'Created', key: 'created_at' },
  { title: 'Actions', key: 'actions', sortable: false }
])

// Computed state from Pinia
const forms = computed(() => formsStore.forms)
const loading = computed(() => formsStore.loading)

// Lifecycle
onMounted(() => {
  formsStore.fetchForms()
})

// Methods
function createNewForm() {
  router.push('/forms/new')
}

function openForm(event: Event, { item }: { item: Form }) {
  router.push(`/forms/${item.id}`)
}

function editForm(id: string) {
  router.push(`/forms/${id}/edit`)
}

function previewForm(id: string) {
  router.push(`/forms/${id}/preview`)
}

function viewAnalytics(id: string) {
  router.push(`/forms/${id}/analytics`)
}

async function duplicateFormItem(id: string) {
  try {
    await formsStore.duplicateForm(id)
    formsStore.showSnackbar({ message: 'Form duplicated successfully', color: 'success' })
    formsStore.fetchForms()
  } catch (error) {
    formsStore.showSnackbar({ message: 'Error duplicating form', color: 'error' })
  }
}

function deleteForm(id: string) {
  console.log('Delete form:', id)
}

function getStatusColor(status: string) {
  const colorMap: Record<string, string> = {
    draft: 'grey',
    published: 'green',
    archived: 'orange'
  }
  return colorMap[status] || 'grey'
}

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString()
}
</script>

<style scoped>
.form-list {
  padding: 16px;
}
</style>
