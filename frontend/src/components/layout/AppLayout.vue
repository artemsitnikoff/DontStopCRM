<script setup lang="ts">
import { onMounted } from 'vue'
import AppSidebar from './AppSidebar.vue'
import { useAuth } from '@/composables/useAuth'
import { useAuthStore } from '@/stores/useAuthStore'

const { checkAuth } = useAuth()
const authStore = useAuthStore()

onMounted(async () => {
  authStore.initAuth()
  if (authStore.token) {
    await checkAuth()
  }
})
</script>

<template>
  <div class="flex h-screen bg-bg">
    <!-- Sidebar -->
    <div class="flex-shrink-0 w-18">
      <AppSidebar />
    </div>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <main class="flex-1 overflow-y-auto">
        <router-view />
      </main>
    </div>
  </div>
</template>