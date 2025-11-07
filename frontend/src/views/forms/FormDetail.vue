<template>
  <v-container fluid class="form-detail">
    <v-row v-if="loading">
      <v-col cols="12" class="text-center">
        <v-progress-circular indeterminate color="primary" size="64" />
      </v-col>
    </v-row>

    <template v-else-if="form">
      <!-- Header -->
      <v-row>
        <v-col cols="12">
          <div class="d-flex align-center mb-4">
            <v-btn
              icon="mdi-arrow-left"
              variant="text"
              @click="goBack"
            />
            <div class="ml-4">
              <h1 class="text-h4 font-weight-bold">{{ form.name }}</h1>
              <p class="text-subtitle-1 text-medium-emphasis">{{ form.description }}</p>
            </div>
            <v-spacer />
            <v-chip :color="getStatusColor(form.status)" class="mr-2">
              {{ form.status }}
            </v-chip>
            <v-menu>
              <template #activator="{ props }">
                <v-btn
                  icon="mdi-dots-vertical"
                  variant="text"
                  v-bind="props"
                />
              </template>
              <v-list>
                <v-list-item 
                  v-if="canEditForm"
                  @click="editForm"
                >
                  <template #prepend>
                    <v-icon>mdi-pencil</v-icon>
                  </template>
                  <v-list-item-title>Edit</v-list-item-title>
                </v-list-item>
                <v-list-item 
                  v-if="canDuplicateForm"
                  @click="duplicateForm"
                >
                  <template #prepend>
                    <v-icon>mdi-content-copy</v-icon>
                  </template>
                  <v-list-item-title>Duplicate</v-list-item-title>
                </v-list-item>
                <v-list-item 
                  v-if="canManageWebhooks"
                  @click="showEmbedDialog = true"
                >
                  <template #prepend>
                    <v-icon>mdi-code-tags</v-icon>
                  </template>
                  <v-list-item-title>Embed Code</v-list-item-title>
                </v-list-item>
                <v-divider v-if="canDeleteForm" />
                <v-list-item 
                  v-if="canDeleteForm"
                  @click="showDeleteDialog = true" 
                  class="text-error"
                >
                  <template #prepend>
                    <v-icon color="error">mdi-delete</v-icon>
                  </template>
                  <v-list-item-title>Delete</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </div>
        </v-col>
      </v-row>

      <!-- Tabs -->
      <v-row>
        <v-col cols="12">
          <v-tabs v-model="activeTab" color="primary">
            <v-tab value="overview">
              <v-icon start>mdi-view-dashboard</v-icon>
              Overview
            </v-tab>
            <v-tab 
              v-if="canViewSubmissions"
              value="submissions"
            >
              <v-icon start>mdi-inbox</v-icon>
              Submissions
              <v-chip size="small" class="ml-2">{{ form.submission_count || 0 }}</v-chip>
            </v-tab>
            <v-tab 
              v-if="canViewAnalytics"
              value="analytics"
            >
              <v-icon start>mdi-chart-line</v-icon>
              Analytics
            </v-tab>
            <v-tab 
              v-if="canManageWebhooks"
              value="settings"
            >
              <v-icon start>mdi-cog</v-icon>
              Settings
            </v-tab>
          </v-tabs>

          <v-window v-model="activeTab" class="mt-4">
            <v-window-item value="overview">
              <FormOverview :form="form" />
            </v-window-item>

            <v-window-item 
              v-if="canViewSubmissions"
              value="submissions"
            >
              <FormSubmissions :form-id="formId.value" />
            </v-window-item>

            <v-window-item 
              v-if="canViewAnalytics"
              value="analytics"
            >
              <FormAnalytics :form-id="formId.value" />
            </v-window-item>

            <v-window-item 
              v-if="canManageWebhooks"
              value="settings"
            >
              <FormSettings :form="form" @update="handleFormUpdate" />
            </v-window-item>
          </v-window>
        </v-col>
      </v-row>
    </template>

    <!-- Embed Code Dialog -->
    <v-dialog v-model="showEmbedDialog" max-width="600">
      <v-card>
        <v-card-title>Embed Code</v-card-title>
        <v-card-text>
          <p class="text-subtitle-2 mb-4">
            Copy and paste this code into your website to embed the form:
          </p>
          
          <v-tabs v-model="embedTab" color="primary">
            <v-tab value="iframe">iFrame</v-tab>
            <v-tab value="script">JavaScript</v-tab>
          </v-tabs>

          <v-window v-model="embedTab" class="mt-4">
            <v-window-item value="iframe">
              <v-textarea
                :model-value="iframeEmbedCode"
                readonly
                rows="4"
                variant="outlined"
              />
            </v-window-item>
            <v-window-item value="script">
              <v-textarea
                :model-value="scriptEmbedCode"
                readonly
                rows="6"
                variant="outlined"
              />
            </v-window-item>
          </v-window>

          <v-btn
            block
            color="primary"
            prepend-icon="mdi-content-copy"
            @click="copyEmbedCode"
          >
            Copy to Clipboard
          </v-btn>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="showEmbedDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="showDeleteDialog" max-width="400">
      <v-card>
        <v-card-title class="text-error">Delete Form</v-card-title>
        <v-card-text>
          <p>Are you sure you want to delete this form? This action cannot be undone.</p>
          <p class="text-caption text-medium-emphasis mt-2">
            All submissions and analytics data will be permanently deleted.
          </p>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="showDeleteDialog = false">Cancel</v-btn>
          <v-btn color="error" @click="handleDelete">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useFormsStore } from '@/stores/forms'
