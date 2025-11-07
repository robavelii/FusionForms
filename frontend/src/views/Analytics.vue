<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 font-weight-bold mb-4">Analytics Dashboard</h1>
        <p class="text-subtitle-1 text-medium-emphasis mb-6">
          View insights and statistics across all your forms
        </p>
      </v-col>
    </v-row>

    <!-- Stats Cards -->
    <v-row>
      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon size="40" color="primary" class="mr-4">mdi-file-document-multiple</v-icon>
              <div>
                <div class="text-h5 font-weight-bold">{{ totalForms }}</div>
                <div class="text-caption text-medium-emphasis">Total Forms</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon size="40" color="success" class="mr-4">mdi-check-circle</v-icon>
              <div>
                <div class="text-h5 font-weight-bold">{{ totalSubmissions }}</div>
                <div class="text-caption text-medium-emphasis">Total Submissions</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon size="40" color="info" class="mr-4">mdi-eye</v-icon>
              <div>
                <div class="text-h5 font-weight-bold">{{ totalViews }}</div>
                <div class="text-caption text-medium-emphasis">Total Views</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon size="40" color="warning" class="mr-4">mdi-chart-line</v-icon>
              <div>
                <div class="text-h5 font-weight-bold">{{ completionRate }}%</div>
                <div class="text-caption text-medium-emphasis">Completion Rate</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Forms List -->
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>Your Forms</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item
                v-for="form in forms"
                :key="form.id"
                :title="form.title"
                :subtitle="`${form.submission_count || 0} submissions`"
                @click="router.push(`/forms/${form.id}/analytics`)"
              >
                <template #prepend>
                  <v-icon>mdi-file-document</v-icon>
                </template>
                <template #append>
                  <v-btn
                    icon="mdi-chevron-right"
                    variant="text"
                    size="small"
                  />
                </template>
              </v-list-item>
              <v-list-item v-if="forms.length === 0">
                <v-list-item-title>No forms yet</v-list-item-title>
                <v-list-item-subtitle>Create your first form to see analytics</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useFormsStore } from '@/stores/forms'

const router = useRouter()
const formsStore = useFormsStore()

const forms = computed(() => formsStore.forms)

const totalForms = computed(() => forms.value.length)
const totalSubmissions = computed(() => {
  return forms.value.reduce((sum, form) => sum + (form.submission_count || 0), 0)
})
const totalViews = computed(() => {
  return forms.value.reduce((sum, form) => sum + (form.view_count || 0), 0)
})
const completionRate = computed(() => {
  if (totalViews.value === 0) return 0
  return Math.round((totalSubmissions.value / totalViews.value) * 100)
})

onMounted(() => {
  formsStore.fetchForms()
})
</script>

<style scoped>
</style>

