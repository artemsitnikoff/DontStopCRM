<script setup lang="ts">
import { onMounted } from 'vue'
import AppButton from '@/components/ui/AppButton.vue'
import KanbanColumn from '@/components/domain/KanbanColumn.vue'
import { useLeads } from '@/composables/useLeads'
import type { LeadStatus } from '@/types/lead'
import { STATUS_LABELS, STATUS_COLORS } from '@/constants/leads'

const { leadsByStatus, loading, error, moveLeadStatus, fetchLeads } = useLeads()

onMounted(() => fetchLeads())

const columns = [
  { status: 'new' as LeadStatus, title: STATUS_LABELS.new, color: STATUS_COLORS.new },
  { status: 'contacted' as LeadStatus, title: STATUS_LABELS.contacted, color: STATUS_COLORS.contacted },
  { status: 'qualified' as LeadStatus, title: STATUS_LABELS.qualified, color: STATUS_COLORS.qualified },
  { status: 'won' as LeadStatus, title: STATUS_LABELS.won, color: STATUS_COLORS.won }
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