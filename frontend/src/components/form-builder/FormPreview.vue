<template>
  <div class="form-preview">
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card>
            <v-card-title class="text-h5">
              {{ formSchema.title || 'Untitled Form' }}
            </v-card-title>
            <v-card-subtitle v-if="formSchema.description">
              {{ formSchema.description }}
            </v-card-subtitle>
            <v-card-text>
              <v-form ref="form" v-model="valid">
                <div
                  v-for="(field, index) in formSchema.fields"
                  :key="field.id || index"
                  class="form-field"
                >
                  <component
                    :is="getFieldComponent(field.type)"
                    :field="field"
                    :is-preview="true"
                    @update="updateFieldValue(index, $event)"
                  />
                </div>

                <v-btn color="primary" :disabled="!valid" @click="submitForm">
                  {{ formSchema.settings?.submitButtonText || 'Submit' }}
                </v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Success Dialog -->
    <v-dialog v-model="showSuccess" max-width="500">
      <v-card>
        <v-card-title class="text-h5">Success!</v-card-title>
        <v-card-text>
          {{ formSchema.settings?.successMessage || 'Thank you for your submission!' }}
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="primary" @click="showSuccess = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, reactive, computed } from 'vue'
import type { FormSchema, FormField } from '@/types/formTypes'

// Props
interface Props {
  formSchema?: FormSchema | null
}
const props = defineProps<Props>()

// Default schema for safety
const defaultSchema: FormSchema = {
  title: '',
  description: '',
  fields: [],
  settings: {
    submitButtonText: 'Submit',
    successMessage: 'Thank you for your submission!'
  }
}

// Computed schema that always returns a valid schema
const formSchema = computed(() => {
  return props.formSchema || defaultSchema
})

// Refs
const form = ref()
const valid = ref(false)
const showSuccess = ref(false)
const formData = reactive<Record<string, any>>({})

// Initialize formData with default values
onMounted(() => {
  const schema = formSchema.value
  if (schema && schema.fields) {
    schema.fields.forEach((field) => {
      if (field.options?.defaultValue !== undefined) {
        formData[field.id || ''] = field.options.defaultValue
      } else {
        formData[field.id || ''] = null
      }
    })
  }
})

// Methods
function getFieldComponent(type: string) {
  const componentMap: Record<string, string> = {
    text: 'FieldText',
    textarea: 'FieldTextarea',
    number: 'FieldNumber',
    email: 'FieldEmail',
    url: 'FieldUrl',
    date: 'FieldDate',
    time: 'FieldTime',
    checkbox: 'FieldCheckbox',
    radio: 'FieldRadio',
    select: 'FieldSelect',
    file: 'FieldFile',
    rating: 'FieldRating',
    signature: 'FieldSignature',
    hidden: 'FieldHidden',
    richtext: 'FieldRichtext',
    heading: 'FieldHeading',
    paragraph: 'FieldParagraph',
    divider: 'FieldDivider',
    image: 'FieldImage'
  }
  return componentMap[type] || 'FieldText'
}

function updateFieldValue(index: number, field: FormField) {
  formData[field.id] = field.value
}

function submitForm() {
  console.log('Form submitted:', formData)
  showSuccess.value = true
}
</script>

<style scoped>
.form-preview {
  padding: 24px;
}

.form-field {
  margin-bottom: 16px;
}
</style>
