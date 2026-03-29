import apiClient from './client'
import type { Lead, LeadCreate, LeadUpdate } from '@/types/lead'

export const getLeads = async (): Promise<Lead[]> => {
  const { data } = await apiClient.get<Lead[]>('/leads/')
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

export const deleteLead = async (id: number): Promise<void> => {
  await apiClient.delete(`/leads/${id}`)
}