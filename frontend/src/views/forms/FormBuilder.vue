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
              v-model="formSchema.settings.submitButtonText"
              label="Submit Button Text"
              default-value="Submit"
            />
            <v-text-field
              v-model="formSchema.settings.successMessage"
              label="Success Message"
              default-value="Thank you for your submission!"
            />
            <v-checkbox
              v-model="formSchema.settings.saveProgress"
              label="Allow users to save progress"
            />
            <v-checkbox
              v-model="formSchema.settings.multipleSubmissions"
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
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useFormsStore } from '@/stores/forms'
import FieldPalette from '@/components/form-builder/FieldPalette.vue'
import FormCanvas from '@/components/form-builder/FormCanvas.vue'
import FieldProperties from '@/components/form-builder/FieldProperties.vue'
import FormPreview from '@/components/form-builder/FormPreview.vue'

// Pinia store
const formsStore = useFormsStore()
const router = useRouter()
const route = useRoute()

// Reactive state
const selectedFieldIndex = ref<number>(-1)
const selectedField = ref<any>(null)
const showFormSettings = ref(false)
const showPreview = ref(false)
const saving = ref(false)
const publishing = ref(false)

// Computed
const isEditing = computed(() => !!route.params.id)
const currentForm = computed(() => formsStore.currentForm)
const formSchema = computed({
  get: () => formsStore.formSchema,
  set: (value) => formsStore.setFormSchema(value)
})
const formId = computed(() => currentForm.value?.id)

// Lifecycle
onMounted(async () => {
  if (isEditing.value) {
    await formsStore.fetchForm(route.params.id as string)
  } else {
    formsStore.resetFormSchema()
  }
})

// Methods
function selectField(index: number) {
  selectedFieldIndex.value = index
  selectedField.value = index >= 0 ? formSchema.value.fields[index] : null
}

function goBack() {
  router.push('/forms')
}

async function saveForm() {
  saving.value = true
  try {
    if (isEditing.value) {
      await formsStore.updateForm({
        id: formId.value!,
        formData: { ...currentForm.value, schema: formSchema.value }
      })
    } else {
      const newForm = await formsStore.createForm({
        title: formSchema.value.title || 'Untitled Form',
        description: formSchema.value.description || '',
        schema: formSchema.value
      })
      router.replace(`/forms/${newForm.id}/edit`)
    }
    formsStore.showSnackbar({ message: 'Form saved successfully', color: 'success' })
  } catch (error) {
    formsStore.showSnackbar({ message: 'Error saving form', color: 'error' })
  } finally {
    saving.value = false
  }
}

async function publishForm() {
  publishing.value = true
  try {
    await formsStore.publishForm(formId.value!)
    formsStore.showSnackbar({ message: 'Form published successfully', color: 'success' })
  } catch (error) {
    formsStore.showSnackbar({ message: 'Error publishing form', color: 'error' })
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
