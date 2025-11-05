<template>
  <div class="field-time">
    <v-text-field
      v-model="inputValue"
      :label="isPreview ? field.label : ''"
      :placeholder="field.options.placeholder"
      :required="field.required"
      :hint="field.options.helpText"
      persistent-hint
      type="time"
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

// Keep internal inputValue in sync with parent field value
watch(
  () => props.field.value,
  (newVal) => {
    inputValue.value = newVal || ''
  }
)

// Emit update event whenever value changes
watch(inputValue, (value) => {
  if (!props.isPreview) {
    emit('update', { ...props.field, value })
  }
})
</script>

<style scoped>
.field-time {
  width: 100%;
}
</style>
