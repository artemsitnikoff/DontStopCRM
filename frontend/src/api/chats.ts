import apiClient from './client'
import type { Message, ChatPreview, MessageListResponse, MessageCreate } from '@/types/chat'

export const getChats = async (): Promise<ChatPreview[]> => {
  const { data } = await apiClient.get<{ items: ChatPreview[] }>('/chats/')
  return data.items
}

export const getMessages = async (leadId: number, params?: { page?: number, size?: number }): Promise<MessageListResponse> => {
  const { data } = await apiClient.get<MessageListResponse>(`/chats/${leadId}/messages`, { params })
  return data
}

export const sendMessage = async (leadId: number, data: MessageCreate): Promise<Message> => {
  const response = await apiClient.post<Message>(`/chats/${leadId}/messages`, data)
  return response.data
}