<template>
  <v-container fluid class="dashboard">
    <v-row>
      <v-col cols="12">
        <h1 class="text-h3 font-weight-bold mb-2">Dashboard</h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Welcome back, {{ currentUser?.username }}!
        </p>
      </v-col>
    </v-row>

    <!-- Stats Cards -->
    <v-row class="mt-4">
      <v-col
        v-for="stat in stats"
        :key="stat.title"
        cols="12"
        sm="6"
        md="3"
      >
        <v-card>
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <p class="text-subtitle-2 text-medium-emphasis mb-1">
                  {{ stat.title }}
                </p>
                <h2 class="text-h4 font-weight-bold">
                  {{ stat.value }}
                </h2>
                <p
                  v-if="stat.change"
                  :class="stat.change >= 0 ? 'text-success' : 'text-error'"
                  class="text-caption mt-1"
                >
                  <v-icon size="14">
                    {{ stat.change >= 0 ? 'mdi-arrow-up' : 'mdi-arrow-down' }}
                  </v-icon>
                  {{ Math.abs(stat.change) }}% from last month
                </p>
              </div>
              <v-avatar :color="stat.color" size="56">
                <v-icon size="32" color="white">{{ stat.icon }}</v-icon>
              </v-avatar>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Recent Forms & Quick Actions -->
    <v-row class="mt-6">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title class="d-flex align-center">
            <span>Recent Forms</span>
            <v-spacer />
            <v-btn
              variant="text"
              color="primary"
              @click="goToForms"
            >
              View All
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-list v-if="recentForms.length > 0">
              <v-list-item
                v-for="form in recentForms"
                :key="form.id"
                @click="openForm(form.id)"
                class="cursor-pointer"
              >
                <template #prepend>
                  <v-icon>mdi-file-document</v-icon>
                </template>
                <v-list-item-title>{{ form.name }}</v-list-item-title>
                <v-list-item-subtitle>
                  {{ form.submission_count || 0 }} submissions
                  <v-chip
                    size="small"
                    :color="getStatusColor(form.status)"
                    class="ml-2"
                  >
                    {{ form.status }}
                  </v-chip>
                </v-list-item-subtitle>
                <template #append>
                  <v-btn
                    v-if="canEditForm"
                    icon="mdi-pencil"
                    size="small"
                    variant="text"
                    @click.stop="editForm(form.id)"
                  />
                  <v-btn
                    v-if="canViewAnalytics"
                    icon="mdi-chart-bar"
                    size="small"
                    variant="text"
                    @click.stop="viewAnalytics(form.id)"
                  />
                </template>
              </v-list-item>
            </v-list>
            <div v-else class="text-center py-8">
              <v-icon size="64" color="grey-lighten-1">mdi-file-document-outline</v-icon>
              <p class="text-subtitle-1 text-medium-emphasis mt-4">No forms yet</p>
              <v-btn
                v-if="canCreateForm"
                color="primary"
                class="mt-4"
                @click="createNewForm"
              >
                Create Your First Form
              </v-btn>
              <p v-else class="text-subtitle-2 text-medium-emphasis mt-4">
                Contact an administrator to create forms
              </p>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>Quick Actions</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item
                v-if="canCreateForm"
                prepend-icon="mdi-plus-circle"
                title="Create New Form"
                subtitle="Start building a new form"
                @click="createNewForm"
              />
              <v-divider v-if="canCreateForm" />
              <v-list-item
                prepend-icon="mdi-file-document-multiple"
                title="Browse Templates"
                subtitle="Use pre-built templates"
                @click="browseTemplates"
                disabled
              />
              <v-divider />
              <v-list-item
                v-if="canViewAnalytics"
                prepend-icon="mdi-chart-line"
                title="View Analytics"
                subtitle="See all form insights"
                @click="viewAllAnalytics"
                disabled
              />
              <v-divider v-if="canViewAnalytics" />
              <v-list-item
                prepend-icon="mdi-cog"
                title="Settings"
                subtitle="Configure your account"
                @click="goToSettings"
                disabled
              />
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
import { useAuthStore } from '@/stores/auth'
import { useFormsStore } from '@/stores/forms'
import { usePermissions } from '@/composables/usePermissions'

const router = useRouter()
const authStore = useAuthStore()
const formsStore = useFormsStore()
const { canCreateForm, canEditForm, canViewAnalytics } = usePermissions()

const currentUser = computed(() => authStore.currentUser)
const recentForms = computed(() => formsStore.forms.slice(0, 5))

// Stats
const stats = ref([
  {
    title: 'Total Forms',
    value: 0,
    change: 0,
    icon: 'mdi-file-document-multiple',
    color: 'primary'
  },
  {
    title: 'Total Submissions',
    value: 0,
    change: 0,
    icon: 'mdi-inbox',
    color: 'success'
  },
  {
    title: 'Avg. Conversion',
    value: '0%',
    change: 0,
    icon: 'mdi-chart-line',
    color: 'info'
  },
  {
    title: 'Active Forms',
    value: 0,
    change: 0,
    icon: 'mdi-check-circle',
    color: 'warning'
  }
])

onMounted(async () => {
  await formsStore.fetchForms()
  updateStats()
})

function updateStats() {
  const forms = formsStore.forms
  if (stats.value[0]) stats.value[0].value = forms.length
  if (stats.value[3]) stats.value[3].value = forms.filter(f => f.status === 'published').length
  
  // Calculate total submissions
  const totalSubmissions = forms.reduce((sum, form) => sum + (form.submission_count || 0), 0)
  if (stats.value[1]) stats.value[1].value = totalSubmissions
}

function getStatusColor(status: string) {
  const colorMap: Record<string, string> = {
    draft: 'grey',
    published: 'green',
    archived: 'orange'
  }
  return colorMap[status] || 'grey'
}

function createNewForm() {
  router.push('/forms/new')
}

function goToForms() {
  router.push('/forms')
}

function openForm(id: number) {
  router.push(`/forms/${id}`)
}

function editForm(id: number) {
  router.push(`/forms/${id}/edit`)
}

function viewAnalytics(id: number) {
  router.push(`/forms/${id}/analytics`)
}

function browseTemplates() {
  // TODO: Implement templates feature
}

function viewAllAnalytics() {
  // TODO: Implement global analytics
}

function goToSettings() {
  // TODO: Implement settings
}
</script>

<style scoped>
.dashboard {
  padding: 24px;
}

.cursor-pointer {
  cursor: pointer;
}
</style>

