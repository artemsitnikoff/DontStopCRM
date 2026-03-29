<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import AppModal from '@/components/ui/AppModal.vue'
import AppButton from '@/components/ui/AppButton.vue'
import EventForm from './EventForm.vue'
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
  event_type: 'task' as EventType,
  status: 'planned' as EventStatus,
  lead_id: null as number | null
})

// Form validation
const errors = ref({
  title: '',
  start_at: '',
  end_at: ''
})


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
  } catch (err) {
    // Error handling could be improved with user feedback
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
      event_type: 'task',
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
    <EventForm
      v-model="formData"
      :leads="leads"
      :is-edit-mode="isEditMode"
      :loading-leads="loadingLeads"
      :errors="errors"
    />

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