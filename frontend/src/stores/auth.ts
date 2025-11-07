import { defineStore } from 'pinia'
import apiClient from '@/services/api'

// Define types for the user and state
interface User {
  id: number
  username: string
  email: string
  first_name?: string
  last_name?: string
  role?: string
  organization?: string
  [key: string]: any
}

interface RegisterData {
  username: string
  email: string
  password: string
  password_confirm: string
  first_name?: string
  last_name?: string
  role?: string
  organization?: string
}

interface AuthState {
  user: User | null
  token: string
  status: 'idle' | 'loading' | 'success' | 'error'
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    token: localStorage.getItem('token') || '',
    status: 'idle'
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    authStatus: (state) => state.status,
    currentUser: (state) => state.user,
    isAdmin: (state) => state.user?.role === 'admin',
    isSuperAdmin: (state) => state.user?.role === 'super_admin'
  },

  actions: {
    async login(userCredentials: { email: string; password: string }) {
      this.status = 'loading'
      try {
        const response = await apiClient.post('/accounts/login/', userCredentials)
        const { token, user } = response.data

        localStorage.setItem('token', token)
        this.token = token
        this.user = user
        this.status = 'success'

        return response
      } catch (err) {
        this.status = 'error'
        localStorage.removeItem('token')
        throw err
      }
    },

    async register(userData: RegisterData) {
      this.status = 'loading'
      try {
        const response = await apiClient.post('/accounts/register/', userData)
        const { token, user } = response.data

        localStorage.setItem('token', token)
        this.token = token
        this.user = user
        this.status = 'success'

        return response
      } catch (err) {
        this.status = 'error'
        localStorage.removeItem('token')
        throw err
      }
    },

    async logout() {
      this.user = null
      this.token = ''
      this.status = 'idle'
      localStorage.removeItem('token')
    },

    async fetchProfile() {
      try {
        const response = await apiClient.get('/accounts/profile/')
        this.user = response.data
        return response
      } catch (err) {
        throw err
      }
    }
  }
})
