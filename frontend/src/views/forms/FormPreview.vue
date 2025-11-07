<template>
  <v-app>
    <v-container fluid class="form-preview">
      <v-row justify="center">
        <v-col cols="12" md="8" lg="6">
          <!-- Loading State -->
          <div v-if="loading" class="text-center py-16">
            <v-progress-circular indeterminate color="primary" size="64" />
            <p class="text-subtitle-1 mt-4">Loading form...</p>
          </div>

          <!-- Success State -->
          <v-card v-else-if="submitted" class="pa-8 text-center">
            <v-icon size="80" color="success" class="mb-4">mdi-check-circle</v-icon>
            <h2 class="text-h4 font-weight-bold mb-4">
              {{ formSchema?.settings?.successMessage || 'Thank you for your submission!' }}
            </h2>
            <p class="text-body-1 text-medium-emphasis mb-6">
              Your response has been recorded successfully.
            </p>
            <v-btn
              v-if="formSchema?.settings?.allowMultipleSubmissions"
              color="primary"
              @click="resetForm"
            >
              Submit Another Response
            </v-btn>
          </v-card>

          <!-- Form State -->
          <v-card v-else-if="formSchema" class="form-card">
            <v-card-title class="text-h4 font-weight-bold pa-6">
              {{ formSchema.title }}
            </v-card-title>
            
            <v-card-subtitle v-if="formSchema.description" class="px-6 pb-4">
              {{ formSchema.description }}
            </v-card-subtitle>

            <!-- Progress Bar for Multi-page Forms -->
            <v-progress-linear
              v-if="formSchema.settings?.showProgressBar && totalPages > 1"
              :model-value="(currentPage / totalPages) * 100"
              color="primary"
              height="8"
              class="mb-4"
            />

            <v-divider />

            <v-card-text class="pa-6">
              <v-form ref="formRef" @submit.prevent="submitForm">
                <!-- Render Fields -->
                <div v-for="field in visibleFields" :key="field.id" class="mb-6">
                  <component
                    :is="getFieldComponent(field.type)"
                    v-model="formData[field.id]"
                    :field="field"
                    :is-preview="true"
                    @update:model-value="handleFieldChange(field)"
                  />
                </div>

                <!-- Honeypot (Hidden Anti-spam Field) -->
                <input
                  v-if="formSchema.settings?.enableHoneypot"
                  v-model="honeypot"
                  type="text"
                  name="website"
                  style="display: none"
                  tabindex="-1"
                  autocomplete="off"
                />

                <!-- CAPTCHA -->
                <div v-if="formSchema.settings?.enableCaptcha" class="mb-6">
                  <v-alert type="info" variant="tonal">
                    CAPTCHA verification would appear here
                  </v-alert>
                </div>

                <!-- Error Alert -->
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

                <!-- Form Actions -->
                <div class="d-flex gap-2 mt-6">
                  <v-btn
                    v-if="currentPage > 1"
                    variant="outlined"
                    @click="previousPage"
                  >
                    Previous
                  </v-btn>

                  <v-spacer />

                  <v-btn
                    v-if="formSchema.settings?.saveProgress"
                    variant="outlined"
                    prepend-icon="mdi-content-save"
                    @click="saveProgress"
                  >
                    Save Progress
                  </v-btn>

                  <v-btn
                    v-if="currentPage < totalPages"
                    color="primary"
                    @click="nextPage"
                  >
                    Next
                  </v-btn>

                  <v-btn
                    v-else
                    type="submit"
                    color="primary"
                    :loading="submitting"
                  >
                    {{ formSchema.settings?.submitButtonText || 'Submit' }}
                  </v-btn>
                </div>
              </v-form>
            </v-card-text>
          </v-card>

          <!-- Error State -->
          <v-card v-else class="pa-8 text-center">
            <v-icon size="80" color="error" class="mb-4">mdi-alert-circle</v-icon>
            <h2 class="text-h4 font-weight-bold mb-4">Form Not Found</h2>
            <p class="text-body-1 text-medium-emphasis">
              The form you're looking for doesn't exist or has been removed.
            </p>
          </v-card>

          <!-- Powered by FusionForms -->
          <div class="text-center mt-4">
            <p class="text-caption text-medium-emphasis">
              Powered by <span class="font-weight-bold">FusionForms</span>
            </p>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue'
import { useRoute } from 'vue-router'
import apiClient from '@/services/api'

// Import field components
import FieldText from '@/components/form-builder/fields/FieldText.vue'
import FieldTextarea from '@/components/form-builder/fields/FieldTextarea.vue'
import FieldNumber from '@/components/form-builder/fields/FieldNumber.vue'
import FieldEmail from '@/components/form-builder/fields/FieldEmail.vue'
import FieldUrl from '@/components/form-builder/fields/FieldUrl.vue'
import FieldDate from '@/components/form-builder/fields/FieldDate.vue'
import FieldTime from '@/components/form-builder/fields/FieldTime.vue'
import FieldCheckbox from '@/components/form-builder/fields/FieldCheckbox.vue'
import FieldRatio from '@/components/form-builder/fields/FieldRadio.vue'
import FieldSelect from '@/components/form-builder/fields/FieldSelect.vue'
import FieldFile from '@/components/form-builder/fields/FieldFile.vue'
import FieldRating from '@/components/form-builder/fields/FieldRating.vue'
import FieldSignature from '@/components/form-builder/fields/FieldSignature.vue'
import FieldRichtext from '@/components/form-builder/fields/FieldRichtext.vue'
import FieldHeading from '@/components/form-builder/fields/FieldHeading.vue'
import FieldParagraph from '@/components/form-builder/fields/FieldParagraph.vue'
import FieldDivider from '@/components/form-builder/fields/FieldDivider.vue'
import FieldImage from '@/components/form-builder/fields/FieldImage.vue'

