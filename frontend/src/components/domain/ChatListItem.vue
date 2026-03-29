<script setup lang="ts">
import type { ChatPreview } from '@/types/chat'
import { computed } from 'vue'
import { formatRelativeTime } from '@/utils/formatDate'

const props = defineProps<{
  chat: ChatPreview
  active: boolean
}>()

const emit = defineEmits<{
  select: [leadId: number]
}>()

// Generate avatar background color based on lead_id
const avatarColor = computed(() => {
  const colors = [
    '#1929bb', // primary
    '#e03a15', // accent
    '#01faff', // cyan
    '#017d0d', // success
    '#e6a23c', // warning
    '#0088cc', // telegram blue
    '#25D366', // whatsapp green
    '#E1306C', // instagram pink
  ]
  return colors[props.chat.lead_id % colors.length]
})

// Get first letter of lead name for avatar
const avatarLetter = computed(() => {
  return props.chat.lead_name?.charAt(0)?.toUpperCase() || '?'
})

// Format time for display
const formattedTime = computed(() => {
  if (!props.chat.last_message_time) return ''
  return formatRelativeTime(props.chat.last_message_time)
})

// Truncate message preview
const messagePreview = computed(() => {
  if (!props.chat.last_message) return 'Нет сообщений'
  return props.chat.last_message.length > 50
    ? props.chat.last_message.substring(0, 50) + '...'
    : props.chat.last_message
})

const handleClick = () => {
  emit('select', props.chat.lead_id)
}
</script>

<template>
  <div
    @click="handleClick"
    class="p-4 hover:bg-gray-50 cursor-pointer transition-colors border-b border-gray-100 last:border-b-0"
    :class="{
      'bg-blue-50 border-l-4 border-l-blue-500': active
    }"
  >
    <div class="flex items-center gap-3">
      <!-- Avatar -->
      <div
        class="w-12 h-12 rounded-full flex items-center justify-center text-white font-semibold text-lg flex-shrink-0"
        :style="{ backgroundColor: avatarColor }"
      >
        {{ avatarLetter }}
      </div>

      <!-- Content -->
      <div class="flex-1 min-w-0">
        <div class="flex items-center justify-between mb-1">
          <h4 class="font-semibold text-gray-900 truncate">
            {{ chat.lead_name }}
          </h4>
          <span v-if="formattedTime" class="text-xs text-gray-500 flex-shrink-0 ml-2">
            {{ formattedTime }}
          </span>
        </div>

        <div class="flex items-center justify-between">
          <p class="text-sm text-gray-600 truncate flex-1">
            {{ messagePreview }}
          </p>

          <!-- Message count badge -->
          <div
            v-if="chat.message_count > 0"
            class="ml-2 min-w-[20px] h-5 rounded-full bg-blue-500 text-white text-xs flex items-center justify-center px-1.5 flex-shrink-0"
          >
            {{ chat.message_count > 99 ? '99+' : chat.message_count }}
          </div>
        </div>

        <!-- Phone number if available -->
        <div v-if="chat.lead_phone" class="text-xs text-gray-500 mt-1">
          {{ chat.lead_phone }}
        </div>
      </div>
    </div>
  </div>
</template>