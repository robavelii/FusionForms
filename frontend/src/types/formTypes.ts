export interface FormFieldOption {
  label: string
  value: string | number
}

export interface FormField {
  id: string
  type: string
  label?: string
  required?: boolean
  options?: any
  value?: any
}

export interface Form {
  id: string
  title: string
  description: string
  status: 'draft' | 'published' | 'archived'
  fields: FormField[]
  settings: {
    submitButtonText?: string
    successMessage?: string
    saveProgress?: boolean
    multipleSubmissions?: boolean
  }
}
