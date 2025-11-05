<template>
  <div class="field-file">
    <v-file-input
      v-model="selectedFiles"
      :label="field.label"
      :accept="field.options.accept"
      :multiple="field.options.multiple"
      :required="field.required"
      :hint="field.options.helpText"
      persistent-hint
      :disabled="!isPreview"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue'

interface FieldFileOption {
  accept?: string
  multiple?: boolean
  helpText?: string
}

interface FieldFile {
  label: string
  value?: File | File[] | null
  required?: boolean
  options: FieldFileOption
}

// Props
const props = defineProps<{
  field: FieldFile
  isPreview?: boolean
}>()

// Emits
const emit = defineEmits<{
  (e: 'update', field: FieldFile): void
}>()

// Reactive selected files
const selectedFiles = ref<File | File[] | null>(
  props.field.value ?? (props.field.options.multiple ? [] : null)
)

// Watch for prop changes
watch(
  () => props.field.value,
  (newVal) => {
    selectedFiles.value = newVal ?? (props.field.options.multiple ? [] : null)
  }
)

// Emit updates when selection changes
watch(selectedFiles, (newVal) => {
  if (!props.isPreview) return
  emit('update', { ...props.field, value: newVal })
})
</script>

<style scoped>
.field-file {
  width: 100%;
  margin-bottom: 16px;
}
</style>
