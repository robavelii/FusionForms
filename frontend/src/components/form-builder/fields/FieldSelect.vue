<template>
  <div class="field-select">
    <v-select
      v-model="selectedValue"
      :label="field.label"
      :items="field.options.options"
      item-title="label"
      item-value="value"
      :required="field.required"
      :hint="field.options.helpText"
      persistent-hint
      :multiple="field.options.multiple"
      :disabled="!isPreview"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue'

interface SelectOption {
  label: string
  value: string
}

interface FieldSelect {
  label: string
  value?: string | string[]
  required?: boolean
  options: {
    options: SelectOption[]
    multiple?: boolean
    helpText?: string
  }
}

// Props
const props = defineProps<{
  field: FieldSelect
  isPreview?: boolean
}>()

// Emits
const emit = defineEmits<{
  (e: 'update', field: FieldSelect): void
}>()

// Reactive selected value
const selectedValue = ref<string | string[]>(
  props.field.value || (props.field.options.multiple ? [] : '')
)

// Sync with prop value
watch(
  () => props.field.value,
  (newVal) => {
    selectedValue.value = newVal ?? (props.field.options.multiple ? [] : '')
  }
)

// Emit updates when selection changes
watch(selectedValue, (newVal) => {
  if (!props.isPreview) return
  emit('update', { ...props.field, value: newVal })
})
</script>

<style scoped>
.field-select {
  width: 100%;
  margin-bottom: 16px;
}
</style>
