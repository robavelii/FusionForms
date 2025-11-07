import { defineStore } from 'pinia'

interface SnackbarState {
  visible: boolean
  message: string
  color: string
  timeout: number
}

export const useSnackbarStore = defineStore('snackbar', {
  state: (): SnackbarState => ({
    visible: false,
    message: '',
    color: 'info',
    timeout: 3000
  }),

  actions: {
    show(options: { message: string; color?: string; timeout?: number }) {
      this.message = options.message
      this.color = options.color || 'info'
      this.timeout = options.timeout || 3000
      this.visible = true
    },

    hide() {
      this.visible = false
    },

    success(message: string, timeout?: number) {
      this.show({ message, color: 'success', timeout })
    },

    error(message: string, timeout?: number) {
      this.show({ message, color: 'error', timeout })
    },

    warning(message: string, timeout?: number) {
      this.show({ message, color: 'warning', timeout })
    },

    info(message: string, timeout?: number) {
      this.show({ message, color: 'info', timeout })
    }
  }
})


