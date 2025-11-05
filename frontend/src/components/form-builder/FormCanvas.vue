<template>
  <div class="form-canvas">
    <v-card>
      <v-card-title class="text-h6">
        {{ formSchema.title || 'Untitled Form' }}
      </v-card-title>
      <v-card-subtitle v-if="formSchema.description">
        {{ formSchema.description }}
      </v-card-subtitle>
      <v-card-text>
        <div
          class="form-fields"
          @drop="onDrop"
          @dragover.prevent
          @dragenter.prevent
        >
          <draggable
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

          <div v-if="formSchema.fields.length === 0" class="empty-state">
            <v-icon size="48">mdi-drag</v-icon>
            <p>Drag fields here to start building your form</p>
          </div>
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'
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
  formSchema: FormSchema
  selectedFieldIndex: number
}>()

const emit = defineEmits<{
  (e: 'update:formSchema', value: FormSchema): void
  (e: 'selectField', index: number): void
}>()

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

function onDrop(event: DragEvent) {
  try {
    if (!event.dataTransfer) return
    const fieldData = JSON.parse(event.dataTransfer.getData('application/json'))
    const newField: Field = reactive({
      id: `field_${Date.now()}`,
      type: fieldData.type,
      label: fieldData.label,
      required: false,
      options: getDefaultOptions(fieldData.type)
    })
    props.formSchema.fields.push(newField)
    emit('update:formSchema', props.formSchema)
    selectField(props.formSchema.fields.length - 1)
  } catch (error) {
    console.error('Error parsing field data:', error)
  }
}

function onFieldChange() {
  emit('update:formSchema', props.formSchema)
}

function selectField(index: number) {
  emit('selectField', index)
}

function updateField(index: number, field: Field) {
  props.formSchema.fields.splice(index, 1, field)
  emit('update:formSchema', props.formSchema)
}

function duplicateField(index: number) {
  const field = { ...props.formSchema.fields[index] }
  field.id = `field_${Date.now()}`
  props.formSchema.fields.splice(index + 1, 0, field)
  emit('update:formSchema', props.formSchema)
  selectField(index + 1)
}

function removeField(index: number) {
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
  border: 2px dashed #e0e0e0;
  border-radius: 4px;
  padding: 16px;
  transition: border-color 0.2s;
}

.form-fields:hover {
  border-color: #bdbdbd;
}

.form-field {
  position: relative;
  margin-bottom: 16px;
  padding: 8px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.form-field:hover {
  background-color: #f5f5f5;
}

.form-field.selected {
  background-color: #e3f2fd;
  border: 1px solid #2196f3;
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
  color: #9e9e9e;
  text-align: center;
}

.empty-state p {
  margin-top: 16px;
}
</style>
