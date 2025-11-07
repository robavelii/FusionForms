import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import type { ThemeDefinition } from 'vuetify'

// Dark Theme - Matches design mockup
const darkTheme: ThemeDefinition = {
  dark: true,
  colors: {
    // Background colors
    background: '#1a202c',        // Main background
    surface: '#2d3748',           // Card/surface background
    'surface-variant': '#3a4556', // Elevated surfaces
    'surface-bright': '#4a5568',  // Hover states
    
    // Primary colors
    primary: '#3b82f6',           // Blue accent (buttons, links)
    'primary-darken-1': '#2563eb',
    'primary-lighten-1': '#60a5fa',
    
    // Secondary colors
    secondary: '#64748b',         // Gray accent
    'secondary-darken-1': '#475569',
    'secondary-lighten-1': '#94a3b8',
    
    // Semantic colors
    success: '#10b981',           // Green
    warning: '#f59e0b',           // Orange
    error: '#ef4444',             // Red
    info: '#3b82f6',              // Blue
    
    // Text colors
    'on-background': '#f8fafc',   // Text on background
    'on-surface': '#f1f5f9',      // Text on surface
    'on-primary': '#ffffff',      // Text on primary
    'on-secondary': '#ffffff',    // Text on secondary
    'on-success': '#ffffff',
    'on-warning': '#ffffff',
    'on-error': '#ffffff',
    'on-info': '#ffffff',
    
    // Additional colors
    accent: '#818cf8',            // Purple accent
    anchor: '#60a5fa',            // Link color
  }
}

// Light Theme - Clean and modern
const lightTheme: ThemeDefinition = {
  dark: false,
  colors: {
    // Background colors
    background: '#f8fafc',        // Main background
    surface: '#ffffff',           // Card/surface background
    'surface-variant': '#f1f5f9', // Elevated surfaces
    'surface-bright': '#e2e8f0',  // Hover states
    
    // Primary colors
    primary: '#3b82f6',           // Blue accent
    'primary-darken-1': '#2563eb',
    'primary-lighten-1': '#60a5fa',
    
    // Secondary colors
    secondary: '#64748b',         // Gray accent
    'secondary-darken-1': '#475569',
    'secondary-lighten-1': '#94a3b8',
    
    // Semantic colors
    success: '#10b981',           // Green
    warning: '#f59e0b',           // Orange
    error: '#ef4444',             // Red
    info: '#3b82f6',              // Blue
    
    // Text colors
    'on-background': '#0f172a',   // Text on background
    'on-surface': '#1e293b',      // Text on surface
    'on-primary': '#ffffff',      // Text on primary
    'on-secondary': '#ffffff',    // Text on secondary
    'on-success': '#ffffff',
    'on-warning': '#ffffff',
    'on-error': '#ffffff',
    'on-info': '#ffffff',
    
    // Additional colors
    accent: '#818cf8',            // Purple accent
    anchor: '#2563eb',            // Link color
  }
}

const vuetify = createVuetify({
  components,
  directives,
  
  theme: {
    defaultTheme: 'dark', // Set to 'dark' to match your mockup
    themes: {
      dark: darkTheme,
      light: lightTheme
    },
    variations: {
      colors: ['primary', 'secondary', 'success', 'warning', 'error', 'info'],
      lighten: 5,
      darken: 5
    }
  },
  
  defaults: {
    global: {
      ripple: true,
    },
    VBtn: {
      rounded: 'lg',
      elevation: 0,
      style: 'text-transform: none; letter-spacing: normal;'
    },
    VCard: {
      elevation: 1,
      rounded: 'lg'
    },
    VTextField: {
      variant: 'outlined',
      density: 'comfortable',
      color: 'primary'
    },
    VTextarea: {
      variant: 'outlined',
      density: 'comfortable',
      color: 'primary'
    },
    VSelect: {
      variant: 'outlined',
      density: 'comfortable',
      color: 'primary'
    },
    VAutocomplete: {
      variant: 'outlined',
      density: 'comfortable',
      color: 'primary'
    },
    VCheckbox: {
      color: 'primary'
    },
    VRadio: {
      color: 'primary'
    },
    VSwitch: {
      color: 'primary',
      inset: true
    },
    VChip: {
      rounded: 'lg'
    },
    VAlert: {
      variant: 'tonal',
      rounded: 'lg'
    }
  }
})

export default vuetify
