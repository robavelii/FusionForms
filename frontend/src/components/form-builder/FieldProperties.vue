<template>
  <div class="field-properties">
    <v-card v-if="selectedField">
      <v-card-title class="text-h6">
        Field Properties
      </v-card-title>
      <v-card-text>
        <v-form>
          <!-- Label -->
          <v-text-field
            v-model="selectedField.label"
            label="Label"
            @update:model-value="updateField"
          />

          <!-- Placeholder -->
          <v-text-field
            v-if="hasPlaceholder"
            v-model="selectedField.options.placeholder"
            label="Placeholder"
            @update:model-value="updateField"
          />

          <!-- Default Value -->
          <v-text-field
            v-if="hasDefaultValue"
            v-model="selectedField.options.defaultValue"
            label="Default Value"
            @update:model-value="updateField"
          />

          <!-- Required -->
          <v-checkbox
            v-model="selectedField.required"
            label="Required"
            @update:model-value="updateField"
          />

          <!-- Help Text -->
          <v-text-field
            v-if="hasHelpText"
            v-model="selectedField.options.helpText"
            label="Help Text"
            @update:model-value="updateField"
          />

          <!-- Field-specific options -->
          <template v-if="selectedField.type === 'textarea'">
            <v-slider
              v-model="selectedField.options.rows"
              label="Rows"
              min="2"
              max="10"
              thumb-label
              @update:model-value="updateField"
            />
          </template>

          <template v-if="selectedField.type === 'number'">
            <v-text-field
              v-model="selectedField.options.min"
              label="Minimum Value"
              type="number"
              @update:model-value="updateField"
            />
            <v-text-field
              v-model="selectedField.options.max"
              label="Maximum Value"
              type="number"
              @update:model-value="updateField"
            />
          </template>

          <template v-if="['select','checkbox','radio'].includes(selectedField.type)">
            <v-checkbox
              v-if="selectedField.type === 'select'"
              v-model="selectedField.options.multiple"
              label="Allow Multiple Selection"
              @update:model-value="updateField"
            />

            <div class="options-list">
              <div class="options-header">
                <h3>Options</h3>
                <v-btn icon="mdi-plus" size="small" variant="text" @click="addOption" />
              </div>

              <div
                v-for="(option, index) in selectedField.options.options"
                :key="index"
                class="option-item"
              >
                <v-text-field
                  v-model="option.label"
                  label="Label"
                  @update:model-value="updateField"
                />
                <v-text-field
                  v-model="option.value"
                  label="Value"
                  @update:model-value="updateField"
                />
                <v-btn
                  icon="mdi-delete"
                  size="small"
                  variant="text"
                  color="error"
                  @click="removeOption(index)"
                />
              </div>
            </div>
          </template>

          <!-- File -->
          <template v-if="selectedField.type === 'file'">
            <v-text-field
              v-model="selectedField.options.accept"
              label="Accepted File Types"
              hint="e.g., image/*, .pdf, .doc"
              @update:model-value="updateField"
            />
            <v-checkbox
              v-model="selectedField.options.multiple"
              label="Allow Multiple Files"
              @update:model-value="updateField"
            />
          </template>

          <!-- Rating -->
          <template v-if="selectedField.type === 'rating'">
            <v-slider
              v-model="selectedField.options.max"
              label="Maximum Rating"
              min="3"
              max="10"
              thumb-label
              @update:model-value="updateField"
            />
          </template>

          <!-- Signature -->
          <template v-if="selectedField.type === 'signature'">
            <v-text-field
              v-model.number="selectedField.options.width"
              label="Width (px)"
              type="number"
              @update:model-value="updateField"
            />
            <v-text-field
              v-model.number="selectedField.options.height"
              label="Height (px)"
              type="number"
              @update:model-value="updateField"
            />
          </template>

          <!-- Hidden -->
          <template v-if="selectedField.type === 'hidden'">
            <v-text-field
              v-model="selectedField.options.value"
              label="Value"
              @update:model-value="updateField"
            />
          </template>

          <!-- Heading -->
          <template v-if="selectedField.type === 'heading'">
            <v-select
              v-model="selectedField.options.level"
              :items="[1,2,3,4,5,6]"
              label="Heading Level"
              @update:model-value="updateField"
            />
            <v-text-field
              v-model="selectedField.options.text"
              label="Text"
              @update:model-value="updateField"
            />
          </template>

          <!-- Paragraph -->
          <template v-if="selectedField.type === 'paragraph'">
            <v-textarea
              v-model="selectedField.options.text"
              label="Text"
              @update:model-value="updateField"
            />
          </template>

          <!-- Image -->
          <template v-if="selectedField.type === 'image'">
            <v-text-field
              v-model="selectedField.options.src"
              label="Image URL"
              @update:model-value="updateField"
            />
            <v-text-field
              v-model="selectedField.options.alt"
              label="Alt Text"
              @update:model-value="updateField"
            />
            <v-text-field
              v-model="selectedField.options.width"
              label="Width"
              @update:model-value="updateField"
            />
            <v-text-field
              v-model="selectedField.options.height"
              label="Height"
              @update:model-value="updateField"
            />
          </template>

          <!-- Validation Rules -->
          <v-divider class="my-4" />
          <h3>Validation Rules</h3>
          <v-checkbox
            v-if="['text','textarea'].includes(selectedField.type)"
            v-model="selectedField.validation.minLength"
            label="Minimum Length"
            @update:model-value="updateField"
          />
          <v-text-field
            v-if="selectedField.validation?.minLength"
            v-model.number="selectedField.validation.minLengthValue"
            label="Minimum Length Value"
            type="number"
            @update:model-value="updateField"
          />
          <v-checkbox
            v-if="['text','textarea'].includes(selectedField.type)"
            v-model="selectedField.validation.maxLength"
            label="Maximum Length"
            @update:model-value="updateField"
          />
          <v-text-field
            v-if="selectedField.validation?.maxLength"
            v-model.number="selectedField.validation.maxLengthValue"
            label="Maximum Length Value"
            type="number"
            @update:model-value="updateField"
          />
          <v-checkbox
            v-if="['text','textarea'].includes(selectedField.type)"
            v-model="selectedField.validation.pattern"
            label="Custom Pattern (Regex)"
            @update:model-value="updateField"
          />
          <v-text-field
            v-if="selectedField.validation?.pattern"
            v-model="selectedField.validation.patternValue"
            label="Pattern"
            @update:model-value="updateField"
          />

          <!-- Conditional Visibility -->
          <v-divider class="my-4" />
          <h3>Conditional Visibility</h3>
          <v-checkbox
            v-model="selectedField.conditionalVisibility.enabled"
            label="Enable Conditional Visibility"
            @update:model-value="updateField"
          />
          <template v-if="selectedField.conditionalVisibility.enabled">
            <v-select
              v-model="selectedField.conditionalVisibility.field"
              :items="availableFields"
              label="Show this field when"
              item-title="label"
              item-value="id"
              @update:model-value="updateField"
            />
            <v-select
              v-model="selectedField.conditionalVisibility.operator"
              :items="['equals','not_equals','contains','not_contains','is_empty','is_not_empty']"
              label="Operator"
              @update:model-value="updateField"
            />
            <v-text-field
              v-model="selectedField.conditionalVisibility.value"
              label="Value"
              @update:model-value="updateField"
            />
          </template>
        </v-form>
      </v-card-text>
    </v-card>

    <v-card v-else>
      <v-card-title class="text-h6">Field Properties</v-card-title>
      <v-card-text>
        <p class="text-center text-medium-emphasis">
          Select a field to edit its properties
        </p>
      </v-card-text>
    </v-card>
  </div>
