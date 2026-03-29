import type { DashboardStats } from '@/types/dashboard'
import apiClient from './client'

export async function getDashboardStats(): Promise<DashboardStats> {
  const { data } = await apiClient.get<DashboardStats>('/dashboard/stats')
  return data
}