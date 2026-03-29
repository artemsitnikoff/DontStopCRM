export enum SenderType {
  User = 'user',
  Lead = 'lead',
  System = 'system'
}

export interface Message {
  id: number
  lead_id: number
  sender_type: SenderType
  sender_name: string
  content: string
  is_read: boolean
  created_at: string
}

export interface Chat {
  lead_id: number
  lead_name: string
  last_message?: Message
  unread_count: number
}