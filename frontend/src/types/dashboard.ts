export interface DashboardStats {
  total_leads: number
  new_leads: number
  qualified_leads: number
  won_deals: number
  total_revenue: number
  conversion_rate: number
  monthly_revenue: number
  pending_appointments: number
  unread_messages: number
}

export interface RevenueChart {
  month: string
  revenue: number
}

export interface LeadsByStatus {
  status: string
  count: number
  percentage: number
}