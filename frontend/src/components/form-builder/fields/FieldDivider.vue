<template>
  <div class="field-divider">
    <v-divider :class="dividerClass" />
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'

interface FieldDividerOptions {
  style?: string
}

interface FieldDivider {
  label?: string
  options: FieldDividerOptions
}

// Props
const props = defineProps<{
  field: FieldDivider
  isPreview?: boolean
}>()

// Computed class based on style option
const dividerClass = computed(() => props.field.options.style || '')
</script>

<style scoped>
.field-divider {
  margin: 16px 0;
}
</style>
