<template>
  <div class="form-builder">
    <!-- App Bar -->
    <v-app-bar color="primary" dark>
      <v-btn icon="mdi-arrow-left" @click="goBack" />
      <v-toolbar-title>{{ isEditing ? 'Edit Form' : 'Create Form' }}</v-toolbar-title>
      <v-spacer />
      <v-btn variant="text" @click="previewForm">
        <v-icon left>mdi-eye</v-icon>
        Preview
      </v-btn>
      <v-btn variant="text" @click="saveForm" :loading="saving">
        <v-icon left>mdi-content-save</v-icon>
        Save
      </v-btn>
      <v-btn
        variant="elevated"
        @click="publishForm"
        :loading="publishing"
        :disabled="!formId"
      >
        <v-icon left>mdi-publish</v-icon>
        Publish
      </v-btn>
    </v-app-bar>

    <!-- Main Container -->
    <v-container fluid class="form-builder-container">
      <v-row>
        <v-col cols="12" md="3">
          <FieldPalette />
        </v-col>

        <v-col cols="12" md="6">
          <FormCanvas
            v-model:formSchema="formSchema"
            :selected-field-index="selectedFieldIndex"
            @select-field="selectField"
          />
        </v-col>

        <v-col cols="12" md="3">
          <FieldProperties
            v-model:selectedField="selectedField"
            :form-schema="formSchema"
          />
        </v-col>
      </v-row>
    </v-container>

    <!-- Form Settings Dialog -->
    <v-dialog v-model="showFormSettings" max-width="600">
      <v-card>
        <v-card-title>Form Settings</v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field v-model="formSchema.title" label="Form Title" required />
            <v-textarea v-model="formSchema.description" label="Form Description" />
            <v-text-field
              v-model="formSchema.settings!.submitButtonText"
              label="Submit Button Text"
              default-value="Submit"
            />
            <v-text-field
              v-model="formSchema.settings!.successMessage"
              label="Success Message"
              default-value="Thank you for your submission!"
            />
            <v-checkbox
              v-model="formSchema.settings!.saveProgress"
              label="Allow users to save progress"
            />
            <v-checkbox
              v-model="formSchema.settings!.multipleSubmissions"
              label="Allow multiple submissions"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="showFormSettings = false">Cancel</v-btn>
          <v-btn color="primary" @click="showFormSettings = false">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Preview Dialog -->
    <v-dialog v-model="showPreview" fullscreen>
      <v-card>
        <v-app-bar color="primary" dark>
          <v-toolbar-title>Form Preview</v-toolbar-title>
          <v-spacer />
          <v-btn icon @click="showPreview = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-app-bar>
        <v-card-text>
          <FormPreview :form-schema="formSchema" />
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useFormsStore } from '@/stores/forms'
import { useSnackbarStore } from '@/stores/snackbar'
import FieldPalette from '@/components/form-builder/FieldPalette.vue'
import FormCanvas from '@/components/form-builder/FormCanvas.vue'
import FieldProperties from '@/components/form-builder/FieldProperties.vue'
import FormPreview from '@/components/form-builder/FormPreview.vue'

// Pinia stores
const formsStore = useFormsStore()
const snackbarStore = useSnackbarStore()
const router = useRouter()
const route = useRoute()

// Reactive state
const selectedFieldIndex = ref<number>(-1)
const selectedField = ref<any>(null)
const showFormSettings = ref(false)
const showPreview = ref(false)
const saving = ref(false)
const publishing = ref(false)

// Default schema for fallback
const defaultSchema = {
  title: '',
  description: '',
  fields: [],
  settings: {
    submitButtonText: 'Submit',
    successMessage: 'Thank you for your submission!',
    saveProgress: false,
    multipleSubmissions: false,
    allowMultipleSubmissions: false,
    showProgressBar: false,
    enableHoneypot: false,
    enableCaptcha: false,
    redirectUrl: ''
  }
}

// Computed
const isEditing = computed(() => !!route.params.id)
const currentForm = computed(() => formsStore.currentForm)

// Use a ref to track the formSchema to avoid readonly computed issues
// This allows direct mutations while still syncing with the store
const formSchemaRef = ref({ ...defaultSchema, ...formsStore.formSchema })

