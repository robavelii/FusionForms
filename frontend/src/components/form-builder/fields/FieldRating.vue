<template>
  <div class="field-rating">
    <p>{{ field.label }}</p>
    <v-rating
      v-model="ratingValue"
      :length="field.options.max || 5"
      :hover="true"
      :readonly="!isPreview"
    />

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

interface FieldRatingOption {
  max?: number
  helpText?: string
}

interface FieldRating {
  label: string
  value?: number
  required?: boolean
  options: FieldRatingOption
}

// Props
const props = defineProps<{
  field: FieldRating
  isPreview?: boolean
}>()

// Emits
const emit = defineEmits<{
  (e: 'update', field: FieldRating): void
}>()

// Reactive rating value
const ratingValue = ref<number>(props.field.value ?? 0)

// Watch prop changes
watch(
  () => props.field.value,
  (newVal) => {
    ratingValue.value = newVal ?? 0
  }
)

// Emit updates on change
watch(ratingValue, (newVal) => {
  if (!props.isPreview) return
  emit('update', { ...props.field, value: newVal })
})
</script>

<style scoped>
.field-rating {
  width: 100%;
  margin-bottom: 16px;
}
</style>
