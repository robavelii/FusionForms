<template>
  <div class="field-checkbox">
    <!-- Preview mode: interactive checkboxes -->
    <div v-if="isPreview">
      <v-checkbox
        v-for="option in field.options.options"
        :key="option.value"
        :label="option.label"
        :value="option.value"
        v-model="selectedValues"
        :required="field.required"
      />
    </div>

    <!-- Builder mode: show label and disabled checkboxes -->
    <div v-else>
      <p>{{ field.label }}</p>
      <v-checkbox
        v-for="option in field.options.options"
        :key="option.value"
        :label="option.label"
        :value="option.value"
        v-model="selectedValues"
        disabled
      />
    </div>

    <!-- Help text -->
    <v-textarea
      v-if="field.options.helpText"
      :model-value="field.options.helpText"
      label="Help Text"
      readonly
      class="mt-2"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue'

interface CheckboxOption {
  label: string
  value: string
}

interface FieldCheckbox {
  label: string
  value?: string[] | string
  required?: boolean
  options: {
    options: CheckboxOption[]
    helpText?: string
  }
}

// Props
const props = defineProps<{
  field: FieldCheckbox
  isPreview?: boolean
}>()

// Emits
const emit = defineEmits<{
  (e: 'update', field: FieldCheckbox): void
}>()

// Reactive value for selected options
const selectedValues = ref<string[]>(Array.isArray(props.field.value) ? props.field.value : [])

// Sync with parent field value
watch(
  () => props.field.value,
  (newVal) => {
    selectedValues.value = Array.isArray(newVal) ? newVal : []
  }
)

// Emit updates when selection changes
watch(selectedValues, (newVal) => {
  if (!props.isPreview) return
  emit('update', { ...props.field, value: newVal })
})
</script>

<style scoped>
.field-checkbox {
  width: 100%;
  margin-bottom: 16px;
}
</style>
