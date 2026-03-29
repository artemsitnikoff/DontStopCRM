<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  src?: string
  alt?: string
  name?: string
  size?: 'sm' | 'md' | 'lg' | 'xl'
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md'
})

const initials = computed(() => {
  if (!props.name) return '?'
  const parts = props.name.split(' ')
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return parts[0][0].toUpperCase()
})

const sizeClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'w-6 h-6 text-xs'
    case 'md':
      return 'w-8 h-8 text-sm'
    case 'lg':
      return 'w-10 h-10 text-base'
    case 'xl':
      return 'w-12 h-12 text-lg'
    default:
      return 'w-8 h-8 text-sm'
  }
})
</script>

<template>
  <div
    class="inline-flex items-center justify-center rounded-full bg-accent text-white font-medium"
    :class="sizeClasses"
  >
    <img
      v-if="src"
      :src="src"
      :alt="alt || name"
      class="w-full h-full rounded-full object-cover"
    />
    <span v-else>{{ initials }}</span>
  </div>
</template>