<template>
  <div class="field-select">
    <v-select
      v-model="selectedValue"
      :label="field.label"
      :items="field.options?.options || []"
      item-title="label"
      item-value="value"
      :required="field.required"
      :rules="validationRules"
      :hint="field.options?.helpText"
      :persistent-hint="!!field.options?.helpText"
      :multiple="field.options?.multiple"
      :disabled="!isPreview"
      variant="outlined"
      @update:model-value="handleUpdate"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref, watch, computed } from 'vue'

interface SelectOption {
  label: string
  value: string
}

interface FieldSelect {
  id?: string
  label: string
  value?: string | string[]
  required?: boolean
  options?: {
    options?: SelectOption[]
    multiple?: boolean
    helpText?: string
    [key: string]: any
  }
}

const props = withDefaults(defineProps<{
  field: FieldSelect
  isPreview?: boolean
  modelValue?: string | string[]
}>(), {
  isPreview: false
})

const emit = defineEmits<{
  (e: 'update', field: FieldSelect): void
  (e: 'update:modelValue', value: string | string[]): void
}>()

const selectedValue = ref<string | string[]>(
  props.modelValue || props.field.value || (props.field.options?.multiple ? [] : '')
)

const validationRules = computed(() => {
  const rules: any[] = []
  
  if (props.field.required) {
    rules.push((v: any) => {
      if (Array.isArray(v)) {
        return v.length > 0 || 'Please select at least one option'
      }
      return !!v || 'This field is required'
    })
  }
  
  return rules
})

watch(
  () => props.modelValue,
  (newVal) => {
    if (JSON.stringify(newVal) !== JSON.stringify(selectedValue.value)) {
      selectedValue.value = newVal ?? (props.field.options?.multiple ? [] : '')
    }
  }
)

watch(
  () => props.field.value,
  (newVal) => {
    if (JSON.stringify(newVal) !== JSON.stringify(selectedValue.value)) {
      selectedValue.value = newVal ?? (props.field.options?.multiple ? [] : '')
    }
  }
)

function handleUpdate(value: string | string[]) {
  emit('update:modelValue', value)
  if (!props.isPreview) {
    emit('update', { ...props.field, value })
  }
}
</script>

<style scoped>
.field-select {
  width: 100%;
  margin-bottom: 16px;
}
</style>
