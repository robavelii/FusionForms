import { defineStore } from 'pinia'
import axios from 'axios'

// Types for form fields and schema
export interface FormField {
  id?: number
  name: string
  type: string
  options?: string[]
  [key: string]: any
}

export interface FormSchema {
  title: string
  description: string
  fields: FormField[]
  settings: Record<string, any>
}

export interface Form {
  id: number
  name: string
  schema: FormSchema
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
      settings: {}
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
        settings: {}
      }
    },

    async fetchForms() {
      this.setLoading(true)
      this.setError(null)
      try {
        const response = await axios.get('/api/forms/')
        this.setForms(response.data.results)
      } catch (error: any) {
        this.setError(error.message || 'Failed to fetch forms')
      } finally {
        this.setLoading(false)
      }
    },

    async fetchForm(id: number) {
      this.setLoading(true)
      this.setError(null)
      try {
        const response = await axios.get(`/api/forms/${id}/`)
        this.setCurrentForm(response.data)
        this.setFormSchema(response.data.schema)
      } catch (error: any) {
        this.setError(error.message || 'Failed to fetch form')
      } finally {
        this.setLoading(false)
      }
    },

    async createForm(formData: Partial<Form>) {
      this.setLoading(true)
      this.setError(null)
      try {
        const response = await axios.post('/api/forms/', formData)
        this.setCurrentForm(response.data)
        return response.data
      } catch (error: any) {
        this.setError(error.message || 'Failed to create form')
        throw error
      } finally {
        this.setLoading(false)
      }
    },

    async updateForm(id: number, formData: Partial<Form>) {
      this.setLoading(true)
      this.setError(null)
      try {
        const response = await axios.put(`/api/forms/${id}/`, formData)
        this.setCurrentForm(response.data)
        return response.data
      } catch (error: any) {
        this.setError(error.message || 'Failed to update form')
        throw error
      } finally {
        this.setLoading(false)
      }
    },

    async publishForm(id: number) {
      this.setLoading(true)
      this.setError(null)
      try {
        const response = await axios.post(`/api/forms/${id}/publish/`)
        this.setCurrentForm(response.data)
        return response.data
      } catch (error: any) {
        this.setError(error.message || 'Failed to publish form')
        throw error
      } finally {
        this.setLoading(false)
      }
    },

    async duplicateForm(id: number) {
      this.setLoading(true)
      this.setError(null)
      try {
        const response = await axios.post(`/api/forms/${id}/duplicate/`)
        return response.data
      } catch (error: any) {
        this.setError(error.message || 'Failed to duplicate form')
        throw error
      } finally {
        this.setLoading(false)
      }
    }
  }
})
