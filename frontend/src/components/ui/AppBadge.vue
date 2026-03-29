<script setup lang="ts">
interface Props {
  variant?: 'default' | 'primary' | 'success' | 'warning' | 'danger'
  size?: 'sm' | 'md'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  size: 'md'
})
</script>

<template>
  <span
    class="inline-flex items-center font-medium rounded-full"
    :class="[
      {
        'px-2 py-0.5 text-xs': size === 'sm',
        'px-2.5 py-0.5 text-xs': size === 'md',
        'bg-gray-100 text-gray-800': variant === 'default',
        'bg-accent bg-opacity-10 text-accent': variant === 'primary',
        'bg-success bg-opacity-10 text-green-800': variant === 'success',
        'bg-warning bg-opacity-10 text-yellow-800': variant === 'warning',
        'bg-danger bg-opacity-10 text-red-800': variant === 'danger'
      }
    ]"
  >
    <slot />
  </span>
</template>