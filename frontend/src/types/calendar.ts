export enum AppointmentType {
  Call = 'call',
  Meeting = 'meeting',
  Demo = 'demo',
  Followup = 'followup'
}

export interface Appointment {
  id: number
  title: string
  description?: string
  type: AppointmentType
  start_time: string
  end_time: string
  lead_id?: number
  lead_name?: string
  location?: string
  created_at: string
  updated_at: string
}

export interface AppointmentCreate {
  title: string
  description?: string
  type: AppointmentType
  start_time: string
  end_time: string
  lead_id?: number
  location?: string
}

export interface AppointmentUpdate {
  title?: string
  description?: string
  type?: AppointmentType
  start_time?: string
  end_time?: string
  location?: string
}