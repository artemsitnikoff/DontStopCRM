import { ref, type Ref } from 'vue'

export interface ApiState<T> {
  data: Ref<T | null>
  loading: Ref<boolean>
  error: Ref<string | null>
}

export function useApi<T>() {
  const data = ref<T | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const execute = async (apiCall: () => Promise<T>): Promise<T | null> => {
    try {
      loading.value = true
      error.value = null
      const result = await apiCall()
      data.value = result
      return result
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Произошла ошибка'
      error.value = message
      return null
    } finally {
      loading.value = false
    }
  }

  const reset = () => {
    data.value = null
    error.value = null
    loading.value = false
  }

  return {
    data,
    loading,
    error,
    execute,
    reset,
  }
}