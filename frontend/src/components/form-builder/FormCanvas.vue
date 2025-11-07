<template>
  <div class="form-canvas">
    <v-card>
      <v-card-title class="text-h6">
        <v-text-field
          v-if="isEditingTitle"
          v-model="editableTitle"
          variant="plain"
          density="compact"
          hide-details
          autofocus
          @blur="saveTitle"
          @keyup.enter="saveTitle"
          @keyup.esc="cancelEditTitle"
          class="title-edit-field"
        />
        <span
          v-else
          @click="startEditTitle"
          class="title-editable"
          :title="'Click to edit title'"
        >
          {{ formSchema?.title || 'Untitled Form' }}
        </span>
      </v-card-title>
      <v-card-subtitle class="description-editable">
        <v-textarea
          v-if="isEditingDescription"
          v-model="editableDescription"
          variant="plain"
          density="compact"
          hide-details
          rows="2"
          autofocus
          placeholder="Add a description (click to edit)"
          @blur="saveDescription"
          @keyup.esc="cancelEditDescription"
          class="description-edit-field"
        />
        <span
          v-else
          @click="startEditDescription"
          :title="'Click to edit description'"
          class="description-text"
        >
          {{ formSchema?.description || 'Add a description (click to edit)' }}
        </span>
      </v-card-subtitle>
      <v-card-text>
        <div
          class="form-fields"
          :class="{ 'drag-over': isDraggingOver }"
          @drop="onDrop"
          @dragover.prevent="onDragOver"
          @dragenter.prevent="onDragEnter"
          @dragleave="onDragLeave"
        >
          <draggable
            v-if="formSchema && formSchema.fields"
            v-model="localFormSchema.fields"
            group="formFields"
            item-key="id"
            @change="onFieldChange"
          >
            <template #item="{ element: field, index }">
              <div
                class="form-field"
                :class="{ selected: selectedFieldIndex === index }"
                @click="selectField(index)"
              >
                <component
                  :is="getFieldComponent(field.type)"
                  :field="field"
                  :is-preview="false"
                  @update="updateField(index, $event)"
                />
                <v-menu>
                  <template #activator="{ props }">
                    <v-btn
                      icon="mdi-dots-vertical"
                      size="small"
                      variant="text"
                      v-bind="props"
                      class="field-menu"
                    />
                  </template>
                  <v-list>
                    <v-list-item @click="duplicateField(index)">
                      <v-list-item-title>Duplicate</v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="removeField(index)">
                      <v-list-item-title>Delete</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </div>
            </template>
          </draggable>

          <div v-if="!formSchema || !formSchema.fields || formSchema.fields.length === 0" class="empty-state">
            <v-icon size="48">mdi-drag</v-icon>
            <p>Drag fields here to start building your form</p>
          </div>
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref, computed, watch } from 'vue'
import draggable from 'vuedraggable'

import FieldText from './fields/FieldText.vue'
import FieldTextarea from './fields/FieldTextarea.vue'
import FieldNumber from './fields/FieldNumber.vue'
import FieldEmail from './fields/FieldEmail.vue'
import FieldUrl from './fields/FieldUrl.vue'
import FieldDate from './fields/FieldDate.vue'
import FieldTime from './fields/FieldTime.vue'
import FieldCheckbox from './fields/FieldCheckbox.vue'
import FieldRadio from './fields/FieldRadio.vue'
import FieldSelect from './fields/FieldSelect.vue'
import FieldFile from './fields/FieldFile.vue'
import FieldRating from './fields/FieldRating.vue'
import FieldSignature from './fields/FieldSignature.vue'
import FieldHidden from './fields/FieldHidden.vue'
import FieldRichtext from './fields/FieldRichtext.vue'
import FieldHeading from './fields/FieldHeading.vue'
import FieldParagraph from './fields/FieldParagraph.vue'
import FieldDivider from './fields/FieldDivider.vue'
import FieldImage from './fields/FieldImage.vue'
import type { FormField, FormSchema } from '@/stores/forms'

/* ----------------- TYPES ----------------- */
// Use Field as an alias for FormField for local use
type Field = FormField

/* ----------------- PROPS ----------------- */
const props = defineProps<{
  formSchema?: FormSchema | null
  selectedFieldIndex: number
}>()

const emit = defineEmits<{
  (e: 'update:formSchema', value: FormSchema): void
  (e: 'selectField', index: number): void
}>()

/* ----------------- STATE ----------------- */
const isDraggingOver = ref(false)
const isEditingTitle = ref(false)
const isEditingDescription = ref(false)
const editableTitle = ref('')
const editableDescription = ref('')

// Create a local reactive copy of formSchema to avoid mutating props
const localFormSchema = ref<FormSchema>({
  title: '',
  description: '',
  fields: [],
  settings: {}
})

