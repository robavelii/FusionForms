<template>
  <div class="form-detail">
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-title class="d-flex align-center">
              <span>{{ form?.title }}</span>
              <v-spacer />
              <v-btn color="primary" prepend-icon="mdi-pencil" @click="editForm">
                Edit
              </v-btn>
            </v-card-title>
            <v-card-subtitle v-if="form?.description">
              {{ form.description }}
            </v-card-subtitle>
            <v-card-text>
              <v-tabs v-model="tab">
                <v-tab value="overview">Overview</v-tab>
                <v-tab value="submissions">Submissions</v-tab>
                <v-tab value="analytics">Analytics</v-tab>
                <v-tab value="settings">Settings</v-tab>
              </v-tabs>

              <v-window v-model="tab">
                <v-window-item value="overview">
                  <FormOverview :form="form" />
                </v-window-item>

                <v-window-item value="submissions">
                  <FormSubmissions :form-id="form?.id" />
                </v-window-item>

                <v-window-item value="analytics">
                  <FormAnalytics :form-id="form?.id" />
                </v-window-item>

                <v-window-item value="settings">
                  <FormSettings :form="form" />
                </v-window-item>
              </v-window>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useFormsStore } from '@/stores/forms'
import type { Form } from '@/types/formTypes'

import FormOverview from '@/components/forms/FormOverview.vue'
import FormSubmissions from '@/components/forms/FormSubmissions.vue'
import FormAnalytics from '@/components/forms/FormAnalytics.vue'
import FormSettings from '@/components/forms/FormSettings.vue'

// Router and route
const router = useRouter()
const route = useRoute()

// Pinia store
const formsStore = useFormsStore()

// Reactive state
const tab = ref<string>('overview')

// Computed form
const form = computed<Form | null>(() => formsStore.currentForm)

// Lifecycle
onMounted(async () => {
  const id = route.params.id as string
  if (id) {
    await formsStore.fetchForm(id)
  }
})

// Methods
function editForm() {
  if (form.value?.id) {
    router.push(`/forms/${form.value.id}/edit`)
  }
}
</script>

<style scoped>
.form-detail {
  padding: 16px;
}
</style>
