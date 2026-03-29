<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'

interface Props {
  show: boolean
  title?: string
  size?: 'sm' | 'md' | 'lg' | 'xl'
  closable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  closable: true
})

const emit = defineEmits<{
  close: []
}>()

const handleEscape = (event: KeyboardEvent) => {
  if (event.key === 'Escape' && props.closable) {
    emit('close')
  }
}

const handleOverlayClick = (event: MouseEvent) => {
  if (event.target === event.currentTarget && props.closable) {
    emit('close')
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleEscape)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscape)
})
</script>

<template>
  <Transition name="modal">
    <div
      v-if="show"
      class="fixed inset-0 z-50 overflow-y-auto"
      @click="handleOverlayClick"
    >
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>

        <div
          class="relative inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all"
          :class="{
            'max-w-sm w-full': size === 'sm',
            'max-w-lg w-full': size === 'md',
            'max-w-4xl w-full': size === 'lg',
            'max-w-7xl w-full': size === 'xl'
          }"
        >
          <div v-if="title || closable" class="flex items-center justify-between p-4 border-b">
            <h3 v-if="title" class="text-lg font-medium text-text">
              {{ title }}
            </h3>
            <button
              v-if="closable"
              @click="emit('close')"
              class="p-1 text-text-secondary hover:text-text rounded-md"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>

          <div class="p-4">
            <slot />
          </div>

          <div v-if="$slots.footer" class="flex justify-end gap-3 p-4 border-t bg-gray-50">
            <slot name="footer" />
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>