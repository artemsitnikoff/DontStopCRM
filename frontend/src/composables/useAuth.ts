import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'
import * as authApi from '@/api/auth'
import { useApi } from './useApi'
import type { LoginRequest, RegisterRequest } from '@/types/auth'

export function useAuth() {
  const authStore = useAuthStore()
  const router = useRouter()
  const { execute, loading, error } = useApi()

  const isAuthenticated = computed(() => authStore.isAuthenticated)
  const user = computed(() => authStore.user)

  const login = async (credentials: LoginRequest): Promise<boolean> => {
    const result = await execute(() => authApi.login(credentials))
    if (result) {
      authStore.setAuth(result)
      router.push('/')
      return true
    }
    return false
  }

  const register = async (userData: RegisterRequest): Promise<boolean> => {
    const result = await execute(() => authApi.register(userData))
    if (result) {
      authStore.setAuth(result)
      router.push('/')
      return true
    }
    return false
  }

  const logout = async (): Promise<void> => {
    try {
      await authApi.logout()
    } catch {
      // Ignore error, clear auth anyway
    }
    authStore.clearAuth()
    router.push('/login')
  }

  const checkAuth = async (): Promise<void> => {
    if (!authStore.token) return

    try {
      const user = await authApi.getMe()
      authStore.setUser(user)
    } catch {
      authStore.clearAuth()
    }
  }

  return {
    isAuthenticated,
    user,
    loading,
    error,
    login,
    register,
    logout,
    checkAuth,
  }
}