<script setup lang="ts">
import { ref, computed } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import type { CalendarOptions, DateSelectArg, EventClickArg, EventDropArg, EventResizeArg, DatesSetArg } from '@fullcalendar/core'
import AppButton from '@/components/ui/AppButton.vue'
import EventModal from '@/components/domain/EventModal.vue'
import { useCalendar } from '@/composables/useCalendar'
import type { CalendarEvent, EventCreate, EventUpdate } from '@/types/calendar'

const {
  events,
  fullCalendarEvents,
  loading,
  error,
  fetchEvents,
  createEvent,
  updateEvent,
  deleteEvent
} = useCalendar()

// Modal state
const showEventModal = ref(false)
const selectedEvent = ref<CalendarEvent | null>(null)
const selectedStart = ref<string | null>(null)
const selectedEnd = ref<string | null>(null)

// Calendar options (reactive)
const calendarOptions = computed((): CalendarOptions => ({
  plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
  headerToolbar: {
    left: 'prev,next today',
    center: 'title',
    right: 'dayGridMonth,timeGridWeek,timeGridDay'
  },
  initialView: 'dayGridMonth',
  locale: 'ru',
  buttonText: {
    today: 'Сегодня',
    month: 'Месяц',
    week: 'Неделя',
    day: 'День'
  },
  allDayText: 'Весь день',
  dayHeaderFormat: { weekday: 'short' },
  editable: true,
  selectable: true,
  selectMirror: true,
  dayMaxEvents: true,
  weekends: true,
  height: 'auto',
  events: fullCalendarEvents.value,

  // Event handlers
  datesSet: handleDatesSet,
  select: handleDateSelect,
  eventClick: handleEventClick,
  eventDrop: handleEventDrop,
  eventResize: handleEventResize
}))

// Handle date range change (load events for visible range)
async function handleDatesSet(info: DatesSetArg) {
  const start = info.startStr
  const end = info.endStr
  await fetchEvents(start, end)
}

// Handle date selection (open create modal)
function handleDateSelect(selectInfo: DateSelectArg) {
  selectedEvent.value = null
  selectedStart.value = selectInfo.startStr
  selectedEnd.value = selectInfo.endStr || selectInfo.startStr
  showEventModal.value = true

  // Clear selection
  selectInfo.view.calendar.unselect()
}

// Handle event click (open edit modal)
function handleEventClick(clickInfo: EventClickArg) {
  selectedEvent.value = events.value.find(e => e.id === parseInt(clickInfo.event.id)) ?? null
  selectedStart.value = null
  selectedEnd.value = null
  showEventModal.value = true
}

// Handle event drag (update start/end times)
async function handleEventDrop(dropInfo: EventDropArg) {
  const eventId = parseInt(dropInfo.event.id)
  const updateData: EventUpdate = {
    start_at: dropInfo.event.start?.toISOString(),
    end_at: dropInfo.event.end?.toISOString()
  }

  try {
    await updateEvent(eventId, updateData)
  } catch (error) {
    // Revert on error
    dropInfo.revert()
  }
}

// Handle event resize (update end time)
async function handleEventResize(resizeInfo: EventResizeArg) {
  const eventId = parseInt(resizeInfo.event.id)
  const updateData: EventUpdate = {
    end_at: resizeInfo.event.end?.toISOString()
  }

  try {
    await updateEvent(eventId, updateData)
  } catch (error) {
    // Revert on error
    resizeInfo.revert()
  }
}

// Open create modal
const openCreateModal = () => {
  selectedEvent.value = null
  selectedStart.value = null
  selectedEnd.value = null
  showEventModal.value = true
}

// Handle modal save
const handleModalSave = async (data: EventCreate | EventUpdate) => {
  try {
    if (selectedEvent.value) {
      // Update existing event
      await updateEvent(selectedEvent.value.id, data as EventUpdate)
    } else {
      // Create new event
      await createEvent(data as EventCreate)
    }
    closeModal()
  } catch (err) {
    // Error is already handled in the composable
  }
}

// Handle modal delete
const handleModalDelete = async (id: number) => {
  try {
    await deleteEvent(id)
    closeModal()
  } catch (err) {
    // Error is already handled in the composable
  }
}

// Close modal
const closeModal = () => {
  showEventModal.value = false
  selectedEvent.value = null
  selectedStart.value = null
  selectedEnd.value = null
}
</script>

<template>
  <div class="p-6">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-semibold text-text">Календарь</h1>
        <p class="text-text-secondary mt-1">Управление событиями и задачами</p>
      </div>
      <AppButton variant="primary" @click="openCreateModal">
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        Новое событие
      </AppButton>
    </div>

    <!-- Error message -->
    <div v-if="error" class="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
      <p class="text-red-700">{{ error }}</p>
    </div>

    <!-- Loading indicator -->
    <div v-if="loading" class="mb-4 flex justify-center">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-accent"></div>
    </div>

    <!-- Calendar -->
    <div class="card p-6">
      <FullCalendar :options="calendarOptions.value" class="calendar-wrapper" />
    </div>

    <!-- Event Modal -->
    <EventModal
      :show="showEventModal"
      :event="selectedEvent"
      :initial-start="selectedStart"
      :initial-end="selectedEnd"
      @close="closeModal"
      @save="handleModalSave"
      @delete="handleModalDelete"
    />
  </div>
</template>

<style>
/* FullCalendar custom styles */
.calendar-wrapper {
  --fc-border-color: #e5e7eb;
  --fc-button-bg-color: var(--color-accent);
  --fc-button-border-color: var(--color-accent);
  --fc-button-hover-bg-color: var(--color-accent-light);
  --fc-button-hover-border-color: var(--color-accent-light);
  --fc-button-active-bg-color: var(--color-accent);
  --fc-button-active-border-color: var(--color-accent);
  --fc-today-bg-color: rgba(25, 41, 187, 0.1);
}

.fc-toolbar {
  margin-bottom: 1.5rem !important;
}

.fc-toolbar-title {
  font-size: 1.25rem !important;
  font-weight: 600 !important;
  color: var(--color-text) !important;
}

.fc-button {
  font-size: 0.875rem !important;
  font-weight: 500 !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
  border-radius: 0.5rem !important;
}

.fc-button-primary:not(:disabled):active,
.fc-button-primary:not(:disabled).fc-button-active {
  background-color: var(--color-accent) !important;
  border-color: var(--color-accent) !important;
}

.fc-daygrid-event,
.fc-timegrid-event {
  border-radius: 0.375rem !important;
  border: none !important;
  font-size: 0.75rem !important;
  font-weight: 500 !important;
  padding: 0.125rem 0.375rem !important;
}

.fc-event-title {
  font-weight: 500 !important;
}

.fc-daygrid-day-number {
  color: var(--color-text) !important;
  font-weight: 500 !important;
}

.fc-col-header-cell {
  font-weight: 600 !important;
  background-color: #f9fafb !important;
  border-color: var(--fc-border-color) !important;
}

.fc-scrollgrid {
  border-color: var(--fc-border-color) !important;
}

.fc-daygrid-day {
  border-color: var(--fc-border-color) !important;
}

.fc-timegrid-slot {
  border-color: var(--fc-border-color) !important;
}

.fc-timegrid-axis {
  font-size: 0.75rem !important;
  color: var(--color-text-secondary) !important;
}

/* Hover effects */
.fc-daygrid-day:hover {
  background-color: #f9fafb;
}

.fc-event:hover {
  opacity: 0.9;
  cursor: pointer;
}

/* Selection styles */
.fc-highlight {
  background-color: rgba(25, 41, 187, 0.2) !important;
}
</style>