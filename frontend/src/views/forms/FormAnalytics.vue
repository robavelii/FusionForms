<template>
  <v-container fluid class="form-analytics">
    <!-- Header -->
    <v-row>
      <v-col cols="12">
        <div class="d-flex align-center mb-4">
          <v-btn
            icon="mdi-arrow-left"
            variant="text"
            @click="goBack"
          />
          <div class="ml-4">
            <h1 class="text-h4 font-weight-bold">{{ formTitle }} - Analytics</h1>
            <p class="text-subtitle-1 text-medium-emphasis">Real-time insights and data visualization</p>
          </div>
          <v-spacer />
          <v-btn
            color="primary"
            prepend-icon="mdi-download"
            variant="outlined"
            @click="exportData"
          >
            Export Data
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <!-- Date Range Filter -->
    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-text>
            <v-row>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="dateRange.start"
                  label="Start Date"
                  type="date"
                  variant="outlined"
                  density="compact"
                  @change="fetchAnalytics"
                />
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="dateRange.end"
                  label="End Date"
                  type="date"
                  variant="outlined"
                  density="compact"
                  @change="fetchAnalytics"
                />
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-text>
            <v-btn-toggle
              v-model="selectedPeriod"
              mandatory
              divided
              @update:model-value="changePeriod"
            >
              <v-btn value="7d">Last 7 Days</v-btn>
              <v-btn value="30d">Last 30 Days</v-btn>
              <v-btn value="90d">Last 90 Days</v-btn>
              <v-btn value="all">All Time</v-btn>
            </v-btn-toggle>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Key Metrics -->
    <v-row class="mt-4">
      <v-col
        v-for="metric in keyMetrics"
        :key="metric.title"
        cols="12"
        sm="6"
        md="3"
      >
        <v-card>
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <p class="text-subtitle-2 text-medium-emphasis mb-1">
                  {{ metric.title }}
                </p>
                <h2 class="text-h4 font-weight-bold">
                  {{ metric.value }}
                </h2>
                <p
                  v-if="metric.change !== undefined"
                  :class="metric.change >= 0 ? 'text-success' : 'text-error'"
                  class="text-caption mt-1"
                >
                  <v-icon size="14">
                    {{ metric.change >= 0 ? 'mdi-arrow-up' : 'mdi-arrow-down' }}
                  </v-icon>
                  {{ Math.abs(metric.change) }}%
                </p>
              </div>
              <v-avatar :color="metric.color" size="56">
                <v-icon size="32" color="white">{{ metric.icon }}</v-icon>
              </v-avatar>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Charts Row 1 -->
    <v-row class="mt-4">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>Submission Trends</v-card-title>
          <v-card-text>
            <Line :data="submissionTrendsData" :options="lineChartOptions" />
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>Completion Rate</v-card-title>
          <v-card-text>
            <Doughnut :data="completionRateData" :options="doughnutChartOptions" />
            <div class="text-center mt-4">
              <p class="text-h5 font-weight-bold">{{ completionRate }}%</p>
              <p class="text-subtitle-2 text-medium-emphasis">Overall Completion</p>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Charts Row 2 -->
    <v-row class="mt-4">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Top Referrers</v-card-title>
          <v-card-text>
            <Bar :data="referrersData" :options="barChartOptions" />
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Device Breakdown</v-card-title>
          <v-card-text>
            <Pie :data="deviceBreakdownData" :options="pieChartOptions" />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Field-specific Analytics -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title>Field-Specific Analytics</v-card-title>
          <v-card-text>
            <v-expansion-panels>
              <v-expansion-panel
                v-for="field in fieldAnalytics"
                :key="field.id"
              >
                <v-expansion-panel-title>
                  <div class="d-flex justify-space-between w-100 mr-4">
                    <span>{{ field.label }}</span>
                    <v-chip size="small" color="primary">
                      {{ field.responseRate }}% response rate
                    </v-chip>
                  </div>
                </v-expansion-panel-title>
                <v-expansion-panel-text>
                  <div v-if="field.type === 'text' || field.type === 'textarea'">
                    <p class="text-subtitle-2 mb-2">Most Common Responses:</p>
                    <v-chip
                      v-for="(response, idx) in field.topResponses"
                      :key="idx"
                      class="ma-1"
                    >
                      {{ response }}
                    </v-chip>
                  </div>
                  <div v-else-if="field.type === 'select' || field.type === 'radio' || field.type === 'checkbox'">
                    <Bar :data="getFieldChartData(field)" :options="barChartOptions" />
                  </div>
                  <div v-else-if="field.type === 'rating'">
                    <p class="text-h6">Average Rating: {{ field.averageRating }}/5</p>
                    <Bar :data="getFieldChartData(field)" :options="barChartOptions" />
                  </div>
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Line, Doughnut, Bar, Pie } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import apiClient from '@/services/api'
import { useSnackbarStore } from '@/stores/snackbar'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const route = useRoute()
const router = useRouter()
const snackbarStore = useSnackbarStore()

const formId = route.params.id
const formTitle = ref('Form')
const loading = ref(false)
const selectedPeriod = ref('30d')

const dateRange = reactive({
  start: '',
  end: ''
})

// Key Metrics
const keyMetrics = ref([
  {
    title: 'Total Submissions',
    value: '1,832',
    change: 12.5,
    icon: 'mdi-inbox',
    color: 'primary'
  },
  {
    title: 'Conversion Rate',
    value: '45.2%',
    change: 5.3,
    icon: 'mdi-chart-line',
    color: 'success'
  },
  {
    title: 'Avg. Time',
    value: '3m 42s',
    change: -8.1,
    icon: 'mdi-clock',
    color: 'info'
  },
  {
    title: 'Completion Rate',
    value: '78.5%',
    change: 3.2,
    icon: 'mdi-check-circle',
    color: 'warning'
  }
])

