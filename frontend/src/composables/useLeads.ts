import { ref, computed } from 'vue'
import type { Lead, LeadStatus } from '@/types/lead'
import * as leadsApi from '@/api/leads'

const KANBAN_PAGE_SIZE = 1000

export function useLeads() {
  const leads = ref<Lead[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Group leads by status
  const leadsByStatus = computed(() => {
    const groups = {
      new: [] as Lead[],
      contacted: [] as Lead[],
      qualified: [] as Lead[],
      won: [] as Lead[]
    }

    leads.value.forEach(lead => {
      if (groups[lead.status]) {
        groups[lead.status].push(lead)
      }
    })

    return groups
  })

  const fetchLeads = async () => {
    try {
      loading.value = true
      error.value = null
      // Fetch all leads without status filter for kanban view with large size
      const response = await leadsApi.getLeads({ size: KANBAN_PAGE_SIZE })
      leads.value = response.items
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Ошибка загрузки лидов'
    } finally {
      loading.value = false
    }
  }

  const moveLeadStatus = async (leadId: number, newStatus: LeadStatus) => {
    // Find the lead
    const lead = leads.value.find(l => l.id === leadId)
    if (!lead) return

    // Store old status for rollback
    const oldStatus = lead.status

    try {
      // Optimistic update
      lead.status = newStatus

      // API call
      await leadsApi.updateLeadStatus(leadId, newStatus)
    } catch (err) {
      // Rollback on error
      lead.status = oldStatus
      error.value = err instanceof Error ? err.message : 'Ошибка обновления статуса лида'
    }
  }

  return {
    leads,
    loading,
    error,
    leadsByStatus,
    fetchLeads,
    moveLeadStatus
  }
}