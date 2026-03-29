<script setup lang="ts">
import { computed } from 'vue'
import AppInput from '@/components/ui/AppInput.vue'
import type { EventType, EventStatus } from '@/types/calendar'
import type { Lead } from '@/types/lead'

interface FormData {
  title: string
  description: string
  start_at: string
  end_at: string
  event_type: EventType
  status: EventStatus
  lead_id: number | null
}

interface Props {
  modelValue: FormData
  leads: Lead[]
  isEditMode: boolean
  loadingLeads?: boolean
  errors?: {
    title: string
    start_at: string
    end_at: string
  }
}

const props = withDefaults(defineProps<Props>(), {
  loadingLeads: false,
  errors: () => ({ title: '', start_at: '', end_at: '' })
})

const emit = defineEmits<{
  'update:modelValue': [value: FormData]
}>()

// Dropdown options
const eventTypeOptions = [
  { value: 'booking', label: 'Запись' },
  { value: 'task', label: 'Задача' },
  { value: 'follow_up', label: 'Напоминание' }
]

const eventStatusOptions = [
  { value: 'planned', label: 'Запланировано' },
  { value: 'done', label: 'Выполнено' },
  { value: 'cancelled', label: 'Отменено' }
]

// Computed for v-model
const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// Helper functions for individual fields
const updateField = <K extends keyof FormData>(field: K, value: FormData[K]) => {
  emit('update:modelValue', { ...props.modelValue, [field]: value })
}
</script>

<template>
  <div class="space-y-4">
    <!-- Title -->
    <AppInput
      :model-value="modelValue.title"
      label="Название"
      placeholder="Введите название события"
      required
      :error="errors.title"
      @update:model-value="updateField('title', $event)"
    />

    <!-- Description -->
    <div>
      <label class="block text-sm font-medium text-text mb-1">Описание</label>
      <textarea
        :value="modelValue.description"
        placeholder="Опишите детали события"
        rows="3"
        class="input resize-none"
        @input="updateField('description', ($event.target as HTMLTextAreaElement).value)"
      ></textarea>
    </div>

    <!-- Date and time -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-text mb-1">
          Время начала <span class="text-danger">*</span>
        </label>
        <input
          :value="modelValue.start_at"
          type="datetime-local"
          required
          class="input"
          :class="{ 'border-danger focus:border-danger focus:ring-danger': errors.start_at }"
          @input="updateField('start_at', ($event.target as HTMLInputElement).value)"
        />
        <p v-if="errors.start_at" class="mt-1 text-sm text-danger">
          {{ errors.start_at }}
        </p>
      </div>

      <div>
        <label class="block text-sm font-medium text-text mb-1">
          Время окончания <span class="text-danger">*</span>
        </label>
        <input
          :value="modelValue.end_at"
          type="datetime-local"
          required
          class="input"
          :class="{ 'border-danger focus:border-danger focus:ring-danger': errors.end_at }"
          @input="updateField('end_at', ($event.target as HTMLInputElement).value)"
        />
        <p v-if="errors.end_at" class="mt-1 text-sm text-danger">
          {{ errors.end_at }}
        </p>
      </div>
    </div>

    <!-- Event type -->
    <div>
      <label class="block text-sm font-medium text-text mb-1">Тип события</label>
      <select
        :value="modelValue.event_type"
        class="input"
        @change="updateField('event_type', ($event.target as HTMLSelectElement).value as EventType)"
      >
        <option v-for="option in eventTypeOptions" :key="option.value" :value="option.value">
          {{ option.label }}
        </option>
      </select>
    </div>

    <!-- Status (only in edit mode) -->
    <div v-if="isEditMode">
      <label class="block text-sm font-medium text-text mb-1">Статус</label>
      <select
        :value="modelValue.status"
        class="input"
        @change="updateField('status', ($event.target as HTMLSelectElement).value as EventStatus)"
      >
        <option v-for="option in eventStatusOptions" :key="option.value" :value="option.value">
          {{ option.label }}
        </option>
      </select>
    </div>

    <!-- Lead selection -->
    <div>
      <label class="block text-sm font-medium text-text mb-1">Лид</label>
      <select
        :value="modelValue.lead_id"
        class="input"
        :disabled="loadingLeads"
        @change="updateField('lead_id', ($event.target as HTMLSelectElement).value ? parseInt(($event.target as HTMLSelectElement).value) : null)"
      >
        <option value="">Не выбран</option>
        <option v-for="lead in leads" :key="lead.id" :value="lead.id">
          {{ lead.name }} {{ lead.phone ? `(${lead.phone})` : '' }}
        </option>
      </select>
      <p v-if="loadingLeads" class="mt-1 text-sm text-text-secondary">
        Загрузка лидов...
      </p>
    </div>
  </div>
</template>