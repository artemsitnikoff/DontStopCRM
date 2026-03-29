<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import ChatListItem from '@/components/domain/ChatListItem.vue'
import ChatContent from '@/components/domain/ChatContent.vue'
import { useChat } from '@/composables/useChat'

const {
  chats,
  selectedLeadId,
  messages,
  loading,
  sendingMessage,
  error,
  fetchChats,
  selectChat,
  sendMessage,
  disconnectWebSocket
} = useChat()

const searchQuery = ref('')

// Filter chats by search query
const filteredChats = computed(() => {
  if (!searchQuery.value.trim()) return chats.value

  const query = searchQuery.value.toLowerCase()
  return chats.value.filter(chat =>
    chat.lead_name.toLowerCase().includes(query) ||
    (chat.lead_phone && chat.lead_phone.includes(query)) ||
    (chat.last_message && chat.last_message.toLowerCase().includes(query))
  )
})

// Get selected chat info
const selectedChat = computed(() => {
  if (!selectedLeadId.value) return null
  return chats.value.find(chat => chat.lead_id === selectedLeadId.value)
})

const handleSelectChat = (leadId: number) => {
  selectChat(leadId)
}

const handleSendMessage = (content: string) => {
  sendMessage(content, 'out', 'manual')
}

const handleConnectAgent = () => {
  // TODO: Implement agent connection
}

// Load chats on mount
onMounted(() => {
  fetchChats()
})

// Cleanup WebSocket on unmount
onUnmounted(() => {
  disconnectWebSocket()
})
</script>

<template>
  <div class="h-screen flex overflow-hidden">
    <!-- Left Panel - Chat List -->
    <div class="w-80 bg-white border-r border-gray-200 flex flex-col">
      <!-- Search Header -->
      <div class="p-4 border-b border-gray-100">
        <div class="relative">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Поиск чатов..."
            class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
      </div>

      <!-- Chat List -->
      <div class="flex-1 overflow-y-auto">
        <!-- Loading -->
        <div v-if="loading" class="flex items-center justify-center h-32">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        </div>

        <!-- Error -->
        <div v-else-if="error" class="p-4 text-center text-red-600">
          {{ error }}
        </div>

        <!-- Chat List -->
        <div v-else-if="filteredChats.length > 0">
          <ChatListItem
            v-for="chat in filteredChats"
            :key="chat.lead_id"
            :chat="chat"
            :active="selectedLeadId === chat.lead_id"
            @select="handleSelectChat"
          />
        </div>

        <!-- Empty State -->
        <div v-else class="flex flex-col items-center justify-center h-64 text-center p-4">
          <svg class="w-16 h-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          <h3 class="text-lg font-medium text-gray-900 mb-2">Нет чатов</h3>
          <p class="text-gray-500">
            {{ searchQuery ? 'Ничего не найдено' : 'Диалоги появятся, когда клиенты начнут писать' }}
          </p>
        </div>
      </div>
    </div>

    <!-- Right Panel - Chat Content -->
    <div class="flex-1 flex flex-col" style="background-color: var(--color-bg);">
      <div v-if="loading && !messages.length" class="flex items-center justify-center h-64">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>

      <div v-else-if="error" class="flex items-center justify-center h-64 text-center text-red-600">
        {{ error }}
      </div>

      <ChatContent
        v-else-if="selectedChat"
        :lead-id="selectedChat.lead_id"
        :lead-name="selectedChat.lead_name"
        :lead-phone="selectedChat.lead_phone"
        :messages="messages"
        :sending="sendingMessage"
        @send="handleSendMessage"
        @connect-agent="handleConnectAgent"
      />

      <!-- No Chat Selected -->
      <div v-else class="flex-1 flex items-center justify-center">
        <div class="text-center">
          <svg class="w-24 h-24 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          <h3 class="text-xl font-medium text-gray-900 mb-2">Выберите чат</h3>
          <p class="text-gray-500">Выберите диалог из списка слева для начала общения</p>
        </div>
      </div>
    </div>
  </div>
</template>