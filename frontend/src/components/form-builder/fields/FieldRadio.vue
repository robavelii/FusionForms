<template>
  <div class="field-radio">
    <!-- Preview mode: interactive radio buttons -->
    <div v-if="isPreview">
      <v-radio-group
        :label="field.label"
        :required="field.required"
        v-model="selectedValue"
      >
        <v-radio
          v-for="option in field.options.options"
          :key="option.value"
          :label="option.label"
          :value="option.value"
        />
      </v-radio-group>
    </div>

    <!-- Builder mode: disabled radio buttons -->
    <div v-else>
      <p>{{ field.label }}</p>
      <v-radio-group v-model="selectedValue">
        <v-radio
          v-for="option in field.options.options"
          :key="option.value"
          :label="option.label"
          :value="option.value"
          disabled
        />
      </v-radio-group>
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

interface RadioOption {
  label: string
  value: string
}

interface FieldRadio {
  label: string
  value?: string
  required?: boolean
  options: {
    options: RadioOption[]
    helpText?: string
  }
}

// Props
const props = defineProps<{
  field: FieldRadio
  isPreview?: boolean
}>()

// Emits
const emit = defineEmits<{
  (e: 'update', field: FieldRadio): void
}>()

// Reactive selected value
const selectedValue = ref<string>(props.field.value || '')

// Sync with prop value
watch(
  () => props.field.value,
  (newVal) => {
    selectedValue.value = newVal || ''
  }
)

// Emit updates when selection changes
watch(selectedValue, (newVal) => {
  if (!props.isPreview) return
  emit('update', { ...props.field, value: newVal })
})
</script>

<style scoped>
.field-radio {
  width: 100%;
  margin-bottom: 16px;
}
</style>
