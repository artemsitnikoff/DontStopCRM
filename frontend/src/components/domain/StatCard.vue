<script setup lang="ts">
const props = defineProps<{
  title: string
  value: string | number
  icon: 'users' | 'new' | 'calendar' | 'percent'
  color: string
}>()

const iconPaths = {
  users: "M12 14c-4.418 0-8 1.79-8 4v2h16v-2c0-2.21-3.582-4-8-4zm0-1c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4z",
  new: "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm5 11h-4v4h-2v-4H7v-2h4V7h2v4h4v2z",
  calendar: "M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z",
  percent: "M7.5 4A1.5 1.5 0 016 2.5 1.5 1.5 0 017.5 1 1.5 1.5 0 019 2.5 1.5 1.5 0 017.5 4zM2 6v2l10 10h2v-2L4 6H2zm14.5 14A1.5 1.5 0 0115 18.5a1.5 1.5 0 011.5-1.5 1.5 1.5 0 011.5 1.5 1.5 1.5 0 01-1.5 1.5z"
}
</script>

<template>
  <div class="bg-white rounded-xl shadow-sm p-6 border-l-4" :style="{ borderLeftColor: color }">
    <div class="flex items-start justify-between">
      <div class="flex-1">
        <p class="text-2xl font-bold text-gray-900">{{ value }}</p>
        <p class="text-sm font-medium text-gray-600 mt-1">{{ title }}</p>
      </div>
      <div class="flex-shrink-0 ml-4">
        <svg class="w-6 h-6 text-gray-400" fill="currentColor" viewBox="0 0 24 24">
          <path :d="iconPaths[icon]" />
        </svg>
      </div>
    </div>
  </div>
</template>