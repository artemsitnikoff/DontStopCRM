<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AppBadge from '@/components/ui/AppBadge.vue'
import AppInput from '@/components/ui/AppInput.vue'
import AppButton from '@/components/ui/AppButton.vue'
import { useApi } from '@/composables/useApi'
import { getChats } from '@/api/chats'
import { formatRelativeTime } from '@/utils/formatDate'
import type { Chat } from '@/types/chat'

const { data: chats, loading, error, execute } = useApi<Chat[]>()
const selectedChatId = ref<number | null>(null)
const messageText = ref('')

onMounted(() => {
  execute(getChats)
})

const selectChat = (leadId: number) => {
  selectedChatId.value = leadId
}

const sendMessage = () => {
  if (!messageText.value.trim()) return

  // TODO: Implement send message
  messageText.value = ''
}
</script>

<template>
  <div class="p-6">
    <div class="mb-6">
      <h1 class="text-2xl font-semibold text-text">Чаты</h1>
      <p class="text-text-secondary mt-1">Общение с клиентами</p>
    </div>

    <div class="flex h-[calc(100vh-200px)] gap-6">
      <!-- Chat List -->
      <div class="w-80 card overflow-hidden flex flex-col">
        <div class="p-4 border-b">
          <h3 class="font-medium text-text">Диалоги</h3>
        </div>

        <div class="flex-1 overflow-y-auto">
          <!-- Loading -->
          <div v-if="loading" class="flex items-center justify-center h-32">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-accent"></div>
          </div>

          <!-- Error -->
          <div v-else-if="error" class="p-4 text-center text-danger">
            {{ error }}
          </div>

          <!-- Chat List -->
          <div v-else-if="chats && chats.length > 0" class="divide-y">
            <div
              v-for="chat in chats"
              :key="chat.lead_id"
              @click="selectChat(chat.lead_id)"
              class="p-4 hover:bg-gray-50 cursor-pointer transition-colors"
              :class="{
                'bg-accent bg-opacity-5 border-r-2 border-accent': selectedChatId === chat.lead_id
              }"
            >
              <div class="flex items-center justify-between mb-1">
                <h4 class="font-medium text-text truncate">{{ chat.lead_name }}</h4>
                <AppBadge v-if="chat.unread_count > 0" variant="danger" size="sm">
                  {{ chat.unread_count }}
                </AppBadge>
              </div>

              <div v-if="chat.last_message" class="text-sm">
                <p class="text-text-secondary truncate">
                  {{ chat.last_message.content }}
                </p>
                <p class="text-xs text-text-secondary mt-1">
                  {{ formatRelativeTime(chat.last_message.created_at) }}
                </p>
              </div>

              <div v-else class="text-sm text-text-secondary">
                Нет сообщений
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-else class="flex flex-col items-center justify-center h-64 text-center">
            <svg class="w-16 h-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            <h3 class="text-lg font-medium text-text mb-2">Нет активных чатов</h3>
            <p class="text-text-secondary">Диалоги появятся, когда клиенты начнут писать</p>
          </div>
        </div>
      </div>

      <!-- Chat Content -->
      <div class="flex-1 card flex flex-col">
        <div v-if="selectedChatId" class="flex flex-col h-full">
          <!-- Chat Header -->
          <div class="p-4 border-b bg-gray-50">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="font-medium text-text">
                  {{ chats?.find(c => c.lead_id === selectedChatId)?.lead_name }}
                </h3>
                <p class="text-sm text-text-secondary">Онлайн</p>
              </div>

              <div class="flex gap-2">
                <button class="p-2 text-text-secondary hover:text-text rounded-lg hover:bg-white transition-colors">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                </button>
                <button class="p-2 text-text-secondary hover:text-text rounded-lg hover:bg-white transition-colors">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Messages Area -->
          <div class="flex-1 p-4 overflow-y-auto bg-gray-50">
            <div class="text-center text-text-secondary">
              <p>История сообщений будет загружаться здесь</p>
              <p class="text-sm mt-2">Выбран чат с ID: {{ selectedChatId }}</p>
            </div>
          </div>

          <!-- Message Input -->
          <div class="p-4 border-t bg-white">
            <div class="flex gap-3">
              <div class="flex-1">
                <AppInput
                  v-model="messageText"
                  placeholder="Введите сообщение..."
                  @keyup.enter="sendMessage"
                />
              </div>
              <AppButton @click="sendMessage" :disabled="!messageText.trim()">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </AppButton>
            </div>
          </div>
        </div>

        <!-- No Chat Selected -->
        <div v-else class="flex-1 flex items-center justify-center">
          <div class="text-center">
            <svg class="w-24 h-24 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            <h3 class="text-xl font-medium text-text mb-2">Выберите диалог</h3>
            <p class="text-text-secondary">Выберите чат из списка слева для начала общения</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>