const route = useRoute()
const formId = route.params.id

const loading = ref(true)
const submitting = ref(false)
const submitted = ref(false)
const formSchema = ref<any>(null)
const formData = reactive<Record<string, any>>({})
const formRef = ref()
const errorMessage = ref('')
const honeypot = ref('')
const currentPage = ref(1)

const totalPages = computed(() => {
  // Calculate total pages based on form structure
  // For now, we'll treat it as a single page
  return 1
})

const visibleFields = computed(() => {
  if (!formSchema.value?.fields) return []
  
  return formSchema.value.fields.filter((field: any) => {
    // Check conditional visibility
    if (field.conditionalVisibility?.enabled) {
      const dependentField = field.conditionalVisibility.field
      const operator = field.conditionalVisibility.operator
      const expectedValue = field.conditionalVisibility.value
      const actualValue = formData[dependentField]

      switch (operator) {
        case 'equals':
          if (actualValue !== expectedValue) return false
          break
        case 'not_equals':
          if (actualValue === expectedValue) return false
          break
        case 'contains':
          if (!actualValue || !actualValue.includes(expectedValue)) return false
          break
        case 'not_contains':
          if (actualValue && actualValue.includes(expectedValue)) return false
          break
        case 'is_empty':
          if (actualValue) return false
          break
        case 'is_not_empty':
          if (!actualValue) return false
          break
      }
    }
    
    return true
  })
})

onMounted(async () => {
  await fetchForm()
  loadSavedProgress()
})

async function fetchForm() {
  loading.value = true
  try {
    // Use public endpoint for published forms (no auth required)
    const response = await apiClient.get(`/forms/public/${formId}/`)
    formSchema.value = response.data.schema || response.data
    
    // Initialize form data with default values
    if (formSchema.value?.fields) {
      formSchema.value.fields.forEach((field: any) => {
        if (field.options?.defaultValue !== undefined) {
          formData[field.id || ''] = field.options.defaultValue
        } else {
          formData[field.id || ''] = null
        }
      })
    }
  } catch (error: any) {
    console.error('Error fetching form:', error)
    errorMessage.value = error.response?.data?.detail || 'Failed to load form. The form may not exist or may not be published.'
    loading.value = false
  } finally {
    loading.value = false
  }
}

function getFieldComponent(type: string) {
  const componentMap: Record<string, any> = {
    text: FieldText,
    textarea: FieldTextarea,
    number: FieldNumber,
    email: FieldEmail,
    url: FieldUrl,
    date: FieldDate,
    time: FieldTime,
    checkbox: FieldCheckbox,
    radio: FieldRatio,
    select: FieldSelect,
    file: FieldFile,
    rating: FieldRating,
    signature: FieldSignature,
    richtext: FieldRichtext,
    heading: FieldHeading,
    paragraph: FieldParagraph,
    divider: FieldDivider,
    image: FieldImage
  }
  return componentMap[type] || FieldText
}

function handleFieldChange(field: any) {
  // Handle field changes (useful for conditional logic)
}

function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

function previousPage() {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

function saveProgress() {
  try {
    localStorage.setItem(`form_${formId}_progress`, JSON.stringify(formData))
    alert('Progress saved! You can return later to complete the form.')
  } catch (error) {
    console.error('Error saving progress:', error)
  }
}

function loadSavedProgress() {
  try {
    const saved = localStorage.getItem(`form_${formId}_progress`)
    if (saved) {
      const savedData = JSON.parse(saved)
      Object.assign(formData, savedData)
    }
  } catch (error) {
    console.error('Error loading saved progress:', error)
  }
}

async function submitForm() {
  // Validate form
  const { valid } = await formRef.value.validate()
  if (!valid) {
    errorMessage.value = 'Please fill in all required fields correctly'
    return
  }

  // Check honeypot
  if (honeypot.value) {
    console.warn('Honeypot triggered')
    return
  }

  submitting.value = true
  errorMessage.value = ''

  try {
    // Use public submission endpoint (no auth required)
    await apiClient.post(`/submissions/public/${formId}/`, {
      data: formData,
      recaptchaToken: null // Add reCAPTCHA token if enabled
    })

    submitted.value = true

    // Clear saved progress
    localStorage.removeItem(`form_${formId}_progress`)

    // Redirect if configured
    if (formSchema.value?.settings?.redirectUrl) {
      setTimeout(() => {
        window.location.href = formSchema.value.settings.redirectUrl
      }, 2000)
    }
  } catch (error: any) {
    console.error('Submission error:', error)
    const errorDetail = error.response?.data
    if (errorDetail?.data) {
      errorMessage.value = `Validation error: ${JSON.stringify(errorDetail.data)}`
    } else if (errorDetail?.recaptcha) {
      errorMessage.value = 'reCAPTCHA verification failed. Please try again.'
    } else {
      errorMessage.value = errorDetail?.detail || errorDetail?.message || 'Failed to submit form. Please try again.'
    }
  } finally {
    submitting.value = false
  }
}

function resetForm() {
  submitted.value = false
  Object.keys(formData).forEach(key => {
    delete formData[key]
  })
  currentPage.value = 1
  
  // Reinitialize with default values
  formSchema.value.fields?.forEach((field: any) => {
    if (field.options?.defaultValue) {
      formData[field.id] = field.options.defaultValue
    }
  })
}
</script>

<style scoped>
.form-preview {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40px 20px;
}

.form-card {
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}
</style>

