<script setup lang="ts">
import type { Message } from '@/types/chat'
import { computed } from 'vue'
import { formatRelativeTime } from '@/utils/formatDate'

const props = defineProps<{
  message: Message
}>()

// Message alignment and styling based on direction
const isIncoming = computed(() => props.message.direction === 'in')
const isOutgoing = computed(() => props.message.direction === 'out')
const isFromAgent = computed(() => props.message.is_from_agent)

// Bubble styles based on message type
const bubbleClasses = computed(() => {
  const base = 'max-w-[70%] rounded-2xl px-4 py-3 relative break-words'

  if (isFromAgent.value) {
    return `${base} bg-cyan-50 border border-cyan-200`
  }

  if (isIncoming.value) {
    return `${base} bg-white border border-gray-200 shadow-sm`
  }

  // Outgoing
  return `${base} bg-blue-500 text-white`
})

const containerClasses = computed(() => {
  if (isIncoming.value) {
    return 'flex justify-start'
  }
  return 'flex justify-end'
})

// Source icon
const sourceIcon = computed(() => {
  switch (props.message.source) {
    case 'telegram':
      return 'M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z'
    case 'whatsapp':
      return 'M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893A11.821 11.821 0 0020.885 3.108'
    case 'manual':
    default:
      return null
  }
})

const sourceColor = computed(() => {
  switch (props.message.source) {
    case 'telegram':
      return '#0088cc'
    case 'whatsapp':
      return '#25D366'
    case 'manual':
    default:
      return '#6b7280'
  }
})

const formattedTime = computed(() => {
  return formatRelativeTime(props.message.created_at)
})
</script>

<template>
  <div class="mb-4" :class="containerClasses">
    <div :class="bubbleClasses">
      <!-- Agent indicator -->
      <div v-if="isFromAgent" class="flex items-center gap-2 mb-1">
        <svg class="w-4 h-4 text-cyan-600" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
        </svg>
        <span class="text-xs text-cyan-700 font-medium">Агент</span>
      </div>

      <!-- Message content -->
      <div class="whitespace-pre-wrap">
        {{ message.content }}
      </div>

      <!-- Footer with time and source -->
      <div class="flex items-center justify-between mt-2 gap-2">
        <div class="flex items-center gap-1">
          <!-- Source icon -->
          <svg
            v-if="sourceIcon"
            class="w-3 h-3 opacity-60"
            :style="{ color: sourceColor }"
            viewBox="0 0 24 24"
            fill="currentColor"
          >
            <path :d="sourceIcon"/>
          </svg>

          <!-- Manual source icon -->
          <svg
            v-else-if="message.source === 'manual'"
            class="w-3 h-3 opacity-60"
            :style="{ color: sourceColor }"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
        </div>

        <span
          class="text-xs opacity-60 flex-shrink-0"
          :class="isOutgoing && !isFromAgent ? 'text-blue-100' : 'text-gray-500'"
        >
          {{ formattedTime }}
        </span>
      </div>

      <!-- Message tail -->
      <div
        v-if="isIncoming"
        class="absolute -left-2 top-3 w-0 h-0 border-t-8 border-b-8 border-r-8 border-transparent"
        :class="isFromAgent ? 'border-r-cyan-50' : 'border-r-white'"
      ></div>

      <div
        v-else
        class="absolute -right-2 top-3 w-0 h-0 border-t-8 border-b-8 border-l-8 border-transparent border-l-blue-500"
      ></div>
    </div>
  </div>
</template>