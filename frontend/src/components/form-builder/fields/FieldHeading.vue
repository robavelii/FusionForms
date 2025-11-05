<template>
  <div class="field-heading">
    <component
      :is="`h${headingLevel}`"
      contenteditable="true"
      @input="onInput"
      v-html="headingText"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref, watch, computed } from 'vue'

interface FieldHeadingOption {
  level?: number
  text?: string
}

interface FieldHeading {
  label: string
  options: FieldHeadingOption
}

// Props
const props = defineProps<{
  field: FieldHeading
  isPreview?: boolean
}>()

// Emits
const emit = defineEmits<{
  (e: 'update', field: FieldHeading): void
}>()

// Reactive heading text
const headingText = ref(props.field.options.text || '')

// Compute heading level with default 2
const headingLevel = computed(() => props.field.options.level || 2)

// Sync with prop changes
watch(
  () => props.field.options.text,
  (newVal) => {
    headingText.value = newVal || ''
  }
)

// Handle contenteditable input
const onInput = (event: Event) => {
  if (!props.isPreview) {
    const target = event.target as HTMLElement
    headingText.value = target.innerText
    emit('update', {
      ...props.field,
      options: { ...props.field.options, text: headingText.value }
    })
  }
}
</script>

<style scoped>
.field-heading {
  margin: 16px 0;
}

.field-heading[contenteditable="true"]:focus {
  outline: none;
  background-color: #f5f5f5;
  padding: 4px;
  border-radius: 4px;
}
</style>
