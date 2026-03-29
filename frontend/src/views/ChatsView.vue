<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import ChatListItem from '@/components/domain/ChatListItem.vue'
import MessageBubble from '@/components/domain/MessageBubble.vue'
import ChatInput from '@/components/domain/ChatInput.vue'
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

// Group messages by date
const groupedMessages = computed(() => {
  const groups: { [key: string]: typeof messages.value } = {}

  messages.value.forEach(message => {
    const date = new Date(message.created_at)
    const today = new Date()
    const yesterday = new Date(today)
    yesterday.setDate(yesterday.getDate() - 1)

    let dateKey: string

    if (date.toDateString() === today.toDateString()) {
      dateKey = 'Сегодня'
    } else if (date.toDateString() === yesterday.toDateString()) {
      dateKey = 'Вчера'
    } else {
      dateKey = date.toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'long',
        year: date.getFullYear() !== today.getFullYear() ? 'numeric' : undefined
      })
    }

    if (!groups[dateKey]) {
      groups[dateKey] = []
    }
    groups[dateKey].push(message)
  })

  return groups
})

const handleSelectChat = (leadId: number) => {
  selectChat(leadId)
}

const handleSendMessage = (content: string) => {
  sendMessage(content, 'out', 'manual')
}

const handleConnectAgent = () => {
  // TODO: Implement agent connection
  console.log('Connect agent requested')
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
      <div v-if="selectedChat" class="flex flex-col h-full">
        <!-- Chat Header -->
        <div class="p-4 bg-white border-b border-gray-200">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <!-- Avatar -->
              <div
                class="w-10 h-10 rounded-full bg-blue-500 text-white flex items-center justify-center font-semibold"
              >
                {{ selectedChat.lead_name.charAt(0).toUpperCase() }}
              </div>

              <div>
                <h3 class="font-semibold text-gray-900">
                  {{ selectedChat.lead_name }}
                </h3>
                <div class="flex items-center gap-2 text-sm text-gray-500">
                  <span v-if="selectedChat.lead_phone">{{ selectedChat.lead_phone }}</span>
                  <!-- Source badge could be added here -->
                </div>
              </div>
            </div>

            <!-- Action buttons -->
            <div class="flex gap-2">
              <button class="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100 transition-colors">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                </svg>
              </button>
              <button class="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100 transition-colors">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h.01M12 12h.01M19 12h.01M6 2v20M18 2v20" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Messages Area -->
        <div class="flex-1 overflow-y-auto p-4 messages-container" style="scroll-behavior: smooth;">
          <div v-if="loading && !messages.length" class="flex items-center justify-center h-64">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
          </div>

          <div v-else-if="error" class="text-center text-red-600 py-8">
            {{ error }}
          </div>

          <div v-else>
            <!-- Messages grouped by date -->
            <div v-for="(dateMessages, date) in groupedMessages" :key="date">
              <!-- Date separator -->
              <div class="flex items-center justify-center my-6">
                <div class="bg-white rounded-full px-3 py-1 text-xs text-gray-500 shadow-sm border">
                  {{ date }}
                </div>
              </div>

              <!-- Messages for this date -->
              <div v-for="message in dateMessages" :key="message.id">
                <MessageBubble :message="message" />
              </div>
            </div>

            <!-- Empty state -->
            <div v-if="!messages.length && !loading" class="flex items-center justify-center h-64">
              <div class="text-center">
                <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
                <h3 class="text-lg font-medium text-gray-900 mb-2">Начните общение</h3>
                <p class="text-gray-500">Отправьте первое сообщение для начала диалога</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Chat Input -->
        <ChatInput
          :disabled="sendingMessage"
          @send="handleSendMessage"
          @connect-agent="handleConnectAgent"
        />
      </div>

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

<style scoped>
/* Ensure smooth scrolling */
.messages-container {
  scroll-behavior: smooth;
}

/* Custom scrollbar for messages */
.messages-container::-webkit-scrollbar {
  width: 6px;
}

.messages-container::-webkit-scrollbar-track {
  background: transparent;
}

.messages-container::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}
</style>