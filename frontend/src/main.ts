import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import router from './router'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Auto-login for development
import { useAuthStore } from '@/stores/useAuthStore'
const authStore = useAuthStore()
authStore.initAuth()

// If no token, auto-login with dev credentials
if (!authStore.isAuthenticated) {
  import('@/api/auth').then(({ login }) => {
    login({ email: 'admin@dnstp.ru', password: 'admin123' })
      .then((response) => {
        authStore.setAuth(response)
      })
      .catch(() => {
        // Backend not available, continue without auth
      })
  })
}

app.mount('#app')