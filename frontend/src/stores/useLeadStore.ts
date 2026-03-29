import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Lead, LeadCreate, LeadUpdate, LeadStatus } from '@/types/lead'
import * as leadsApi from '@/api/leads'

export const useLeadStore = defineStore('leads', () => {
  const leads = ref<Lead[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const leadsByStatus = computed(() => {
    return leads.value.reduce((acc, lead) => {
      if (!acc[lead.status]) {
        acc[lead.status] = []
      }
      acc[lead.status].push(lead)
      return acc
    }, {} as Record<LeadStatus, Lead[]>)
  })

  const totalValue = computed(() => {
    return leads.value.reduce((sum, lead) => sum + (lead.value || 0), 0)
  })

  const fetchLeads = async () => {
    try {
      loading.value = true
      error.value = null
      leads.value = await leadsApi.getLeads()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Ошибка загрузки лидов'
    } finally {
      loading.value = false
    }
  }

  const addLead = async (leadData: LeadCreate): Promise<Lead | null> => {
    try {
      error.value = null
      const newLead = await leadsApi.createLead(leadData)
      leads.value.push(newLead)
      return newLead
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Ошибка создания лида'
      return null
    }
  }

  const updateLead = async (id: number, updates: LeadUpdate): Promise<Lead | null> => {
    try {
      error.value = null
      const updatedLead = await leadsApi.updateLead(id, updates)
      const index = leads.value.findIndex(lead => lead.id === id)
      if (index !== -1) {
        leads.value[index] = updatedLead
      }
      return updatedLead
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Ошибка обновления лида'
      return null
    }
  }

  const removeLead = async (id: number): Promise<boolean> => {
    try {
      error.value = null
      await leadsApi.deleteLead(id)
      const index = leads.value.findIndex(lead => lead.id === id)
      if (index !== -1) {
        leads.value.splice(index, 1)
      }
      return true
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Ошибка удаления лида'
      return false
    }
  }

  const getLeadById = (id: number): Lead | undefined => {
    return leads.value.find(lead => lead.id === id)
  }

  return {
    leads,
    loading,
    error,
    leadsByStatus,
    totalValue,
    fetchLeads,
    addLead,
    updateLead,
    removeLead,
    getLeadById,
  }
})