<template>
  <v-container fluid class="not-found">
    <v-row align="center" justify="center" style="min-height: 80vh;">
      <v-col cols="12" class="text-center">
        <v-icon size="150" color="grey-lighten-1">mdi-alert-circle-outline</v-icon>
        <h1 class="text-h2 font-weight-bold mt-6 mb-4">404</h1>
        <p class="text-h5 text-medium-emphasis mb-8">
          Oops! The page you're looking for doesn't exist.
        </p>
        <v-btn
          size="large"
          color="primary"
          prepend-icon="mdi-home"
          @click="goHome"
        >
          Back to Dashboard
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function goHome() {
  router.push('/dashboard')
}
</script>

<style scoped>
.not-found {
  background-color: #f5f5f5;
  min-height: 100vh;
}
</style>


