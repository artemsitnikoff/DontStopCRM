import { ref } from 'vue'
import type { ChatPreview, Message, MessageCreate, MessageDirection, MessageSource } from '@/types/chat'
import * as chatsApi from '@/api/chats'

export function useChat() {
  const chats = ref<ChatPreview[]>([])
  const selectedLeadId = ref<number | null>(null)
  const messages = ref<Message[]>([])
  const loading = ref(false)
  const sendingMessage = ref(false)
  const error = ref<string | null>(null)
  const wsConnected = ref(false)

  let ws: WebSocket | null = null

  // WebSocket URL construction
  const getWebSocketUrl = (leadId: number): string => {
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const baseUrl = import.meta.env.VITE_WS_URL
    const token = localStorage.getItem('access_token')

    let wsUrl: string
    if (baseUrl) {
      wsUrl = `${baseUrl}/api/v1/chats/ws/${leadId}`
    } else {
      // Construct from current location
      const host = window.location.host
      wsUrl = `${wsProtocol}//${host}/api/v1/chats/ws/${leadId}`
    }

    // Add token as query parameter
    return token ? `${wsUrl}?token=${token}` : wsUrl
  }

  const fetchChats = async () => {
    try {
      loading.value = true
      error.value = null
      const result = await chatsApi.getChats()
      chats.value = result
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Ошибка загрузки чатов'
    } finally {
      loading.value = false
    }
  }

  const selectChat = async (leadId: number) => {
    if (selectedLeadId.value === leadId) return

    // Disconnect previous WebSocket
    disconnectWebSocket()

    selectedLeadId.value = leadId
    await loadMessages(leadId)
    connectWebSocket(leadId)
  }

  const loadMessages = async (leadId: number, page = 1, size = 50) => {
    try {
      loading.value = true
      error.value = null
      const result = await chatsApi.getMessages(leadId, { page, size })

      // For simplicity, just replace all messages (in real app, you'd handle pagination)
      messages.value = [...result.items].reverse() // Reverse to show oldest first

      // Scrolling handled by component with proper ref
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Ошибка загрузки сообщений'
    } finally {
      loading.value = false
    }
  }

  const sendMessage = async (content: string, direction: MessageDirection = 'out', source: MessageSource = 'manual') => {
    if (!selectedLeadId.value || !content.trim()) return

    try {
      sendingMessage.value = true
      error.value = null

      const messageData: MessageCreate = {
        content: content.trim(),
        direction,
        source,
        is_from_agent: false
      }

      const newMessage = await chatsApi.sendMessage(selectedLeadId.value, messageData)

      // Add message to local state (WebSocket will also send it, but this ensures immediate feedback)
      if (!messages.value.find(m => m.id === newMessage.id)) {
        messages.value.push(newMessage)
      }

      // Update chat preview
      updateChatPreview(newMessage)

    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Ошибка отправки сообщения'
    } finally {
      sendingMessage.value = false
    }
  }

  const connectWebSocket = (leadId: number) => {
    try {
      const wsUrl = getWebSocketUrl(leadId)
      ws = new WebSocket(wsUrl)

      ws.onopen = () => {
        wsConnected.value = true
      }

      ws.onmessage = async (event) => {
        try {
          const payload = JSON.parse(event.data)
          if (payload.type === 'message') {
            const message = payload.data as Message

            // Add message if not already present
            if (!messages.value.find(m => m.id === message.id)) {
              messages.value.push(message)
            }

            // Update chat preview
            updateChatPreview(message)
          }
        } catch (err) {
          // Set error state for malformed WebSocket messages
          error.value = 'Ошибка обработки сообщения'
        }
      }

      ws.onerror = () => {
        wsConnected.value = false
      }

      ws.onclose = () => {
        wsConnected.value = false
      }
    } catch (err) {
      wsConnected.value = false
    }
  }

  const disconnectWebSocket = () => {
    if (ws) {
      ws.close()
      ws = null
    }
    wsConnected.value = false
  }

  const updateChatPreview = (message: Message) => {
    const chat = chats.value.find(c => c.lead_id === message.lead_id)
    if (chat) {
      chat.last_message = message.content
      chat.last_message_time = message.created_at
      chat.message_count += 1

      // Move chat to top of list
      const index = chats.value.indexOf(chat)
      chats.value.splice(index, 1)
      chats.value.unshift(chat)
    }
  }

  return {
    chats,
    selectedLeadId,
    messages,
    loading,
    sendingMessage,
    error,
    wsConnected,
    fetchChats,
    selectChat,
    sendMessage,
    connectWebSocket,
    disconnectWebSocket
  }
}