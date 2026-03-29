import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, TokenResponse } from '@/types/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const user = ref<User | null>(null)

  const isAuthenticated = computed(() => !!token.value)

  const setAuth = (authData: TokenResponse) => {
    token.value = authData.access_token
    user.value = authData.user

    localStorage.setItem('access_token', authData.access_token)
    localStorage.setItem('user', JSON.stringify(authData.user))
  }

  const setUser = (userData: User) => {
    user.value = userData
    localStorage.setItem('user', JSON.stringify(userData))
  }

  const clearAuth = () => {
    token.value = null
    user.value = null

    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
  }

  const initAuth = () => {
    const savedUser = localStorage.getItem('user')
    if (savedUser && token.value) {
      try {
        user.value = JSON.parse(savedUser)
      } catch {
        clearAuth()
      }
    }
  }

  return {
    token,
    user,
    isAuthenticated,
    setAuth,
    setUser,
    clearAuth,
    initAuth,
  }
})