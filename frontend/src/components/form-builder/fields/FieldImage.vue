<template>
  <div class="field-image">
    <v-img
      :src="field.options.src"
      :alt="field.options.alt"
      :width="field.options.width"
      :height="field.options.height"
      contain
    />
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'

interface FieldImageOptions {
  src?: string
  alt?: string
  width?: string | number
  height?: string | number
}

interface FieldImage {
  label?: string
  options: FieldImageOptions
}

// Props
const props = defineProps<{
  field: FieldImage
  isPreview?: boolean
}>()

// Computed reactive values (optional, can be used for dynamic updates)
const imageSrc = computed(() => props.field.options.src || '')
const imageAlt = computed(() => props.field.options.alt || 'Image')
const imageWidth = computed(() => props.field.options.width || '100%')
const imageHeight = computed(() => props.field.options.height || 'auto')
</script>

<style scoped>
.field-image {
  margin: 16px 0;
  text-align: center;
}
</style>
