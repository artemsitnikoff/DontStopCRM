export interface StatusCount {
  status: string
  count: number
}

export interface SourceCount {
  source: string
  count: number
}

export interface UpcomingTask {
  id: number
  title: string
  start_at: string
  end_at: string
  event_type: string
  lead_id: number | null
  lead_name: string | null
}

export interface DashboardStats {
  total_leads: number
  leads_by_status: StatusCount[]
  leads_by_source: SourceCount[]
  upcoming_tasks: UpcomingTask[]
  today_bookings: number
  conversion_rate: number
}