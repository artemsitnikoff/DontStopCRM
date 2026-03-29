<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import AppModal from '@/components/ui/AppModal.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppInput from '@/components/ui/AppInput.vue'
import type { CalendarEvent, EventCreate, EventUpdate, EventType, EventStatus } from '@/types/calendar'
import type { Lead } from '@/types/lead'
import { getLeads } from '@/api/leads'

interface Props {
  show: boolean
  event?: CalendarEvent | null
  initialStart?: string | null
  initialEnd?: string | null
}

const props = withDefaults(defineProps<Props>(), {
  event: null,
  initialStart: null,
  initialEnd: null
})

const emit = defineEmits<{
  close: []
  save: [data: EventCreate | EventUpdate]
  delete: [id: number]
}>()

// Form data
const formData = ref({
  title: '',
  description: '',
  start_at: '',
  end_at: '',
  event_type: 'booking' as EventType,
  status: 'planned' as EventStatus,
  lead_id: null as number | null
})

// Form validation
const errors = ref({
  title: '',
  start_at: '',
  end_at: ''
})

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

// Leads for dropdown
const leads = ref<Lead[]>([])
const loadingLeads = ref(false)

// Computed
const isEditMode = computed(() => !!props.event)
const title = computed(() => isEditMode.value ? 'Редактировать событие' : 'Новое событие')

// Format datetime for datetime-local input
const formatForInput = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  // Convert to local timezone and format as YYYY-MM-DDTHH:MM
  const offset = date.getTimezoneOffset()
  const localDate = new Date(date.getTime() - offset * 60000)
  return localDate.toISOString().slice(0, 16)
}

// Convert datetime-local input to ISO string
const formatForApi = (inputValue: string) => {
  if (!inputValue) return ''
  return new Date(inputValue).toISOString()
}

// Load leads for dropdown
const loadLeads = async () => {
  try {
    loadingLeads.value = true
    const response = await getLeads({ size: 1000 })
    leads.value = response.items
  } catch (error) {
    console.error('Failed to load leads:', error)
  } finally {
    loadingLeads.value = false
  }
}

// Initialize form
const initializeForm = () => {
  if (props.event) {
    // Edit mode - populate with event data
    formData.value = {
      title: props.event.title,
      description: props.event.description || '',
      start_at: formatForInput(props.event.start_at),
      end_at: formatForInput(props.event.end_at),
      event_type: props.event.event_type,
      status: props.event.status,
      lead_id: props.event.lead_id
    }
  } else {
    // Create mode - reset form and use initial dates if provided
    formData.value = {
      title: '',
      description: '',
      start_at: props.initialStart ? formatForInput(props.initialStart) : '',
      end_at: props.initialEnd ? formatForInput(props.initialEnd) : '',
      event_type: 'booking',
      status: 'planned',
      lead_id: null
    }
  }

  // Clear errors
  errors.value = { title: '', start_at: '', end_at: '' }
}

// Validate form
const validateForm = () => {
  errors.value = { title: '', start_at: '', end_at: '' }
  let isValid = true

  if (!formData.value.title.trim()) {
    errors.value.title = 'Название обязательно'
    isValid = false
  }

  if (!formData.value.start_at) {
    errors.value.start_at = 'Время начала обязательно'
    isValid = false
  }

  if (!formData.value.end_at) {
    errors.value.end_at = 'Время окончания обязательно'
    isValid = false
  }

  if (formData.value.start_at && formData.value.end_at) {
    const start = new Date(formData.value.start_at)
    const end = new Date(formData.value.end_at)
    if (start >= end) {
      errors.value.end_at = 'Время окончания должно быть после времени начала'
      isValid = false
    }
  }

  return isValid
}

// Handle save
const handleSave = () => {
  if (!validateForm()) return

  const data = {
    title: formData.value.title.trim(),
    description: formData.value.description.trim() || undefined,
    start_at: formatForApi(formData.value.start_at),
    end_at: formatForApi(formData.value.end_at),
    event_type: formData.value.event_type,
    status: formData.value.status,
    lead_id: formData.value.lead_id
  }

  emit('save', data)
}

// Handle delete
const handleDelete = () => {
  if (props.event && confirm('Вы уверены, что хотите удалить это событие?')) {
    emit('delete', props.event.id)
  }
}

// Watch for modal show/hide
watch(() => props.show, (show) => {
  if (show) {
    initializeForm()
    loadLeads()
  }
})

// Initialize on mount if modal is already shown
onMounted(() => {
  if (props.show) {
    initializeForm()
    loadLeads()
  }
})
</script>

<template>
  <AppModal :show="show" :title="title" size="md" @close="emit('close')">
    <form @submit.prevent="handleSave" class="space-y-4">
      <!-- Title -->
      <AppInput
        v-model="formData.title"
        label="Название"
        placeholder="Введите название события"
        required
        :error="errors.title"
      />

      <!-- Description -->
      <div>
        <label class="block text-sm font-medium text-text mb-1">Описание</label>
        <textarea
          v-model="formData.description"
          placeholder="Опишите детали события"
          rows="3"
          class="input resize-none"
        ></textarea>
      </div>

      <!-- Date and time -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-text mb-1">
            Время начала <span class="text-danger">*</span>
          </label>
          <input
            v-model="formData.start_at"
            type="datetime-local"
            required
            class="input"
            :class="{ 'border-danger focus:border-danger focus:ring-danger': errors.start_at }"
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
            v-model="formData.end_at"
            type="datetime-local"
            required
            class="input"
            :class="{ 'border-danger focus:border-danger focus:ring-danger': errors.end_at }"
          />
          <p v-if="errors.end_at" class="mt-1 text-sm text-danger">
            {{ errors.end_at }}
          </p>
        </div>
      </div>

      <!-- Event type -->
      <div>
        <label class="block text-sm font-medium text-text mb-1">Тип события</label>
        <select v-model="formData.event_type" class="input">
          <option v-for="option in eventTypeOptions" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
      </div>

      <!-- Status (only in edit mode) -->
      <div v-if="isEditMode">
        <label class="block text-sm font-medium text-text mb-1">Статус</label>
        <select v-model="formData.status" class="input">
          <option v-for="option in eventStatusOptions" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
      </div>

      <!-- Lead selection -->
      <div>
        <label class="block text-sm font-medium text-text mb-1">Лид</label>
        <select v-model="formData.lead_id" class="input" :disabled="loadingLeads">
          <option :value="null">Не выбран</option>
          <option v-for="lead in leads" :key="lead.id" :value="lead.id">
            {{ lead.name }} {{ lead.phone ? `(${lead.phone})` : '' }}
          </option>
        </select>
        <p v-if="loadingLeads" class="mt-1 text-sm text-text-secondary">
          Загрузка лидов...
        </p>
      </div>
    </form>

    <template #footer>
      <div class="flex justify-between w-full">
        <div>
          <AppButton
            v-if="isEditMode"
            variant="danger"
            @click="handleDelete"
          >
            Удалить
          </AppButton>
        </div>
        <div class="flex gap-3">
          <AppButton variant="secondary" @click="emit('close')">
            Отмена
          </AppButton>
          <AppButton variant="primary" @click="handleSave">
            {{ isEditMode ? 'Сохранить' : 'Создать' }}
          </AppButton>
        </div>
      </div>
    </template>
  </AppModal>
</template>