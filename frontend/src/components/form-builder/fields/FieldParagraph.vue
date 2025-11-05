<template>
  <div class="field-paragraph">
    <p
      contenteditable="true"
      @input="onInput"
      v-html="paragraphText"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue'

interface FieldParagraphOption {
  text?: string
}

interface FieldParagraph {
  label: string
  options: FieldParagraphOption
}

// Props
const props = defineProps<{
  field: FieldParagraph
  isPreview?: boolean
}>()

// Emits
const emit = defineEmits<{
  (e: 'update', field: FieldParagraph): void
}>()

// Reactive paragraph text
const paragraphText = ref(props.field.options.text || '')

// Watch prop changes
watch(
  () => props.field.options.text,
  (newVal) => {
    paragraphText.value = newVal || ''
  }
)

// Handle input event
const onInput = (event: Event) => {
  if (!props.isPreview) {
    const target = event.target as HTMLElement
    paragraphText.value = target.innerText
    emit('update', {
      ...props.field,
      options: { ...props.field.options, text: paragraphText.value }
    })
  }
}
</script>

<style scoped>
.field-paragraph {
  margin: 16px 0;
}

.field-paragraph[contenteditable="true"]:focus {
  outline: none;
  background-color: #f5f5f5;
  padding: 4px;
  border-radius: 4px;
}
</style>
