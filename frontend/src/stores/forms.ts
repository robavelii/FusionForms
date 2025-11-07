import { defineStore } from 'pinia'
import apiClient from '@/services/api'

// Types for form fields and schema
export interface FormField {
  id?: string | number
  label: string  // Changed from 'name' to 'label' to match form builder
  type: string
  required?: boolean
  options?: any
  value?: any
  [key: string]: any
}

export interface FormSchema {
  title: string
  description?: string
  fields: FormField[]
  settings?: Record<string, any>
}

export interface Form {
  id: string | number  // Backend uses UUID (string), but we support both
  title: string
  name?: string  // Some APIs might use 'name' instead of 'title'
  description?: string
  schema: FormSchema
  status?: string
  version?: number
  created_by?: any
  created_at?: string
  updated_at?: string
  published_at?: string
  [key: string]: any
}

// State type
interface FormsState {
  forms: Form[]
  currentForm: Form | null
  formSchema: FormSchema
  loading: boolean
  error: string | null
}

export const useFormsStore = defineStore('forms', {
  state: (): FormsState => ({
    forms: [],
    currentForm: null,
    formSchema: {
      title: '',
      description: '',
      fields: [],
      settings: {
        submitButtonText: 'Submit',
        successMessage: 'Thank you for your submission!',
        saveProgress: false,
        multipleSubmissions: false,
        allowMultipleSubmissions: false,
        showProgressBar: false,
        enableHoneypot: false,
        enableCaptcha: false,
        redirectUrl: ''
      }
    },
    loading: false,
    error: null
  }),

  getters: {
    allForms: (state) => state.forms,
    currentForm: (state) => state.currentForm,
    formSchema: (state) => state.formSchema,
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

    setForms(forms: Form[]) {
      this.forms = forms
    },

    setCurrentForm(form: Form) {
      this.currentForm = form
    },

    setFormSchema(schema: FormSchema) {
      this.formSchema = schema
    },

    addField(field: FormField) {
      this.formSchema.fields.push(field)
    },

    updateField(index: number, field: FormField) {
      this.formSchema.fields.splice(index, 1, field)
    },

    removeField(index: number) {
      this.formSchema.fields.splice(index, 1)
    },

    resetFormSchema() {
      this.formSchema = {
        title: '',
        description: '',
        fields: [],
        settings: {
          submitButtonText: 'Submit',
          successMessage: 'Thank you for your submission!',
          saveProgress: false,
          multipleSubmissions: false,
          allowMultipleSubmissions: false,
          showProgressBar: false,
          enableHoneypot: false,
          enableCaptcha: false,
          redirectUrl: ''
        }
      }
    },

    async fetchForms() {
      this.setLoading(true)
      this.setError(null)
      try {
        const response = await apiClient.get('/forms/')
        // Handle both paginated and non-paginated responses
        const forms = response.data.results || response.data
        this.setForms(Array.isArray(forms) ? forms : [])
      } catch (error: any) {
        this.setError(error.message || 'Failed to fetch forms')
        throw error
      } finally {
        this.setLoading(false)
      }
    },

    async fetchForm(id: string | number) {
      this.setLoading(true)
      this.setError(null)
      try {
        const response = await apiClient.get(`/forms/${id}/`)
        this.setCurrentForm(response.data)
        // Ensure schema has all required properties with defaults
        const schema = response.data.schema || {}
        // If schema doesn't have title/description, use form's title/description
        this.setFormSchema({
          title: schema.title || response.data.title || '',
          description: schema.description || response.data.description || '',
          fields: schema.fields || [],
          settings: {
            submitButtonText: 'Submit',
            successMessage: 'Thank you for your submission!',
            saveProgress: false,
            multipleSubmissions: false,
            allowMultipleSubmissions: false,
            showProgressBar: false,
            enableHoneypot: false,
            enableCaptcha: false,
            redirectUrl: '',
            ...schema.settings
          }
        })
      } catch (error: any) {
        this.setError(error.message || 'Failed to fetch form')
        throw error
      } finally {
        this.setLoading(false)
      }
    },

    async createForm(formData: Partial<Form>) {
      this.setLoading(true)
      this.setError(null)
      try {
        const response = await apiClient.post('/forms/', formData)
        this.setCurrentForm(response.data)
        return response.data
      } catch (error: any) {
        this.setError(error.message || 'Failed to create form')
        throw error
      } finally {
        this.setLoading(false)
      }
    },

    async updateForm(id: string | number, formData: Partial<Form>) {
      this.setLoading(true)
      this.setError(null)
      try {
        const response = await apiClient.put(`/forms/${id}/`, formData)
        this.setCurrentForm(response.data)
        // Update schema if it was included in the response
        if (response.data.schema) {
          this.setFormSchema(response.data.schema)
        }
        return response.data
      } catch (error: any) {
        this.setError(error.message || 'Failed to update form')
        throw error
      } finally {
        this.setLoading(false)
      }
    },

    async publishForm(id: string | number) {
      this.setLoading(true)
      this.setError(null)
      try {
        const response = await apiClient.post(`/forms/${id}/publish/`)
        // Refresh the form to get updated status
        await this.fetchForm(id)
        return response.data
      } catch (error: any) {
        this.setError(error.message || 'Failed to publish form')
        throw error
      } finally {
        this.setLoading(false)
      }
    },

    async duplicateForm(id: string | number) {
      this.setLoading(true)
      this.setError(null)
      try {
        const response = await apiClient.post(`/forms/${id}/duplicate/`)
        return response.data
      } catch (error: any) {
        this.setError(error.message || 'Failed to duplicate form')
        throw error
      } finally {
        this.setLoading(false)
      }
    },

    async deleteForm(id: string | number) {
      this.setLoading(true)
      this.setError(null)
      try {
        await apiClient.delete(`/forms/${id}/`)
        this.forms = this.forms.filter(f => String(f.id) !== String(id))
        return true
      } catch (error: any) {
        this.setError(error.message || 'Failed to delete form')
        throw error
      } finally {
        this.setLoading(false)
      }
    }
  }
})
