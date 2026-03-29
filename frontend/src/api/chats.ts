import apiClient from './client'
import type { Message, Chat, ChatPreview, MessageListResponse, MessageCreate } from '@/types/chat'

// New API functions matching backend
export const getChats = async (): Promise<ChatPreview[]> => {
  const { data } = await apiClient.get<ChatPreview[]>('/chats/')
  return data
}

export const getMessages = async (leadId: number, params?: { page?: number, size?: number }): Promise<MessageListResponse> => {
  const { data } = await apiClient.get<MessageListResponse>(`/chats/${leadId}/messages`, { params })
  return data
}

export const sendMessage = async (leadId: number, data: MessageCreate): Promise<Message> => {
  const response = await apiClient.post<Message>(`/chats/${leadId}/messages`, data)
  return response.data
}

// Legacy functions for backward compatibility
export const getChatsLegacy = async (): Promise<Chat[]> => {
  const { data } = await apiClient.get<Chat[]>('/chats/legacy')
  return data
}

export const getMessagesLegacy = async (leadId: number): Promise<Message[]> => {
  const { data } = await apiClient.get<Message[]>(`/chats/${leadId}/messages/legacy`)
  return data
}

export const sendMessageLegacy = async (leadId: number, content: string): Promise<Message> => {
  const { data } = await apiClient.post<Message>(`/chats/${leadId}/messages/legacy`, {
    content,
  })
  return data
}

export const markAsRead = async (messageId: number): Promise<void> => {
  await apiClient.patch(`/chats/messages/${messageId}/read`)
}

export const markChatAsRead = async (leadId: number): Promise<void> => {
  await apiClient.patch(`/chats/${leadId}/read`)
}