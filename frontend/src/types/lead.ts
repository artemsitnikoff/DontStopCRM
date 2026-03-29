export enum LeadStatus {
  New = 'new',
  Contacted = 'contacted',
  Qualified = 'qualified',
  Proposal = 'proposal',
  Won = 'won',
  Lost = 'lost'
}

export interface Lead {
  id: number
  name: string
  email?: string
  phone?: string
  status: LeadStatus
  value?: number
  notes?: string
  source?: string
  assigned_to?: number
  created_at: string
  updated_at: string
}

export interface LeadCreate {
  name: string
  email?: string
  phone?: string
  status?: LeadStatus
  value?: number
  notes?: string
  source?: string
}

export interface LeadUpdate {
  name?: string
  email?: string
  phone?: string
  status?: LeadStatus
  value?: number
  notes?: string
  assigned_to?: number
}