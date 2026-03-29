<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppAvatar from '@/components/ui/AppAvatar.vue'
import { useAuth } from '@/composables/useAuth'

const route = useRoute()
const router = useRouter()
const { user, logout } = useAuth()

const navigationItems = [
  {
    name: 'Dashboard',
    route: '/dashboard',
    icon: 'chart-bar'
  },
  {
    name: 'Leads',
    route: '/leads',
    icon: 'users'
  },
  {
    name: 'Chats',
    route: '/chats',
    icon: 'chat'
  },
  {
    name: 'Calendar',
    route: '/calendar',
    icon: 'calendar'
  }
]

const isActive = (itemRoute: string) => {
  return route.path === itemRoute
}

const handleLogout = async () => {
  await logout()
}
</script>

<template>
  <div class="flex flex-col h-full w-18 bg-primary text-white">
    <!-- Navigation Items -->
    <nav class="flex-1 px-3 py-4 space-y-2">
      <router-link
        v-for="item in navigationItems"
        :key="item.name"
        :to="item.route"
        class="flex flex-col items-center justify-center p-3 rounded-lg text-xs font-medium transition-colors hover:bg-white hover:bg-opacity-10 group"
        :class="{
          'bg-accent text-white': isActive(item.route),
          'text-gray-300 hover:text-white': !isActive(item.route)
        }"
      >
        <!-- Dashboard Icon -->
        <svg
          v-if="item.icon === 'chart-bar'"
          class="w-6 h-6 mb-1"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>

        <!-- Users Icon -->
        <svg
          v-else-if="item.icon === 'users'"
          class="w-6 h-6 mb-1"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
        </svg>

        <!-- Chat Icon -->
        <svg
          v-else-if="item.icon === 'chat'"
          class="w-6 h-6 mb-1"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>

        <!-- Calendar Icon -->
        <svg
          v-else-if="item.icon === 'calendar'"
          class="w-6 h-6 mb-1"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>

        <span class="text-center">{{ item.name }}</span>
      </router-link>
    </nav>

    <!-- User Section -->
    <div class="p-3 border-t border-white border-opacity-10">
      <div class="flex flex-col items-center space-y-2">
        <AppAvatar
          :name="user?.full_name"
          size="md"
        />

        <button
          @click="handleLogout"
          class="p-2 text-gray-300 hover:text-white hover:bg-white hover:bg-opacity-10 rounded-lg transition-colors"
          title="Выйти"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>