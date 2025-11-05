<template>
  <div class="field-richtext">
    <div v-if="isPreview">
      <p>{{ field.label }}</p>
      <v-card>
        <v-card-text>
          <div
            contenteditable="true"
            class="richtext-editor"
            @input="onInput"
            v-html="fieldValue"
          />
        </v-card-text>
      </v-card>
    </div>
    <div v-else>
      <p>{{ field.label }}</p>
      <v-card>
        <v-card-text>
          <div class="richtext-preview" v-html="fieldValue" />
        </v-card-text>
      </v-card>
    </div>
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

interface FieldRichtextOption {
  placeholder?: string
  helpText?: string
}

interface FieldRichtext {
  label: string
  value?: string
  options: FieldRichtextOption
}

// Props
const props = defineProps<{
  field: FieldRichtext
  isPreview?: boolean
}>()

// Emits
const emit = defineEmits<{
  (e: 'update', field: FieldRichtext): void
}>()

// Local reactive value
const fieldValue = ref(props.field.value || props.field.options.placeholder || '')

// Sync with prop changes
watch(
  () => props.field.value,
  (newVal) => {
    fieldValue.value = newVal || props.field.options.placeholder || ''
  }
)

// Handle input in contenteditable
const onInput = (event: Event) => {
  if (!props.isPreview) {
    const target = event.target as HTMLElement
    fieldValue.value = target.innerHTML
    emit('update', { ...props.field, value: fieldValue.value })
  }
}
</script>

<style scoped>
.richtext-editor,
.richtext-preview {
  min-height: 100px;
  padding: 8px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
}

.richtext-editor:focus {
  outline: none;
  border-color: #1976d2;
}
</style>
