<script setup lang="ts">
import { ref } from 'vue'
import draggable from 'vuedraggable'
import LeadCard from './LeadCard.vue'
import type { Lead, LeadStatus } from '@/types/lead'

const props = defineProps<{
  title: string
  status: LeadStatus
  leads: Lead[]
  color: string
}>()

const emit = defineEmits<{
  leadMoved: [leadId: number, newStatus: LeadStatus]
}>()

const drag = ref(false)

const onChange = (event: any) => {
  if (event.added) {
    const { element } = event.added
    emit('leadMoved', element.id, props.status)
  }
}</script>

<template>
  <div class="bg-gray-50 rounded-xl p-4 flex-1 min-h-96">
    <!-- Column header -->
    <div class="flex items-center justify-between mb-4">
      <h3 class="font-semibold text-black">{{ title }}</h3>
      <span
        class="text-white text-xs font-medium px-2.5 py-1 rounded-full"
        :style="{ backgroundColor: color }"
      >
        {{ leads.length }}
      </span>
    </div>

    <!-- Draggable leads list -->
    <draggable
      :list="leads"
      group="leads"
      item-key="id"
      @change="onChange"
      class="space-y-3 min-h-80"
      :animation="200"
      :disabled="false"
      ghost-class="ghost"
      @start="drag = true"
      @end="drag = false"
    >
      <template #item="{ element }">
        <LeadCard :lead="element" />
      </template>
    </draggable>

    <!-- Empty state -->
    <div v-if="leads.length === 0" class="text-center py-12">
      <svg class="mx-auto h-12 w-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
      </svg>
      <p class="text-sm text-gray-500">Нет лидов</p>
    </div>
  </div>
</template>

<style scoped>
.ghost {
  opacity: 0.5;
  background: var(--color-bg);
}

.flip-list-move {
  transition: transform 0.5s;
}

.no-move {
  transition: transform 0s;
}

.ghost {
  opacity: 0.5;
  background: var(--color-primary);
}
</style>