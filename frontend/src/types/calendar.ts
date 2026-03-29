export type EventType = 'booking' | 'task' | 'follow_up'
export type EventStatus = 'planned' | 'done' | 'cancelled'

export interface CalendarEvent {
  id: number
  title: string
  description: string | null
  start_at: string
  end_at: string
  lead_id: number | null
  event_type: EventType
  status: EventStatus
  created_at: string
  updated_at: string
}

export interface EventCreate {
  title: string
  description?: string
  start_at: string
  end_at: string
  lead_id?: number | null
  event_type?: EventType
  status?: EventStatus
}

export interface EventUpdate {
  title?: string
  description?: string
  start_at?: string
  end_at?: string
  lead_id?: number | null
  event_type?: EventType
  status?: EventStatus
}

export interface EventStatusUpdate {
  status: EventStatus
}