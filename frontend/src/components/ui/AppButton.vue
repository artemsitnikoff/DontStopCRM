<script setup lang="ts">
interface Props {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  loading?: boolean
  type?: 'button' | 'submit' | 'reset'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  disabled: false,
  loading: false,
  type: 'button'
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const handleClick = (event: MouseEvent) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>

<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    @click="handleClick"
    class="btn transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2"
    :class="[
      {
        'btn-primary': variant === 'primary',
        'btn-secondary': variant === 'secondary',
        'bg-danger text-white hover:bg-red-600 focus:ring-danger': variant === 'danger',
        'bg-transparent text-text-secondary hover:bg-gray-100 border-transparent': variant === 'ghost',
        'px-2 py-1 text-sm': size === 'sm',
        'px-4 py-2': size === 'md',
        'px-6 py-3 text-lg': size === 'lg',
        'opacity-50 cursor-not-allowed': disabled || loading
      }
    ]"
  >
    <svg
      v-if="loading"
      class="animate-spin -ml-1 mr-2 h-4 w-4"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>
    <slot />
  </button>
</template>