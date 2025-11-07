<template>
  <v-container fluid class="form-overview">
    <!-- Quick Stats -->
    <v-row>
      <v-col
        v-for="stat in quickStats"
        :key="stat.title"
        cols="12"
        sm="6"
        md="3"
      >
        <v-card>
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <p class="text-subtitle-2 text-medium-emphasis mb-1">
                  {{ stat.title }}
                </p>
                <h2 class="text-h5 font-weight-bold">
                  {{ stat.value }}
                </h2>
              </div>
              <v-avatar :color="stat.color" size="48">
                <v-icon color="white">{{ stat.icon }}</v-icon>
              </v-avatar>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Form Info & Actions -->
    <v-row class="mt-4">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>Form Information</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item>
                <template #prepend>
                  <v-icon>mdi-identifier</v-icon>
                </template>
                <v-list-item-title>Form ID</v-list-item-title>
                <v-list-item-subtitle>{{ form.id }}</v-list-item-subtitle>
              </v-list-item>
              
              <v-list-item>
                <template #prepend>
                  <v-icon>mdi-calendar-clock</v-icon>
                </template>
                <v-list-item-title>Created</v-list-item-title>
                <v-list-item-subtitle>{{ formatDate(form.created_at) }}</v-list-item-subtitle>
              </v-list-item>
              
              <v-list-item>
                <template #prepend>
                  <v-icon>mdi-update</v-icon>
                </template>
                <v-list-item-title>Last Modified</v-list-item-title>
                <v-list-item-subtitle>{{ formatDate(form.updated_at) }}</v-list-item-subtitle>
              </v-list-item>
              
              <v-list-item>
                <template #prepend>
                  <v-icon>mdi-format-list-numbered</v-icon>
                </template>
                <v-list-item-title>Total Fields</v-list-item-title>
                <v-list-item-subtitle>{{ form.schema?.fields?.length || 0 }}</v-list-item-subtitle>
              </v-list-item>
              
              <v-list-item>
                <template #prepend>
                  <v-icon>mdi-web</v-icon>
                </template>
                <v-list-item-title>Form URL</v-list-item-title>
                <v-list-item-subtitle class="d-flex align-center">
                  <a :href="formUrl" target="_blank" class="text-primary">
                    {{ formUrl }}
                  </a>
                  <v-btn
                    icon="mdi-content-copy"
                    size="x-small"
                    variant="text"
                    class="ml-2"
                    @click="copyUrl"
                  />
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>

        <!-- Recent Submissions -->
        <v-card class="mt-4">
          <v-card-title class="d-flex align-center">
            <span>Recent Submissions</span>
            <v-spacer />
            <v-btn
              variant="text"
              color="primary"
              @click="viewAllSubmissions"
            >
              View All
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-list v-if="recentSubmissions.length > 0">
              <v-list-item
                v-for="(submission, index) in recentSubmissions"
                :key="submission.id"
              >
                <template #prepend>
                  <v-avatar color="primary">
                    {{ index + 1 }}
                  </v-avatar>
                </template>
                <v-list-item-title>
                  Submission #{{ submission.id }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  {{ formatDate(submission.created_at) }}
                </v-list-item-subtitle>
                <template #append>
                  <v-btn
                    icon="mdi-eye"
                    size="small"
                    variant="text"
                    @click="viewSubmission(submission.id)"
                  />
                </template>
              </v-list-item>
            </v-list>
            <div v-else class="text-center py-8">
              <v-icon size="48" color="grey-lighten-1">mdi-inbox-outline</v-icon>
              <p class="text-subtitle-1 text-medium-emphasis mt-4">No submissions yet</p>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <!-- Quick Actions -->
        <v-card>
          <v-card-title>Quick Actions</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item
                prepend-icon="mdi-pencil"
                title="Edit Form"
                @click="editForm"
              />
              <v-divider />
              <v-list-item
                prepend-icon="mdi-eye"
                title="Preview Form"
                @click="previewForm"
              />
              <v-divider />
              <v-list-item
                prepend-icon="mdi-publish"
                :title="form.status === 'published' ? 'Unpublish' : 'Publish'"
                @click="togglePublish"
              />
              <v-divider />
              <v-list-item
                prepend-icon="mdi-content-copy"
                title="Duplicate Form"
                @click="duplicateForm"
              />
              <v-divider />
              <v-list-item
                prepend-icon="mdi-download"
                title="Export Data"
                @click="exportData"
              />
            </v-list>
          </v-card-text>
        </v-card>

        <!-- Form Stats -->
        <v-card class="mt-4">
          <v-card-title>Performance</v-card-title>
          <v-card-text>
            <div class="mb-4">
              <div class="d-flex justify-space-between mb-1">
                <span class="text-subtitle-2">Completion Rate</span>
                <span class="font-weight-bold">78%</span>
              </div>
              <v-progress-linear
                :model-value="78"
                color="success"
                height="8"
                rounded
              />
            </div>
            
            <div class="mb-4">
              <div class="d-flex justify-space-between mb-1">
                <span class="text-subtitle-2">Avg. Time to Complete</span>
                <span class="font-weight-bold">3m 42s</span>
              </div>
              <v-progress-linear
                :model-value="65"
                color="info"
                height="8"
                rounded
              />
            </div>
            
            <div>
              <div class="d-flex justify-space-between mb-1">
                <span class="text-subtitle-2">Response Quality</span>
                <span class="font-weight-bold">85%</span>
              </div>
              <v-progress-linear
                :model-value="85"
                color="warning"
                height="8"
                rounded
              />
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useSnackbarStore } from '@/stores/snackbar'
import { useFormsStore } from '@/stores/forms'

