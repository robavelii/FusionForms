import { ref, computed, watch } from 'vue'
import { useTheme as useVuetifyTheme } from 'vuetify'

// Theme state - persisted in localStorage
const THEME_STORAGE_KEY = 'fusionforms-theme'

export function useTheme() {
  const vuetifyTheme = useVuetifyTheme()
  
  // Get initial theme from localStorage or default to 'dark'
  const getInitialTheme = (): 'light' | 'dark' => {
    const stored = localStorage.getItem(THEME_STORAGE_KEY)
    if (stored === 'light' || stored === 'dark') {
      return stored
    }
    // Default to dark theme (matches your mockup)
    return 'dark'
  }
  
  const currentTheme = ref<'light' | 'dark'>(getInitialTheme())
  
  // Computed properties
  const isDark = computed(() => currentTheme.value === 'dark')
  const isLight = computed(() => currentTheme.value === 'light')
  
  // Toggle theme
  const toggleTheme = () => {
    currentTheme.value = currentTheme.value === 'dark' ? 'light' : 'dark'
  }
  
  // Set specific theme
  const setTheme = (theme: 'light' | 'dark') => {
    currentTheme.value = theme
  }
  
  // Set dark mode
  const setDark = () => {
    currentTheme.value = 'dark'
  }
  
  // Set light mode
  const setLight = () => {
    currentTheme.value = 'light'
  }
  
  // Watch for theme changes and update Vuetify + localStorage
  watch(currentTheme, (newTheme) => {
    vuetifyTheme.global.name.value = newTheme
    localStorage.setItem(THEME_STORAGE_KEY, newTheme)
    
    // Update meta theme-color for mobile browsers
    const metaThemeColor = document.querySelector('meta[name="theme-color"]')
    if (metaThemeColor) {
      metaThemeColor.setAttribute(
        'content',
        newTheme === 'dark' ? '#1a202c' : '#f8fafc'
      )
    }
  }, { immediate: true })
  
  return {
    currentTheme,
    isDark,
    isLight,
    toggleTheme,
    setTheme,
    setDark,
    setLight
  }
}

