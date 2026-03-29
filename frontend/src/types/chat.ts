export type MessageDirection = 'in' | 'out'
export type MessageSource = 'telegram' | 'whatsapp' | 'manual'

export interface Message {
  id: number
  lead_id: number
  direction: MessageDirection
  content: string
  source: MessageSource
  is_from_agent: boolean
  created_at: string
}

export interface ChatPreview {
  lead_id: number
  lead_name: string
  lead_phone: string | null
  last_message: string | null
  last_message_time: string | null
  message_count: number
}

export interface MessageCreate {
  content: string
  direction: MessageDirection
  source?: MessageSource
  is_from_agent?: boolean
}

export interface Pagination {
  page: number
  size: number
  total: number
  pages: number
}

export interface MessageListResponse {
  items: Message[]
  pagination: Pagination
}

// Keep legacy Chat interface for backward compatibility
export interface Chat {
  lead_id: number
  lead_name: string
  last_message?: Message
  unread_count: number
}