const props = defineProps<{
  form: any
}>()

const router = useRouter()
const snackbarStore = useSnackbarStore()
const formsStore = useFormsStore()

const quickStats = computed(() => [
  {
    title: 'Views',
    value: props.form.view_count || 0,
    icon: 'mdi-eye',
    color: 'primary'
  },
  {
    title: 'Submissions',
    value: props.form.submission_count || 0,
    icon: 'mdi-inbox',
    color: 'success'
  },
  {
    title: 'Completion Rate',
    value: '78%',
    icon: 'mdi-check-circle',
    color: 'info'
  },
  {
    title: 'Avg. Time',
    value: '3m 42s',
    icon: 'mdi-clock',
    color: 'warning'
  }
])

const formUrl = computed(() => 
  `${window.location.origin}/forms/${props.form.id}/preview`
)

const recentSubmissions = computed(() => 
  // This would come from the API
  []
)

function formatDate(dateString: string) {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleString()
}

function copyUrl() {
  navigator.clipboard.writeText(formUrl.value)
  snackbarStore.success('Form URL copied to clipboard')
}

function editForm() {
  router.push(`/forms/${props.form.id}/edit`)
}

function previewForm() {
  window.open(formUrl.value, '_blank')
}

async function togglePublish() {
  try {
    if (props.form.status === 'published') {
      // Unpublish logic
      snackbarStore.info('Unpublish feature coming soon')
    } else {
      await formsStore.publishForm(props.form.id)
      snackbarStore.success('Form published successfully')
    }
  } catch (error) {
    snackbarStore.error('Failed to update form status')
  }
}

async function duplicateForm() {
  try {
    const duplicated = await formsStore.duplicateForm(props.form.id)
    snackbarStore.success('Form duplicated successfully')
    router.push(`/forms/${duplicated.id}`)
  } catch (error) {
    snackbarStore.error('Failed to duplicate form')
  }
}

function exportData() {
  snackbarStore.info('Export feature coming soon')
}

function viewAllSubmissions() {
  router.push(`/forms/${props.form.id}/submissions`)
}

function viewSubmission(id: number) {
  // Navigate to submission detail
  console.log('View submission:', id)
}
</script>

<style scoped>
.form-overview {
  padding: 0;
}
</style>
