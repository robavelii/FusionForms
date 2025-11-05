<template>
  <div>
    <p><strong>Title:</strong> {{ form?.title }}</p>
    <p><strong>Description:</strong> {{ form?.description }}</p>
    <p><strong>Status:</strong> {{ form?.status }}</p>
    <p><strong>Fields:</strong> {{ form?.fields.length }}</p>
  </div>
</template>

<script lang="ts" setup>
import type { Form } from '@/types/formTypes'
import { defineProps } from 'vue'

const props = defineProps<{ form: Form | null }>()
</script>