</template>

<script lang="ts" setup>
import { computed, watch, reactive } from 'vue'

interface Option {
  label: string
  value: string
}

interface Validation {
  minLength?: boolean
  minLengthValue?: number
  maxLength?: boolean
  maxLengthValue?: number
  pattern?: boolean
  patternValue?: string
}

interface ConditionalVisibility {
  enabled: boolean
  field: string
  operator: string
  value: string
}

interface Field {
  id: string
  type: string
  label: string
  required?: boolean
  options: Record<string, any>
  validation?: Validation
  conditionalVisibility?: ConditionalVisibility
}

interface FormSchema {
  fields: Field[]
}

const props = defineProps<{
  selectedField: Field | null
  formSchema: FormSchema
}>()

const emit = defineEmits<{
  (e: 'update:selectedField', value: Field | null): void
  (e: 'update:formSchema', value: FormSchema): void
}>()

/* ----------------- COMPUTED ----------------- */
const hasPlaceholder = computed(() =>
  props.selectedField
    ? ['text','textarea','number','email','url','date','time'].includes(props.selectedField.type)
    : false
)

const hasDefaultValue = computed(() =>
  props.selectedField
    ? ['text','textarea','number','email','url','date','time','select','hidden'].includes(props.selectedField.type)
    : false
)

const hasHelpText = computed(() =>
  props.selectedField
    ? !['heading','paragraph','divider','image'].includes(props.selectedField.type)
    : false
)

const availableFields = computed(() => {
  if (!props.selectedField) return []
  return props.formSchema.fields.filter(f => f.id !== props.selectedField!.id)
})

/* ----------------- WATCH ----------------- */
watch(
  () => props.selectedField,
  (newField) => {
    if (!newField) return

    if (!newField.validation) newField.validation = reactive({})
    if (!newField.conditionalVisibility)
      newField.conditionalVisibility = reactive({
        enabled: false,
        field: '',
        operator: 'equals',
        value: ''
      })
  },
  { immediate: true }
)

/* ----------------- METHODS ----------------- */
function updateField() {
  emit('update:selectedField', props.selectedField)
  emit('update:formSchema', props.formSchema)
}

function addOption() {
  if (!props.selectedField?.options.options) props.selectedField.options.options = reactive([])
  const optionsArray = props.selectedField.options.options
  optionsArray.push({
    label: `Option ${optionsArray.length + 1}`,
    value: `option${optionsArray.length + 1}`
  })
  updateField()
}

function removeOption(index: number) {
  props.selectedField?.options.options.splice(index, 1)
  updateField()
}
</script>

<style scoped>
.field-properties {
  height: 100%;
  overflow-y: auto;
}

.options-list {
  margin-top: 16px;
}

.options-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.option-item {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-bottom: 8px;
}
</style>