// Sync store changes to local ref (one-way: store -> local)
watch(() => formsStore.formSchema, (newSchema) => {
  if (newSchema) {
    // Deep merge to preserve local changes that haven't been saved
    const current = formSchemaRef.value
    formSchemaRef.value = {
      ...defaultSchema,
      ...newSchema,
      // Preserve fields if they exist in local but not in store
      fields: newSchema.fields && newSchema.fields.length > 0 
        ? newSchema.fields 
        : (current.fields || [])
    }
  }
}, { immediate: true, deep: true })

const formSchema = computed({
  get: () => {
    // Always return a valid schema
    const schema = formSchemaRef.value
    return {
      ...defaultSchema,
      ...schema,
      fields: schema.fields || [],
      settings: {
        ...defaultSchema.settings,
        ...(schema.settings || {})
      }
    }
  },
  set: (value) => {
    // Update local ref and sync to store
    formSchemaRef.value = {
      ...defaultSchema,
      ...value,
      fields: value.fields || [],
      settings: {
        ...defaultSchema.settings,
        ...(value.settings || {})
      }
    }
    // Update store asynchronously to avoid circular updates
    nextTick(() => {
      formsStore.setFormSchema(formSchemaRef.value)
    })
  }
})

const formId = computed(() => {
  const id = currentForm.value?.id
  // Backend uses UUID strings, ensure we return a string
  return id ? String(id) : null
})

// Lifecycle
onMounted(async () => {
  // Always initialize schema first
  formsStore.resetFormSchema()
  formSchemaRef.value = { ...defaultSchema, ...formsStore.formSchema }
  
  if (isEditing.value && route.params.id) {
    // Backend uses UUID (string), so pass it as string
    try {
      await formsStore.fetchForm(String(route.params.id))
      formSchemaRef.value = { ...defaultSchema, ...formsStore.formSchema }
    } catch (error) {
      console.error('Error fetching form:', error)
    }
  }
})

// Methods
function selectField(index: number) {
  selectedFieldIndex.value = index
  const schema = formSchema.value
  if (schema && schema.fields && index >= 0 && index < schema.fields.length) {
    selectedField.value = schema.fields[index]
  } else {
    selectedField.value = null
  }
}

function goBack() {
  router.push('/forms')
}

async function saveForm() {
  saving.value = true
  try {
    const schema = formSchema.value
    if (!schema) {
      snackbarStore.error('Form schema is not initialized')
      return
    }
    
    if (isEditing.value && formId.value) {
      // Update existing form
      await formsStore.updateForm(formId.value, {
        title: schema.title || 'Untitled Form',
        description: schema.description || '',
        schema: schema
      })
      snackbarStore.success('Form saved successfully')
    } else {
      // Create new form
      const newForm = await formsStore.createForm({
        title: schema.title || 'Untitled Form',
        description: schema.description || '',
        schema: schema
      })
      router.replace(`/forms/${newForm.id}/edit`)
      snackbarStore.success('Form created successfully')
    }
  } catch (error: any) {
    console.error('Error saving form:', error)
    snackbarStore.error(error.response?.data?.detail || error.message || 'Error saving form')
  } finally {
    saving.value = false
  }
}

async function publishForm() {
  if (!formId.value) {
    snackbarStore.error('Please save the form before publishing')
    return
  }
  publishing.value = true
  try {
    await formsStore.publishForm(formId.value)
    snackbarStore.success('Form published successfully')
  } catch (error: any) {
    console.error('Error publishing form:', error)
    snackbarStore.error(error.response?.data?.detail || error.message || 'Error publishing form')
  } finally {
    publishing.value = false
  }
}

function previewForm() {
  showPreview.value = true
}
</script>

<style scoped>
.form-builder {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.form-builder-container {
  flex: 1;
  padding: 0;
  height: calc(100vh - 64px);
}

.form-builder-container .v-row {
  height: 100%;
  margin: 0;
}

.form-builder-container .v-col {
  height: 100%;
  padding: 12px;
  overflow-y: auto;
}
</style>
