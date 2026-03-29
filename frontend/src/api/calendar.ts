import apiClient from './client'
import type { CalendarEvent, EventCreate, EventUpdate, EventStatus } from '@/types/calendar'
import type { Pagination } from '@/types/common'

interface EventsResponse {
  items: CalendarEvent[]
  pagination: Pagination
}

export const getEvents = async (params: {
  start?: string
  end?: string
  lead_id?: number
  event_type?: string
  status?: string
  page?: number
  size?: number
} = {}): Promise<EventsResponse> => {
  const { data } = await apiClient.get<EventsResponse>('/calendar/', { params })
  return data
}

export const getEvent = async (id: number): Promise<CalendarEvent> => {
  const { data } = await apiClient.get<CalendarEvent>(`/calendar/${id}`)
  return data
}

export const createEvent = async (data: EventCreate): Promise<CalendarEvent> => {
  const { data: response } = await apiClient.post<CalendarEvent>('/calendar/', data)
  return response
}

export const updateEvent = async (id: number, data: EventUpdate): Promise<CalendarEvent> => {
  const { data: response } = await apiClient.patch<CalendarEvent>(`/calendar/${id}`, data)
  return response
}

export const updateEventStatus = async (id: number, status: EventStatus): Promise<CalendarEvent> => {
  const { data } = await apiClient.patch<CalendarEvent>(`/calendar/${id}/status`, { status })
  return data
}

export const deleteEvent = async (id: number): Promise<void> => {
  await apiClient.delete(`/calendar/${id}`)
}