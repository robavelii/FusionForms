<template>
  <div class="field-textarea">
    <v-textarea
      v-model="inputValue"
      :label="isPreview ? field.label : ''"
      :placeholder="field.options.placeholder"
      :required="field.required"
      :hint="field.options.helpText"
      persistent-hint
      :rows="field.options.rows || 3"
      :disabled="isPreview"
      @update:model-value="updateValue"
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
    rows?: number
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

const inputValue = ref(props.field.value || '')

watch(
  () => props.field.value,
  (newVal) => {
    inputValue.value = newVal || ''
  }
)

function updateValue(value: string) {
  if (!props.isPreview) {
    emit('update', { ...props.field, value })
  }
}
</script>

<style scoped>
.field-textarea {
  width: 100%;
}
</style>
