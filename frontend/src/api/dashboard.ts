import apiClient from './client'
import type { DashboardStats, RevenueChart, LeadsByStatus } from '@/types/dashboard'

export const getStats = async (): Promise<DashboardStats> => {
  const { data } = await apiClient.get<DashboardStats>('/dashboard/stats')
  return data
}

export const getRevenueChart = async (period: 'month' | 'year' = 'month'): Promise<RevenueChart[]> => {
  const { data } = await apiClient.get<RevenueChart[]>(`/dashboard/revenue?period=${period}`)
  return data
}

export const getLeadsByStatus = async (): Promise<LeadsByStatus[]> => {
  const { data } = await apiClient.get<LeadsByStatus[]>('/dashboard/leads-by-status')
  return data
}