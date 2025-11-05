<template>
  <div class="field-url">
    <v-text-field
      v-model="inputValue"
      :label="isPreview ? field.label : ''"
      :placeholder="field.options.placeholder"
      :required="field.required"
      :hint="field.options.helpText"
      persistent-hint
      type="url"
      :disabled="isPreview"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue'

interface Field {
  label: string
  value?: string
  required?: boolean
  options: {
    placeholder?: string
    helpText?: string
    [key: string]: any
  }
}

const props = defineProps<{
  field: Field
  isPreview?: boolean
}>()

const emit = defineEmits<{
  (e: 'update', value: Field): void
}>()

const inputValue = ref<string>(props.field.value || '')

// Keep internal inputValue in sync with external field value
watch(
  () => props.field.value,
  (newVal) => {
    inputValue.value = newVal || ''
  }
)

// Emit update event whenever the value changes
watch(inputValue, (value) => {
  if (!props.isPreview) {
    emit('update', { ...props.field, value })
  }
})
</script>

<style scoped>
.field-url {
  width: 100%;
}
</style>
