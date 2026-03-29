import { ref } from 'vue'
import type { DashboardStats } from '@/types/dashboard'
import { getDashboardStats } from '@/api/dashboard'

export function useDashboard() {
  const stats = ref<DashboardStats | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchStats = async () => {
    try {
      loading.value = true
      error.value = null
      stats.value = await getDashboardStats()
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Произошла ошибка при загрузке данных'
      error.value = message
    } finally {
      loading.value = false
    }
  }

  return {
    stats,
    loading,
    error,
    fetchStats,
  }
}