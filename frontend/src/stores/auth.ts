import { defineStore } from 'pinia'
import axios from 'axios'

// Define types for the user and state
interface User {
  id: number
  username: string
  email: string
  role?: string
  [key: string]: any
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
    isAdmin: (state) => state.user?.role === 'admin'
  },

  actions: {
    async login(userCredentials: { username: string; password: string }) {
      this.status = 'loading'
      try {
        const response = await axios.post('/api/accounts/login/', userCredentials)
        const { token, user } = response.data

        localStorage.setItem('token', token)
        axios.defaults.headers.common['Authorization'] = `Token ${token}`

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

    async register(userData: { username: string; email: string; password: string }) {
      this.status = 'loading'
      try {
        const response = await axios.post('/api/accounts/register/', userData)
        const { token, user } = response.data

        localStorage.setItem('token', token)
        axios.defaults.headers.common['Authorization'] = `Token ${token}`

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
      delete axios.defaults.headers.common['Authorization']
    },

    async fetchProfile() {
      try {
        const response = await axios.get('/api/accounts/profile/')
        this.user = response.data
        return response
      } catch (err) {
        throw err
      }
    }
  }
})
