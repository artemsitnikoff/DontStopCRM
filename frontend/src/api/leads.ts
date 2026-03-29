import apiClient from './client'
import type { Lead, LeadCreate, LeadUpdate, LeadListResponse, LeadStatus, LeadSource } from '@/types/lead'

export const getLeads = async (params?: {
  status?: LeadStatus
  source?: LeadSource
  page?: number
  size?: number
}): Promise<LeadListResponse> => {
  const { data } = await apiClient.get<LeadListResponse>('/leads/', { params })
  return data
}

export const getLead = async (id: number): Promise<Lead> => {
  const { data } = await apiClient.get<Lead>(`/leads/${id}`)
  return data
}

export const createLead = async (leadData: LeadCreate): Promise<Lead> => {
  const { data } = await apiClient.post<Lead>('/leads/', leadData)
  return data
}

export const updateLead = async (id: number, updates: LeadUpdate): Promise<Lead> => {
  const { data } = await apiClient.put<Lead>(`/leads/${id}`, updates)
  return data
}

export const updateLeadStatus = async (id: number, status: LeadStatus): Promise<Lead> => {
  const { data } = await apiClient.patch<Lead>(`/leads/${id}/status`, { status })
  return data
}

export const deleteLead = async (id: number): Promise<void> => {
  await apiClient.delete(`/leads/${id}`)
}