const completionRate = computed(() => 78.5)

// Chart Data
const submissionTrendsData = ref({
  labels: ['Jan 1', 'Jan 2', 'Jan 3', 'Jan 4', 'Jan 5', 'Jan 6', 'Jan 7'],
  datasets: [
    {
      label: 'Submissions',
      data: [12, 19, 15, 25, 22, 30, 28],
      borderColor: '#1976D2',
      backgroundColor: 'rgba(25, 118, 210, 0.1)',
      fill: true,
      tension: 0.4
    }
  ]
})

const completionRateData = ref({
  labels: ['Completed', 'Abandoned'],
  datasets: [
    {
      data: [78.5, 21.5],
      backgroundColor: ['#4CAF50', '#FF5252'],
      borderWidth: 0
    }
  ]
})

const referrersData = ref({
  labels: ['Google', 'Facebook', 'Twitter', 'Direct', 'Other'],
  datasets: [
    {
      label: 'Referrers',
      data: [450, 320, 180, 280, 120],
      backgroundColor: '#1976D2'
    }
  ]
})

const deviceBreakdownData = ref({
  labels: ['Desktop', 'Mobile', 'Tablet'],
  datasets: [
    {
      data: [60, 30, 10],
      backgroundColor: ['#1976D2', '#4CAF50', '#FB8C00']
    }
  ]
})

const fieldAnalytics = ref([
  {
    id: 1,
    label: 'Full Name',
    type: 'text',
    responseRate: 95,
    topResponses: ['John Doe', 'Jane Smith', 'Bob Johnson']
  },
  {
    id: 2,
    label: 'Event Type',
    type: 'select',
    responseRate: 92,
    options: ['Conference', 'Workshop', 'Webinar'],
    responses: [120, 80, 50]
  },
  {
    id: 3,
    label: 'Rating',
    type: 'rating',
    responseRate: 88,
    averageRating: 4.3,
    responses: [5, 10, 20, 80, 135]
  }
])

// Chart Options
const lineChartOptions = {
  responsive: true,
  maintainAspectRatio: true,
  plugins: {
    legend: {
      display: true,
      position: 'top' as const
    }
  },
  scales: {
    y: {
      beginAtZero: true
    }
  }
}

const doughnutChartOptions = {
  responsive: true,
  maintainAspectRatio: true,
  plugins: {
    legend: {
      position: 'bottom' as const
    }
  }
}

const barChartOptions = {
  responsive: true,
  maintainAspectRatio: true,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    y: {
      beginAtZero: true
    }
  }
}

const pieChartOptions = {
  responsive: true,
  maintainAspectRatio: true,
  plugins: {
    legend: {
      position: 'bottom' as const
    }
  }
}

onMounted(() => {
  setDefaultDateRange()
  fetchAnalytics()
})

function setDefaultDateRange() {
  const end = new Date()
  const start = new Date()
  start.setDate(start.getDate() - 30)
  
  dateRange.end = end.toISOString().split('T')[0]
  dateRange.start = start.toISOString().split('T')[0]
}

function changePeriod(period: string) {
  const end = new Date()
  const start = new Date()
  
  switch (period) {
    case '7d':
      start.setDate(start.getDate() - 7)
      break
    case '30d':
      start.setDate(start.getDate() - 30)
      break
    case '90d':
      start.setDate(start.getDate() - 90)
      break
    case 'all':
      start.setFullYear(2020)
      break
  }
  
  dateRange.end = end.toISOString().split('T')[0]
  dateRange.start = start.toISOString().split('T')[0]
  fetchAnalytics()
}

async function fetchAnalytics() {
  loading.value = true
  try {
    const response = await apiClient.get(`/analytics/forms/${formId}/`, {
      params: {
        start_date: dateRange.start,
        end_date: dateRange.end
      }
    })
    
    // Update metrics and charts with real data
    const data = response.data
    formTitle.value = data.form_name || 'Form'
    
    // Update key metrics if available
    if (data.total_submissions !== undefined) {
      keyMetrics.value[0].value = data.total_submissions.toLocaleString()
    }
    if (data.conversion_rate !== undefined) {
      keyMetrics.value[1].value = `${data.conversion_rate}%`
    }
    
    // Update chart data if available
    if (data.submission_trends) {
      submissionTrendsData.value = {
        labels: data.submission_trends.labels,
        datasets: [{
          label: 'Submissions',
          data: data.submission_trends.data,
          borderColor: '#1976D2',
          backgroundColor: 'rgba(25, 118, 210, 0.1)',
          fill: true,
          tension: 0.4
        }]
      }
    }
  } catch (error) {
    console.error('Error fetching analytics:', error)
    snackbarStore.error('Failed to load analytics data')
  } finally {
    loading.value = false
  }
}

function getFieldChartData(field: any) {
  return {
    labels: field.options || field.responses?.map((_: any, i: number) => `${i + 1} stars`) || [],
    datasets: [
      {
        label: 'Responses',
        data: field.responses || [],
        backgroundColor: '#1976D2'
      }
    ]
  }
}

async function exportData() {
  try {
    const response = await apiClient.get(`/analytics/forms/${formId}/export/`, {
      params: {
        start_date: dateRange.start,
        end_date: dateRange.end,
        format: 'csv'
      },
      responseType: 'blob'
    })
    
    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `form-${formId}-analytics.csv`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    
    snackbarStore.success('Data exported successfully')
  } catch (error) {
    console.error('Error exporting data:', error)
    snackbarStore.error('Failed to export data')
  }
}

function goBack() {
  router.push(`/forms/${formId}`)
}
</script>

<style scoped>
.form-analytics {
  padding: 24px;
}
</style>
