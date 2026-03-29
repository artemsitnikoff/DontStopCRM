import apiClient from './client'
import type { Appointment, AppointmentCreate, AppointmentUpdate } from '@/types/calendar'

export const getAppointments = async (start?: string, end?: string): Promise<Appointment[]> => {
  const params = new URLSearchParams()
  if (start) params.append('start', start)
  if (end) params.append('end', end)

  const { data } = await apiClient.get<Appointment[]>(`/appointments/?${params}`)
  return data
}

export const getAppointment = async (id: number): Promise<Appointment> => {
  const { data } = await apiClient.get<Appointment>(`/appointments/${id}`)
  return data
}

export const createAppointment = async (appointmentData: AppointmentCreate): Promise<Appointment> => {
  const { data } = await apiClient.post<Appointment>('/appointments/', appointmentData)
  return data
}

export const updateAppointment = async (id: number, updates: AppointmentUpdate): Promise<Appointment> => {
  const { data } = await apiClient.put<Appointment>(`/appointments/${id}`, updates)
  return data
}

export const deleteAppointment = async (id: number): Promise<void> => {
  await apiClient.delete(`/appointments/${id}`)
}