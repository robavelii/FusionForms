<template>
  <v-container fluid class="form-submissions">
    <!-- Toolbar -->
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-text>
            <div class="d-flex align-center gap-2">
              <v-text-field
                v-model="search"
                prepend-inner-icon="mdi-magnify"
                label="Search submissions"
                variant="outlined"
                density="compact"
                hide-details
                clearable
                style="max-width: 400px"
              />

              <v-select
                v-model="statusFilter"
                :items="['all', 'pending', 'reviewed', 'archived']"
                label="Status"
                variant="outlined"
                density="compact"
                hide-details
                style="max-width: 150px"
              />

              <v-menu>
                <template #activator="{ props }">
                  <v-btn
                    v-bind="props"
                    prepend-icon="mdi-calendar"
                    variant="outlined"
                  >
                    Date Range
                  </v-btn>
                </template>
                <v-card>
                  <v-card-text>
                    <v-text-field
                      v-model="dateRange.start"
                      label="Start Date"
                      type="date"
                      variant="outlined"
                      density="compact"
                      class="mb-2"
                    />
                    <v-text-field
                      v-model="dateRange.end"
                      label="End Date"
                      type="date"
                      variant="outlined"
                      density="compact"
                    />
                  </v-card-text>
                </v-card>
              </v-menu>

              <v-spacer />

              <v-btn
                v-if="canExportData"
                prepend-icon="mdi-download"
                variant="outlined"
                @click="exportSubmissions"
              >
                Export
              </v-btn>

              <v-btn
                prepend-icon="mdi-refresh"
                variant="text"
                @click="fetchSubmissions"
              >
                Refresh
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Data Table -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-data-table
            :headers="headers"
            :items="submissions"
            :loading="loading"
            :search="search"
            :items-per-page="itemsPerPage"
            :items-per-page-options="[10, 25, 50, 100]"
            @update:items-per-page="itemsPerPage = $event"
          >
            <template #item.id="{ item }">
              <v-chip size="small">
                #{{ item.id }}
              </v-chip>
            </template>

            <template #item.status="{ item }">
              <v-chip
                :color="getStatusColor(item.status)"
                size="small"
              >
                {{ item.status }}
              </v-chip>
            </template>

            <template #item.created_at="{ item }">
              {{ formatDate(item.created_at) }}
            </template>

            <template #item.data="{ item }">
              <v-btn
                size="small"
                variant="text"
                @click="viewSubmission(item)"
              >
                View Details
              </v-btn>
            </template>

            <template #item.actions="{ item }">
              <v-menu>
                <template #activator="{ props }">
                  <v-btn
                    icon="mdi-dots-vertical"
                    size="small"
                    variant="text"
                    v-bind="props"
                  />
                </template>
                <v-list>
                  <v-list-item @click="viewSubmission(item)">
                    <template #prepend>
                      <v-icon>mdi-eye</v-icon>
                    </template>
                    <v-list-item-title>View</v-list-item-title>
                  </v-list-item>
                  <v-list-item 
                    v-if="canEditSubmissions"
                    @click="editSubmission(item)"
                  >
                    <template #prepend>
                      <v-icon>mdi-pencil</v-icon>
                    </template>
                    <v-list-item-title>Edit</v-list-item-title>
                  </v-list-item>
                  <v-list-item 
                    v-if="canEditSubmissions"
                    @click="markAsReviewed(item)"
                  >
                    <template #prepend>
                      <v-icon>mdi-check</v-icon>
                    </template>
                    <v-list-item-title>Mark as Reviewed</v-list-item-title>
                  </v-list-item>
                  <v-divider v-if="canDeleteSubmissions" />
                  <v-list-item 
                    v-if="canDeleteSubmissions"
                    @click="deleteSubmission(item)" 
                    class="text-error"
                  >
                    <template #prepend>
                      <v-icon color="error">mdi-delete</v-icon>
                    </template>
                    <v-list-item-title>Delete</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>
            </template>

            <template #bottom>
              <div class="text-center pa-4">
                <v-pagination
                  v-model="page"
                  :length="pageCount"
                  @update:model-value="fetchSubmissions"
                />
              </div>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <!-- Submission Detail Dialog -->
    <v-dialog v-model="showDetailDialog" max-width="800" scrollable>
      <v-card v-if="selectedSubmission">
        <v-card-title class="d-flex align-center">
          <span>Submission #{{ selectedSubmission.id }}</span>
          <v-spacer />
          <v-btn
            icon="mdi-close"
            variant="text"
            @click="showDetailDialog = false"
          />
        </v-card-title>
        <v-divider />
        <v-card-text class="pa-6">
          <div class="mb-4">
            <v-chip :color="getStatusColor(selectedSubmission.status)" class="mr-2">
              {{ selectedSubmission.status }}
            </v-chip>
            <span class="text-caption text-medium-emphasis">
              Submitted {{ formatDate(selectedSubmission.created_at) }}
            </span>
          </div>

          <v-divider class="my-4" />

          <div v-for="(value, key) in selectedSubmission.data" :key="key" class="mb-4">
            <p class="text-subtitle-2 font-weight-bold mb-1">{{ formatFieldName(key) }}</p>
            <p class="text-body-1">{{ formatFieldValue(value) }}</p>
          </div>

          <v-divider class="my-4" />

          <div class="d-flex flex-column gap-2">
            <div>
              <span class="text-caption text-medium-emphasis">IP Address:</span>
              <span class="ml-2">{{ selectedSubmission.ip_address || 'N/A' }}</span>
            </div>
            <div>
              <span class="text-caption text-medium-emphasis">User Agent:</span>
              <span class="ml-2">{{ selectedSubmission.user_agent || 'N/A' }}</span>
            </div>
          </div>
        </v-card-text>
        <v-divider />
        <v-card-actions>
          <v-btn
            v-if="canEditSubmissions"
            color="primary"
            variant="outlined"
            @click="editSubmission(selectedSubmission)"
          >
            Edit
          </v-btn>
          <v-btn
            v-if="canEditSubmissions"
            color="success"
            variant="outlined"
            @click="markAsReviewed(selectedSubmission)"
          >
            Mark as Reviewed
          </v-btn>
          <v-spacer />
          <v-btn
            v-if="canDeleteSubmissions"
            color="error"
            variant="outlined"
            @click="deleteSubmission(selectedSubmission)"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Edit Submission Dialog -->
    <v-dialog v-model="showEditDialog" max-width="800" scrollable>
      <v-card v-if="editingSubmission">
        <v-card-title>Edit Submission #{{ editingSubmission.id }}</v-card-title>
        <v-divider />
        <v-card-text class="pa-6">
          <v-form ref="editForm">
            <div v-for="(value, key) in editingSubmission.data" :key="key" class="mb-4">
              <v-text-field
                v-model="editingSubmission.data[key]"
                :label="formatFieldName(key)"
                variant="outlined"
              />
            </div>
          </v-form>
        </v-card-text>
        <v-divider />
        <v-card-actions>
          <v-spacer />
          <v-btn @click="showEditDialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="saveSubmission">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useSnackbarStore } from '@/stores/snackbar'
