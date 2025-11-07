import { defineStore } from 'pinia'
import apiClient from '@/services/api'

// Types
export interface Submission {
  id: number
  formId: number
  data: Record<string, any>
  [key: string]: any
}

interface SubmissionsState {
  submissions: Submission[]
  currentSubmission: Submission | null
  loading: boolean
  error: string | null
}

export const useSubmissionsStore = defineStore('submissions', {
  state: (): SubmissionsState => ({
    submissions: [],
    currentSubmission: null,
    loading: false,
    error: null
  }),

  getters: {
    allSubmissions: (state) => state.submissions,
    currentSubmission: (state) => state.currentSubmission,
    isLoading: (state) => state.loading,
    error: (state) => state.error
  },

  actions: {
    setLoading(loading: boolean) {
      this.loading = loading
    },

    setError(error: string | null) {
      this.error = error
    },

    setSubmissions(submissions: Submission[]) {
      this.submissions = submissions
    },

    setCurrentSubmission(submission: Submission) {
      this.currentSubmission = submission
    },

    async fetchSubmissions(formId: number) {
      this.setLoading(true)
      this.setError(null)
      try {
        const response = await apiClient.get(`/submissions/?form_id=${formId}`)
        this.setSubmissions(response.data.results)
      } catch (error: any) {
        this.setError(error.message || 'Failed to fetch submissions')
      } finally {
        this.setLoading(false)
      }
    },

    async fetchSubmission(id: number) {
      this.setLoading(true)
      this.setError(null)
      try {
        const response = await apiClient.get(`/submissions/${id}/`)
        this.setCurrentSubmission(response.data)
      } catch (error: any) {
        this.setError(error.message || 'Failed to fetch submission')
      } finally {
        this.setLoading(false)
      }
    },

    async createSubmission(submissionData: Partial<Submission>) {
      this.setLoading(true)
      this.setError(null)
      try {
        const response = await apiClient.post('/submissions/', submissionData)
        return response.data
      } catch (error: any) {
        this.setError(error.message || 'Failed to create submission')
        throw error
      } finally {
        this.setLoading(false)
      }
    }
  }
})
