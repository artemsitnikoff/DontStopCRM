<script setup lang="ts">
import AppButton from '@/components/ui/AppButton.vue'
import KanbanColumn from '@/components/domain/KanbanColumn.vue'
import { useLeads } from '@/composables/useLeads'
import type { LeadStatus } from '@/types/lead'

const { leadsByStatus, loading, error, moveLeadStatus } = useLeads()

const statusLabels = {
  new: 'Новый',
  contacted: 'Контакт',
  qualified: 'Квалифицирован',
  won: 'Выигран'
}

const statusColors = {
  new: '#1929bb',
  contacted: '#e6a23c',
  qualified: '#6C5CE7',
  won: '#017d0d'
}

const columns = [
  { status: 'new' as LeadStatus, title: statusLabels.new, color: statusColors.new },
  { status: 'contacted' as LeadStatus, title: statusLabels.contacted, color: statusColors.contacted },
  { status: 'qualified' as LeadStatus, title: statusLabels.qualified, color: statusColors.qualified },
  { status: 'won' as LeadStatus, title: statusLabels.won, color: statusColors.won }
]

const handleLeadMoved = async (leadId: number, newStatus: LeadStatus) => {
  await moveLeadStatus(leadId, newStatus)
}
</script>

<template>
  <div class="p-6">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-semibold text-black">Лиды</h1>
        <p class="text-gray-600 mt-1">Управление воронкой продаж</p>
      </div>
      <AppButton variant="primary">
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        Добавить лида
      </AppButton>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-red-500"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-300 text-red-700 px-4 py-3 rounded-md">
      {{ error }}
    </div>

    <!-- Kanban Board -->
    <div v-else class="flex gap-6 overflow-x-auto pb-6">
      <KanbanColumn
        v-for="column in columns"
        :key="column.status"
        :title="column.title"
        :status="column.status"
        :color="column.color"
        :leads="leadsByStatus[column.status] || []"
        @lead-moved="handleLeadMoved"
      />
    </div>
  </div>
</template>