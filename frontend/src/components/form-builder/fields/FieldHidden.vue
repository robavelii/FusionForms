<template>
  <div class="field-hidden">
    <v-alert type="info" variant="tonal">
      This is a hidden field and will not be visible to users.
    </v-alert>
    <v-text-field
      v-model="fieldValue"
      label="Hidden Value"
      @update:model-value="updateValue"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue'

interface FieldHiddenOption {
  value?: string
}

interface FieldHidden {
  label: string
  value?: string
  options: FieldHiddenOption
}

// Props
const props = defineProps<{
  field: FieldHidden
  isPreview?: boolean
}>()

// Emits
const emit = defineEmits<{
  (e: 'update', field: FieldHidden): void
}>()

// Local reactive value for the hidden field
const fieldValue = ref(props.field.options.value || '')

// Watch for external changes to keep in sync
watch(
  () => props.field.options.value,
  (newVal) => {
    fieldValue.value = newVal || ''
  }
)

// Emit updated value
const updateValue = (value: string) => {
  emit('update', {
    ...props.field,
    options: {
      ...props.field.options,
      value
    }
  })
}
</script>

<style scoped>
.field-hidden {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
</style>
