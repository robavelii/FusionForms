<template>
  <v-snackbar
    v-model="show"
    :color="color"
    :timeout="timeout"
    location="top right"
    :multi-line="message.length > 50"
  >
    {{ message }}
    <template #actions>
      <v-btn
        variant="text"
        @click="show = false"
      >
        Close
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useSnackbarStore } from '@/stores/snackbar'

const snackbarStore = useSnackbarStore()
const { message, color, timeout, visible } = storeToRefs(snackbarStore)

const show = ref(false)

watch(visible, (newVal) => {
  show.value = newVal
})

watch(show, (newVal) => {
  if (!newVal) {
    snackbarStore.hide()
  }
})
</script>

