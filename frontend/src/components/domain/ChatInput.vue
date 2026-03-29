<script setup lang="ts">
import { ref, nextTick } from 'vue'

const props = defineProps<{
  disabled?: boolean
}>()

const emit = defineEmits<{
  send: [content: string]
  'connect-agent': []
}>()

const messageText = ref('')
const textareaRef = ref<HTMLTextAreaElement>()

const handleSend = () => {
  if (!messageText.value.trim() || props.disabled) return

  emit('send', messageText.value.trim())
  messageText.value = ''
  resetTextareaHeight()
}

const handleKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    handleSend()
  }
}

const handleInput = async () => {
  await nextTick()
  adjustTextareaHeight()
}

const adjustTextareaHeight = () => {
  if (!textareaRef.value) return

  const textarea = textareaRef.value
  textarea.style.height = 'auto'

  const maxHeight = 4 * 24 // 4 lines * 24px line height
  const newHeight = Math.min(textarea.scrollHeight, maxHeight)

  textarea.style.height = `${newHeight}px`
}

const resetTextareaHeight = () => {
  if (textareaRef.value) {
    textareaRef.value.style.height = 'auto'
  }
}

const handleConnectAgent = () => {
  emit('connect-agent')
}
</script>

<template>
  <div class="p-4 bg-white border-t border-gray-200">
    <div class="flex gap-3 items-end">
      <!-- Connect Agent Button -->
      <button
        @click="handleConnectAgent"
        class="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg font-medium transition-colors flex items-center gap-2 flex-shrink-0"
        :disabled="disabled"
      >
        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
        </svg>
        <span class="hidden sm:inline">Подключить агента</span>
      </button>

      <!-- Message Input -->
      <div class="flex-1 relative">
        <textarea
          ref="textareaRef"
          v-model="messageText"
          @keydown="handleKeydown"
          @input="handleInput"
          placeholder="Введите сообщение..."
          class="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none overflow-y-auto"
          :class="{
            'bg-gray-50 text-gray-400 cursor-not-allowed': disabled
          }"
          :disabled="disabled"
          rows="1"
          style="line-height: 24px; max-height: 96px;"
        />

        <!-- Send Button -->
        <button
          @click="handleSend"
          :disabled="!messageText.trim() || disabled"
          class="absolute right-2 bottom-2 w-8 h-8 bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 text-white rounded-lg transition-colors flex items-center justify-center"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Hint text -->
    <div class="mt-2 text-xs text-gray-500">
      Нажмите Enter для отправки, Shift+Enter для новой строки
    </div>
  </div>
</template>