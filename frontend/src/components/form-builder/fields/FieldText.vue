<template>
  <div class="field-text">
    <v-text-field
      v-model="inputValue"
      :label="field.label"
      :placeholder="field.options?.placeholder"
      :required="field.required"
      :rules="validationRules"
      :hint="field.options?.helpText"
      :persistent-hint="!!field.options?.helpText"
      :disabled="!isPreview"
      variant="outlined"
      @update:model-value="handleUpdate"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref, watch, computed } from 'vue'

interface Field {
  id?: string
  label: string
  value?: string
  required?: boolean
  options?: {
    placeholder?: string
    helpText?: string
    [key: string]: any
  }
  validation?: {
    minLength?: boolean
    minLengthValue?: number
    maxLength?: boolean
    maxLengthValue?: number
    pattern?: boolean
    patternValue?: string
  }
}

const props = withDefaults(defineProps<{
  field: Field
  isPreview?: boolean
  modelValue?: string
}>(), {
  isPreview: false
})

const emit = defineEmits<{
  (e: 'update', value: Field): void
  (e: 'update:modelValue', value: string): void
}>()

const inputValue = ref(props.modelValue || props.field.value || '')

// Validation rules
const validationRules = computed(() => {
  const rules: any[] = []
  
  if (props.field.required) {
    rules.push((v: string) => !!v || 'This field is required')
  }
  
  if (props.field.validation?.minLength && props.field.validation?.minLengthValue) {
    rules.push((v: string) => 
      !v || v.length >= props.field.validation!.minLengthValue! || 
      `Minimum ${props.field.validation!.minLengthValue} characters required`
    )
  }
  
  if (props.field.validation?.maxLength && props.field.validation?.maxLengthValue) {
    rules.push((v: string) => 
      !v || v.length <= props.field.validation!.maxLengthValue! || 
      `Maximum ${props.field.validation!.maxLengthValue} characters allowed`
    )
  }
  
  if (props.field.validation?.pattern && props.field.validation?.patternValue) {
    rules.push((v: string) => {
      if (!v) return true
      const regex = new RegExp(props.field.validation!.patternValue!)
      return regex.test(v) || 'Invalid format'
    })
  }
  
  return rules
})

watch(
  () => props.modelValue,
  (newVal) => {
    if (newVal !== inputValue.value) {
      inputValue.value = newVal || ''
    }
  }
)

watch(
  () => props.field.value,
  (newVal) => {
    if (newVal !== inputValue.value) {
      inputValue.value = newVal || ''
    }
  }
)

function handleUpdate(value: string) {
  emit('update:modelValue', value)
  if (!props.isPreview) {
    emit('update', { ...props.field, value })
  }
}
</script>

<style scoped>
.field-text {
  width: 100%;
}
</style>
