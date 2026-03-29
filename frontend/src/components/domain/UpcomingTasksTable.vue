<script setup lang="ts">
import type { UpcomingTask } from '@/types/dashboard'

const props = defineProps<{
  tasks: UpcomingTask[]
}>()

const eventTypeLabels: Record<string, { label: string; color: string }> = {
  booking: { label: 'Запись', color: 'bg-blue-100 text-blue-800' },
  task: { label: 'Задача', color: 'bg-green-100 text-green-800' },
  follow_up: { label: 'Напоминание', color: 'bg-orange-100 text-orange-800' }
}

const formatTime = (dateTime: string) => {
  return new Date(dateTime).toLocaleTimeString('ru-RU', {
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<template>
  <div class="overflow-x-auto">
    <table v-if="tasks.length > 0" class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Время
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Задача
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Тип
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Лид
          </th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-for="task in tasks" :key="task.id" class="hover:bg-gray-50 transition-colors">
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
            {{ formatTime(task.start_at) }}
          </td>
          <td class="px-6 py-4 text-sm text-gray-900">
            <div class="font-medium">{{ task.title }}</div>
          </td>
          <td class="px-6 py-4 whitespace-nowrap">
            <span
              class="inline-flex px-2 py-1 text-xs font-semibold rounded-full"
              :class="eventTypeLabels[task.event_type]?.color || 'bg-gray-100 text-gray-800'"
            >
              {{ eventTypeLabels[task.event_type]?.label || task.event_type }}
            </span>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
            {{ task.lead_name || '—' }}
          </td>
        </tr>
      </tbody>
    </table>
    <div v-else class="text-center py-8">
      <div class="text-gray-500">
        <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
        </svg>
        <p class="text-lg font-medium">Нет предстоящих задач</p>
      </div>
    </div>
  </div>
</template>