import { useSubmissionsStore } from '@/stores/submission'
import { usePermissions } from '@/composables/usePermissions'
import apiClient from '@/services/api'

const props = defineProps<{
  formId: number | string
}>()

const snackbarStore = useSnackbarStore()
const submissionsStore = useSubmissionsStore()
const { canEditSubmissions, canDeleteSubmissions, canExportData } = usePermissions()

const loading = ref(false)
const search = ref('')
const statusFilter = ref('all')
const page = ref(1)
const itemsPerPage = ref(25)
const submissions = ref<any[]>([])
const selectedSubmission = ref<any>(null)
const editingSubmission = ref<any>(null)
const showDetailDialog = ref(false)
const showEditDialog = ref(false)

const dateRange = reactive({
  start: '',
  end: ''
})

const headers = [
  { title: 'ID', key: 'id', sortable: true },
  { title: 'Status', key: 'status', sortable: true },
  { title: 'Submitted', key: 'created_at', sortable: true },
  { title: 'Data', key: 'data', sortable: false },
  { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
]

const pageCount = computed(() => Math.ceil(submissions.value.length / itemsPerPage.value))

onMounted(() => {
  fetchSubmissions()
})

async function fetchSubmissions() {
  loading.value = true
  try {
    const params: any = {
      form: props.formId,
      page: page.value,
      page_size: itemsPerPage.value
    }

    if (statusFilter.value !== 'all') {
      params.status = statusFilter.value
    }

    if (dateRange.start) params.start_date = dateRange.start
    if (dateRange.end) params.end_date = dateRange.end

    const response = await apiClient.get('/submissions/', { params })
    submissions.value = response.data.results || []
  } catch (error) {
    console.error('Error fetching submissions:', error)
    snackbarStore.error('Failed to load submissions')
  } finally {
    loading.value = false
  }
}

function getStatusColor(status: string) {
  const colorMap: Record<string, string> = {
    pending: 'warning',
    reviewed: 'success',
    archived: 'grey'
  }
  return colorMap[status] || 'grey'
}

function formatDate(dateString: string) {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleString()
}

function formatFieldName(key: string) {
  return key
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (char) => char.toUpperCase())
}

