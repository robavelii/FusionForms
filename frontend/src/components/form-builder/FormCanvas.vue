<template>
  <div class="form-canvas">
    <v-card>
      <v-card-title class="text-h6">
        {{ formSchema?.title || 'Untitled Form' }}
      </v-card-title>
      <v-card-subtitle v-if="formSchema?.description">
        {{ formSchema.description }}
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
            v-model="formSchema.fields"
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
import { reactive, ref } from 'vue'
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

/* ----------------- TYPES ----------------- */
interface Field {
  id: string
  type: string
  label: string
  required?: boolean
  options?: any
}

interface FormSchema {
  title: string
  description?: string
  fields: Field[]
}

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
    
    if (!props.formSchema) {
      console.error('No formSchema available')
      return
    }
    
    const fieldDataStr = event.dataTransfer.getData('application/json')
    if (!fieldDataStr) {
      console.error('No data in drop event')
      return
    }
    
    const fieldData = JSON.parse(fieldDataStr)
    console.log('Dropping field:', fieldData)
    
    const newField: Field = reactive({
      id: `field_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      type: fieldData.type,
      label: fieldData.label,
      required: false,
      options: getDefaultOptions(fieldData.type)
    })
    
    // Ensure fields array exists
    if (!props.formSchema.fields) {
      props.formSchema.fields = []
    }
    
    props.formSchema.fields.push(newField)
    emit('update:formSchema', props.formSchema)
    selectField(props.formSchema.fields.length - 1)
    
    console.log('Field added successfully', newField)
  } catch (error) {
    console.error('Error in onDrop:', error)
  }
}

function onFieldChange() {
  if (props.formSchema) {
    emit('update:formSchema', props.formSchema)
  }
}

function selectField(index: number) {
  emit('selectField', index)
}

function updateField(index: number, field: Field) {
  if (props.formSchema) {
    props.formSchema.fields.splice(index, 1, field)
    emit('update:formSchema', props.formSchema)
  }
}

function duplicateField(index: number) {
  if (!props.formSchema) return
  const field = { ...props.formSchema.fields[index] }
  field.id = `field_${Date.now()}`
  props.formSchema.fields.splice(index + 1, 0, field)
  emit('update:formSchema', props.formSchema)
  selectField(index + 1)
}

function removeField(index: number) {
  if (!props.formSchema) return
  props.formSchema.fields.splice(index, 1)
  emit('update:formSchema', props.formSchema)
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
</style>