// Sync prop changes to local schema
watch(() => props.formSchema, (newSchema) => {
  if (newSchema) {
    localFormSchema.value = {
      title: newSchema.title || '',
      description: newSchema.description || '',
      fields: newSchema.fields ? [...newSchema.fields] : [],
      settings: newSchema.settings || {
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
  } else {
    // Initialize with empty schema if prop is null/undefined
    localFormSchema.value = {
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
  }
}, { immediate: true, deep: true })

// Computed property for template display
const formSchema = computed(() => localFormSchema.value)

// Helper function to update and emit schema
function updateSchema(updater: (schema: FormSchema) => void) {
  const updatedSchema = { ...localFormSchema.value }
  updater(updatedSchema)
  localFormSchema.value = updatedSchema
  emit('update:formSchema', updatedSchema)
}

// Title editing functions
function startEditTitle() {
  editableTitle.value = formSchema.value?.title || ''
  isEditingTitle.value = true
}

function saveTitle() {
  if (editableTitle.value.trim()) {
    updateSchema((schema) => {
      schema.title = editableTitle.value.trim()
    })
  }
  isEditingTitle.value = false
}

function cancelEditTitle() {
  editableTitle.value = formSchema.value?.title || ''
  isEditingTitle.value = false
}

// Description editing functions
function startEditDescription() {
  editableDescription.value = formSchema.value?.description || ''
  isEditingDescription.value = true
}

function saveDescription() {
  updateSchema((schema) => {
    schema.description = editableDescription.value.trim()
  })
  isEditingDescription.value = false
}

function cancelEditDescription() {
  editableDescription.value = formSchema.value?.description || ''
  isEditingDescription.value = false
}

/* ----------------- METHODS ----------------- */
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
    radio: FieldRadio,
    select: FieldSelect,
    file: FieldFile,
    rating: FieldRating,
    signature: FieldSignature,
    hidden: FieldHidden,
    richtext: FieldRichtext,
    heading: FieldHeading,
    paragraph: FieldParagraph,
    divider: FieldDivider,
    image: FieldImage
  }
  return componentMap[type] || FieldText
}

function getDefaultOptions(type: string) {
  const defaultOptions: Record<string, any> = {
    text: { placeholder: 'Enter text here' },
    textarea: { placeholder: 'Enter text here', rows: 3 },
    number: { placeholder: 'Enter number', min: null, max: null },
    email: { placeholder: 'Enter email address' },
    url: { placeholder: 'https://example.com' },
    date: { placeholder: 'Select date' },
    time: { placeholder: 'Select time' },
    checkbox: { options: [{ label: 'Option 1', value: 'option1' }] },
    radio: { options: [{ label: 'Option 1', value: 'option1' }] },
    select: { options: [{ label: 'Option 1', value: 'option1' }], multiple: false },
    file: { accept: '*', multiple: false },
    rating: { max: 5, icons: ['mdi-star-outline', 'mdi-star'] },
    signature: { width: 300, height: 150 },
    hidden: { value: '' },
    richtext: { placeholder: 'Enter rich text here' },
    heading: { level: 2, text: 'Heading' },
    paragraph: { text: 'This is a paragraph text. You can edit it.' },
    divider: { style: 'solid' },
    image: { src: '', alt: 'Image', width: '100%', height: 'auto' }
  }
  return defaultOptions[type] || {}
}

function onDragOver(event: DragEvent) {
  event.preventDefault()
  if (event.dataTransfer) {
    event.dataTransfer.dropEffect = 'copy'
  }
}

function onDragEnter(event: DragEvent) {
  event.preventDefault()
  isDraggingOver.value = true
}

function onDragLeave(event: DragEvent) {
  // Only set to false if leaving the drop zone, not a child element
  const target = event.target as HTMLElement
  const relatedTarget = event.relatedTarget as HTMLElement
  if (!target.contains(relatedTarget)) {
    isDraggingOver.value = false
  }
}

function onDrop(event: DragEvent) {
  event.preventDefault()
  event.stopPropagation()
  isDraggingOver.value = false
  
  try {
    if (!event.dataTransfer) {
      console.error('No dataTransfer in drop event')
      return
    }
    
    const fieldDataStr = event.dataTransfer.getData('application/json')
    if (!fieldDataStr) {
      console.error('No data in drop event')
      return
    }
    
    const fieldData = JSON.parse(fieldDataStr)
    console.log('Dropping field:', fieldData)
    
    // Generate a default label based on field type if not provided
    // Use the label from fieldData if available, otherwise format the type
    let defaultLabel = fieldData.label
    if (!defaultLabel) {
      // Format field type: 'text' -> 'Text', 'text_area' -> 'Text Area'
      defaultLabel = fieldData.type
        .split(/[-_]/)
        .map((word: string) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(' ')
    }
    
    const newField: Field = {
      id: `field_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      type: fieldData.type,
      label: defaultLabel,
      required: false,
      options: getDefaultOptions(fieldData.type)
    }
    
    // Ensure fields array exists and add the new field
    updateSchema((schema) => {
      if (!schema.fields) {
        schema.fields = []
      }
      schema.fields.push(newField)
    })
    
    selectField(localFormSchema.value.fields.length - 1)
    
    console.log('Field added successfully', newField)
  } catch (error) {
    console.error('Error in onDrop:', error)
  }
}

function onFieldChange() {
  // Draggable v-model automatically updates localFormSchema.fields
  // Just emit the update to sync with parent
  emit('update:formSchema', localFormSchema.value)
}

function selectField(index: number) {
  emit('selectField', index)
}

function updateField(index: number, field: any) {
  // Ensure field has all required properties
  const updatedField: Field = {
    id: field.id || `field_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
    type: field.type || 'text',
    label: field.label || '',
    required: field.required || false,
    options: field.options || {}
  }
  updateSchema((schema) => {
    if (schema.fields && index >= 0 && index < schema.fields.length) {
      schema.fields.splice(index, 1, updatedField)
    }
  })
}

function duplicateField(index: number) {
  if (!localFormSchema.value.fields || index < 0 || index >= localFormSchema.value.fields.length) return
  const originalField = localFormSchema.value.fields[index]
  if (!originalField) return
  const field: Field = {
    id: `field_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
    type: originalField.type,
    label: originalField.label,
    required: originalField.required || false,
    options: originalField.options ? { ...originalField.options } : {}
  }
  updateSchema((schema) => {
    if (schema.fields) {
      schema.fields.splice(index + 1, 0, field)
    }
  })
  selectField(index + 1)
}

function removeField(index: number) {
  if (!localFormSchema.value.fields || index < 0 || index >= localFormSchema.value.fields.length) return
  updateSchema((schema) => {
    if (schema.fields) {
      schema.fields.splice(index, 1)
    }
  })
  if (props.selectedFieldIndex === index) {
    selectField(-1)
  } else if (props.selectedFieldIndex > index) {
    selectField(props.selectedFieldIndex - 1)
  }
}
</script>

<style scoped>
.form-canvas {
  height: 100%;
  overflow-y: auto;
}

.form-fields {
  min-height: 400px;
  border: 2px dashed rgba(var(--v-theme-primary), 0.3);
  border-radius: 12px;
  padding: 16px;
  transition: all 0.3s ease;
  background: rgba(var(--v-theme-surface), 0.5);
}

.form-fields:hover {
  border-color: rgba(var(--v-theme-primary), 0.5);
  background: rgba(var(--v-theme-surface-variant), 0.3);
}

.form-fields.drag-over {
  border-color: rgb(var(--v-theme-primary));
  border-width: 3px;
  background: rgba(var(--v-theme-primary), 0.08);
  box-shadow: inset 0 0 20px rgba(var(--v-theme-primary), 0.15);
}

.form-field {
  position: relative;
  margin-bottom: 16px;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid transparent;
  transition: all 0.2s ease;
  cursor: pointer;
}

.form-field:hover {
  background: rgba(var(--v-theme-surface-variant), 0.5);
  border-color: rgba(var(--v-theme-primary), 0.2);
}

.form-field.selected {
  background: rgba(var(--v-theme-primary), 0.08);
  border: 2px solid rgb(var(--v-theme-primary));
  box-shadow: 0 2px 8px rgba(var(--v-theme-primary), 0.2);
}

.field-menu {
  position: absolute;
  top: 8px;
  right: 8px;
  opacity: 0;
  transition: opacity 0.2s;
}

.form-field:hover .field-menu {
  opacity: 1;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: rgba(var(--v-theme-on-surface), 0.4);
  text-align: center;
}

.empty-state v-icon {
  color: rgba(var(--v-theme-primary), 0.3);
}

.empty-state p {
  margin-top: 16px;
  font-size: 1.1rem;
  font-weight: 500;
}

.title-editable {
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.title-editable:hover {
  background-color: rgba(var(--v-theme-on-surface), 0.08);
}

.title-edit-field {
  width: 100%;
}

.description-editable {
  min-height: 40px;
  padding: 8px;
}

.description-text {
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  display: block;
  transition: background-color 0.2s;
  color: rgba(var(--v-theme-on-surface), 0.7);
}

.description-text:hover {
  background-color: rgba(var(--v-theme-on-surface), 0.08);
}

.description-edit-field {
  width: 100%;
}
</style>
