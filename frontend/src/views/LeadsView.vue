<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useLeadStore } from '@/stores/useLeadStore'
import AppButton from '@/components/ui/AppButton.vue'
import AppBadge from '@/components/ui/AppBadge.vue'
import { LeadStatus } from '@/types/lead'

const leadStore = useLeadStore()

const statusLabels = {
  [LeadStatus.New]: 'Новый',
  [LeadStatus.Contacted]: 'Связались',
  [LeadStatus.Qualified]: 'Квалифицирован',
  [LeadStatus.Proposal]: 'Предложение',
  [LeadStatus.Won]: 'Выигран',
  [LeadStatus.Lost]: 'Проигран'
}

const statusVariants = {
  [LeadStatus.New]: 'default',
  [LeadStatus.Contacted]: 'primary',
  [LeadStatus.Qualified]: 'warning',
  [LeadStatus.Proposal]: 'primary',
  [LeadStatus.Won]: 'success',
  [LeadStatus.Lost]: 'danger'
} as const

const columns = computed(() => {
  const statusKeys = Object.values(LeadStatus)
  return statusKeys.map(status => ({
    id: status,
    title: statusLabels[status],
    leads: leadStore.leadsByStatus[status] || []
  }))
})

onMounted(() => {
  leadStore.fetchLeads()
})
</script>

<template>
  <div class="p-6">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-semibold text-text">Лиды</h1>
        <p class="text-text-secondary mt-1">Управление воронкой продаж</p>
      </div>
      <AppButton variant="primary">
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        Добавить лид
      </AppButton>
    </div>

    <!-- Loading State -->
    <div v-if="leadStore.loading" class="flex items-center justify-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-accent"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="leadStore.error" class="bg-danger bg-opacity-10 border border-red-300 text-red-700 px-4 py-3 rounded-md">
      {{ leadStore.error }}
    </div>

    <!-- Kanban Board -->
    <div v-else class="flex gap-6 overflow-x-auto pb-6">
      <div
        v-for="column in columns"
        :key="column.id"
        class="flex-shrink-0 w-80"
      >
        <div class="bg-gray-50 rounded-lg p-4">
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-medium text-text">{{ column.title }}</h3>
            <span class="bg-gray-200 text-gray-700 text-xs font-medium px-2.5 py-0.5 rounded-full">
              {{ column.leads.length }}
            </span>
          </div>

          <div class="space-y-3">
            <div
              v-for="lead in column.leads"
              :key="lead.id"
              class="card p-4 cursor-pointer hover:shadow-md transition-shadow"
            >
              <div class="flex items-start justify-between mb-2">
                <h4 class="font-medium text-text truncate">{{ lead.name }}</h4>
                <AppBadge :variant="statusVariants[lead.status]" size="sm">
                  {{ statusLabels[lead.status] }}
                </AppBadge>
              </div>

              <div class="space-y-1 text-sm text-text-secondary">
                <div v-if="lead.email" class="flex items-center">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                  </svg>
                  {{ lead.email }}
                </div>

                <div v-if="lead.phone" class="flex items-center">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                  {{ lead.phone }}
                </div>

                <div v-if="lead.value" class="flex items-center font-medium text-success">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                  </svg>
                  ₽{{ lead.value.toLocaleString() }}
                </div>

                <div v-if="lead.notes" class="text-xs mt-2 p-2 bg-gray-50 rounded">
                  {{ lead.notes }}
                </div>
              </div>

              <div class="mt-3 text-xs text-text-secondary">
                {{ new Date(lead.created_at).toLocaleDateString('ru-RU') }}
              </div>
            </div>

            <!-- Empty State for Column -->
            <div v-if="column.leads.length === 0" class="text-center py-8">
              <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
              </svg>
              <p class="mt-2 text-sm text-gray-500">Нет лидов</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Summary -->
    <div v-if="!leadStore.loading && !leadStore.error" class="mt-6 bg-white rounded-lg p-6 border border-gray-200">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-lg font-medium text-text">Общая статистика</h3>
          <p class="text-text-secondary">Всего лидов: {{ leadStore.leads.length }}</p>
        </div>
        <div class="text-right">
          <p class="text-2xl font-semibold text-success">
            ₽{{ leadStore.totalValue.toLocaleString() }}
          </p>
          <p class="text-text-secondary">Общая стоимость</p>
        </div>
      </div>
    </div>
  </div>
</template>