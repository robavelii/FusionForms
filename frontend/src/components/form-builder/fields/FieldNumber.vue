<template>
  <div class="field-number">
    <v-text-field
      v-model.number="inputValue"
      :label="isPreview ? field.label : ''"
      :placeholder="field.options.placeholder"
      :required="field.required"
      :hint="field.options.helpText"
      persistent-hint
      type="number"
      :min="field.options.min"
      :max="field.options.max"
      :disabled="isPreview"
      @update:model-value="updateValue"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue'

interface Field {
  label: string
  value?: number
  required?: boolean
  options: {
    placeholder?: string
    helpText?: string
    min?: number
    max?: number
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

const inputValue = ref<number>(props.field.value || 0)

watch(
  () => props.field.value,
  (newVal) => {
    inputValue.value = newVal ?? 0
  }
)

function updateValue(value: number) {
  if (!props.isPreview) {
    emit('update', { ...props.field, value })
  }
}
</script>

<style scoped>
.field-number {
  width: 100%;
}
</style>
