export type LeadStatus = 'new' | 'contacted' | 'qualified' | 'won'
export type LeadSource = 'telegram' | 'whatsapp' | 'instagram' | 'phone'

export interface Lead {
  id: number
  name: string
  phone: string | null
  source: LeadSource
  status: LeadStatus
  first_message: string | null
  created_at: string
  updated_at: string
}

export interface LeadCreate {
  name: string
  phone?: string
  source?: LeadSource
  first_message?: string
}

export interface LeadUpdate {
  name?: string
  phone?: string
  source?: LeadSource
  status?: LeadStatus
  first_message?: string
}

export interface LeadListResponse {
  items: Lead[]
  total: number
  page: number
  size: number
}