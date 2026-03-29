<script setup lang="ts">
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import MessageBubble from '@/components/domain/MessageBubble.vue'
import ChatInput from '@/components/domain/ChatInput.vue'
import type { Message } from '@/types/chat'

interface Props {
  leadId: number
  leadName: string
  leadPhone: string | null
  messages: Message[]
  sending: boolean
}

interface Emits {
  send: [content: string]
  connectAgent: []
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const messagesContainer = ref<HTMLElement | null>(null)

// Group messages by date
const groupedMessages = computed(() => {
  const groups: { [key: string]: Message[] } = {}

  props.messages.forEach(message => {
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

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const handleSendMessage = (content: string) => {
  emit('send', content)
  nextTick(() => scrollToBottom())
}

const handleConnectAgent = () => {
  emit('connectAgent')
}

// Scroll to bottom when messages change
watch(() => props.messages.length, () => {
  nextTick(() => scrollToBottom())
})

onMounted(() => {
  scrollToBottom()
})
</script>

<template>
  <div class="flex flex-col h-full">
    <!-- Chat Header -->
    <div class="p-4 bg-white border-b border-gray-200">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <!-- Avatar -->
          <div
            class="w-10 h-10 rounded-full bg-blue-500 text-white flex items-center justify-center font-semibold"
          >
            {{ leadName.charAt(0).toUpperCase() }}
          </div>

          <div>
            <h3 class="font-semibold text-gray-900">
              {{ leadName }}
            </h3>
            <div class="flex items-center gap-2 text-sm text-gray-500">
              <span v-if="leadPhone">{{ leadPhone }}</span>
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
    <div
      ref="messagesContainer"
      class="flex-1 overflow-y-auto p-4 messages-container"
      style="scroll-behavior: smooth;"
    >
      <div v-if="!messages.length" class="flex items-center justify-center h-64">
        <div class="text-center">
          <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          <h3 class="text-lg font-medium text-gray-900 mb-2">Начните общение</h3>
          <p class="text-gray-500">Отправьте первое сообщение для начала диалога</p>
        </div>
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
      </div>
    </div>

    <!-- Chat Input -->
    <ChatInput
      :disabled="sending"
      @send="handleSendMessage"
      @connect-agent="handleConnectAgent"
    />
  </div>
</template>

<style scoped>
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