import apiClient from './client'
import type { CalendarEvent, EventCreate, EventUpdate, EventStatus } from '@/types/calendar'
import type { Pagination } from '@/types/lead'

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
  const { data } = await apiClient.get<EventsResponse>('/events/', { params })
  return data
}

export const getEvent = async (id: number): Promise<CalendarEvent> => {
  const { data } = await apiClient.get<CalendarEvent>(`/events/${id}`)
  return data
}

export const createEvent = async (data: EventCreate): Promise<CalendarEvent> => {
  const { data: response } = await apiClient.post<CalendarEvent>('/events/', data)
  return response
}

export const updateEvent = async (id: number, data: EventUpdate): Promise<CalendarEvent> => {
  const { data: response } = await apiClient.patch<CalendarEvent>(`/events/${id}`, data)
  return response
}

export const updateEventStatus = async (id: number, status: EventStatus): Promise<CalendarEvent> => {
  const { data } = await apiClient.patch<CalendarEvent>(`/events/${id}/status`, { status })
  return data
}

export const deleteEvent = async (id: number): Promise<void> => {
  await apiClient.delete(`/events/${id}`)
}