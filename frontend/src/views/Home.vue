<template>
  <v-container fluid class="home-view">
    <v-row>
      <v-col cols="12">
        <div class="text-center py-16">
          <v-icon size="120" color="primary" class="mb-6">mdi-form-select</v-icon>
          <h1 class="text-h2 font-weight-bold mb-4">
            Welcome to FusionForms
          </h1>
          <p class="text-h5 text-medium-emphasis mb-8">
            Intelligent Dynamic Form Builder & Data Insights Platform
          </p>
          <div class="d-flex justify-center gap-4">
            <v-btn
              size="x-large"
              color="primary"
              prepend-icon="mdi-plus"
              @click="goToDashboard"
            >
              Get Started
            </v-btn>
            <v-btn
              size="x-large"
              variant="outlined"
              prepend-icon="mdi-information"
              @click="learnMore"
            >
              Learn More
            </v-btn>
          </div>
        </div>
      </v-col>
    </v-row>

    <v-row class="mt-16">
      <v-col
        v-for="feature in features"
        :key="feature.title"
        cols="12"
        md="4"
      >
        <v-card class="feature-card" elevation="2">
          <v-card-text class="text-center">
            <v-icon size="64" :color="feature.color" class="mb-4">
              {{ feature.icon }}
            </v-icon>
            <h3 class="text-h5 font-weight-bold mb-3">{{ feature.title }}</h3>
            <p class="text-body-1">{{ feature.description }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const features = [
  {
    title: 'Drag & Drop Builder',
    description: 'Create beautiful forms with our intuitive drag-and-drop interface. No coding required.',
    icon: 'mdi-drag',
    color: 'primary'
  },
  {
    title: 'Real-time Analytics',
    description: 'Track submissions, conversion rates, and user behavior with powerful analytics dashboards.',
    icon: 'mdi-chart-line',
    color: 'success'
  },
  {
    title: 'Advanced Features',
    description: 'Conditional logic, webhooks, custom validation, and seamless integrations with your tools.',
    icon: 'mdi-cog',
    color: 'warning'
  }
]

function goToDashboard() {
  router.push('/dashboard')
}

function learnMore() {
  // Could navigate to a documentation page or open a modal
  console.log('Learn more clicked')
}
</script>

<style scoped>
.home-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.feature-card {
  height: 100%;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-8px);
}
</style>