function formatFieldValue(value: any) {
  if (value === null || value === undefined) return 'N/A'
  if (typeof value === 'object') return JSON.stringify(value)
  return value
}

function viewSubmission(item: any) {
  selectedSubmission.value = item
  showDetailDialog.value = true
}

function editSubmission(item: any) {
  editingSubmission.value = JSON.parse(JSON.stringify(item))
  showEditDialog.value = true
}

async function saveSubmission() {
  try {
    await apiClient.patch(`/submissions/${editingSubmission.value.id}/`, {
      data: editingSubmission.value.data
    })
    snackbarStore.success('Submission updated successfully')
    showEditDialog.value = false
    fetchSubmissions()
  } catch (error) {
    snackbarStore.error('Failed to update submission')
  }
}

async function markAsReviewed(item: any) {
  try {
    await apiClient.patch(`/submissions/${item.id}/`, {
      status: 'reviewed'
    })
    snackbarStore.success('Marked as reviewed')
    fetchSubmissions()
    if (showDetailDialog.value) showDetailDialog.value = false
  } catch (error) {
    snackbarStore.error('Failed to update status')
  }
}

async function deleteSubmission(item: any) {
  if (!confirm('Are you sure you want to delete this submission?')) return

  try {
    await apiClient.delete(`/submissions/${item.id}/`)
    snackbarStore.success('Submission deleted')
    fetchSubmissions()
    if (showDetailDialog.value) showDetailDialog.value = false
  } catch (error) {
    snackbarStore.error('Failed to delete submission')
  }
}

async function exportSubmissions() {
  try {
    const params: any = {
      form: props.formId,
      format: 'csv'
    }

    if (statusFilter.value !== 'all') params.status = statusFilter.value
    if (dateRange.start) params.start_date = dateRange.start
    if (dateRange.end) params.end_date = dateRange.end

    const response = await apiClient.get('/submissions/export/', {
      params,
      responseType: 'blob'
    })

    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `form-${props.formId}-submissions.csv`)
    document.body.appendChild(link)
    link.click()
    link.remove()

    snackbarStore.success('Submissions exported successfully')
  } catch (error) {
    snackbarStore.error('Failed to export submissions')
  }
}
</script>

<style scoped>
.form-submissions {
  padding: 0;
}
</style>

