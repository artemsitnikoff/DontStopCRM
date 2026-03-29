import apiClient from './client'
import type { Message, Chat } from '@/types/chat'

export const getChats = async (): Promise<Chat[]> => {
  const { data } = await apiClient.get<Chat[]>('/chats/')
  return data
}

export const getMessages = async (leadId: number): Promise<Message[]> => {
  const { data } = await apiClient.get<Message[]>(`/chats/${leadId}/messages`)
  return data
}

export const sendMessage = async (leadId: number, content: string): Promise<Message> => {
  const { data } = await apiClient.post<Message>(`/chats/${leadId}/messages`, {
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