import { useSnackbarStore } from '@/stores/snackbar'
import { usePermissions } from '@/composables/usePermissions'
import FormOverview from './FormOverview.vue'
import FormSubmissions from './FormSubmissions.vue'
import FormAnalytics from './FormAnalytics.vue'
import FormSettings from './FormSettings.vue'

const route = useRoute()
const router = useRouter()
const formsStore = useFormsStore()
const snackbarStore = useSnackbarStore()
const { 
  canEditForm, 
  canDeleteForm, 
  canDuplicateForm, 
  canManageWebhooks,
  canViewSubmissions,
  canViewAnalytics
} = usePermissions()

const formId = computed(() => String(route.params.id))
const activeTab = ref('overview')
const loading = ref(false)
const showEmbedDialog = ref(false)
const showDeleteDialog = ref(false)
const embedTab = ref('iframe')

const form = computed(() => formsStore.currentForm)

const baseUrl = computed(() => window.location.origin)

const iframeEmbedCode = computed(() => 
  `<iframe src="${baseUrl.value}/forms/${formId.value}/preview" width="100%" height="600" frameborder="0"></iframe>`
)

const scriptEmbedCode = computed(() => 
  `<div id="fusionforms-${formId.value}"></div>
<script src="${baseUrl.value}/embed.js"></script>
<script>
  FusionForms.embed('${formId.value}', 'fusionforms-${formId.value}');
</script>`
)

onMounted(async () => {
  loading.value = true
  try {
    await formsStore.fetchForm(formId.value)
  } catch (error) {
    snackbarStore.error('Failed to load form')
    router.push('/forms')
  } finally {
    loading.value = false
  }
})

function getStatusColor(status: string) {
  const colorMap: Record<string, string> = {
    draft: 'grey',
    published: 'green',
    archived: 'orange'
  }
  return colorMap[status] || 'grey'
}

function goBack() {
  router.push('/forms')
}

function editForm() {
  router.push(`/forms/${formId.value}/edit`)
}

async function duplicateForm() {
  try {
    const duplicated = await formsStore.duplicateForm(formId.value)
    snackbarStore.success('Form duplicated successfully')
    router.push(`/forms/${duplicated.id}`)
  } catch (error) {
    snackbarStore.error('Failed to duplicate form')
  }
}

function copyEmbedCode() {
  const code = embedTab.value === 'iframe' ? iframeEmbedCode.value : scriptEmbedCode.value
  navigator.clipboard.writeText(code)
  snackbarStore.success('Embed code copied to clipboard')
}

async function handleDelete() {
  try {
    await formsStore.deleteForm(formId.value)
    snackbarStore.success('Form deleted successfully')
    router.push('/forms')
  } catch (error) {
    snackbarStore.error('Failed to delete form')
  }
  showDeleteDialog.value = false
}

function handleFormUpdate(updatedForm: any) {
  formsStore.setCurrentForm(updatedForm)
  snackbarStore.success('Form updated successfully')
}
</script>

<style scoped>
.form-detail {
  padding: 24px;
}
</style>
