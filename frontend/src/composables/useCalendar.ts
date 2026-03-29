import { ref, computed } from 'vue'
import type { CalendarEvent, EventCreate, EventUpdate, EventStatus, EventType } from '@/types/calendar'
import { getEvents, createEvent as apiCreateEvent, updateEvent as apiUpdateEvent, updateEventStatus as apiUpdateEventStatus, deleteEvent as apiDeleteEvent } from '@/api/calendar'

const EVENT_COLORS: Record<EventType, string> = {
  booking: '#1929bb',    // DC blue
  task: '#017d0d',       // DC green
  follow_up: '#e6a23c',  // DC orange/warning
}

export function useCalendar() {
  const events = ref<CalendarEvent[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const toFullCalendarEvents = (eventList: CalendarEvent[]) => {
    return eventList.map(event => ({
      id: String(event.id),
      title: event.title,
      start: event.start_at,
      end: event.end_at,
      backgroundColor: EVENT_COLORS[event.event_type],
      borderColor: EVENT_COLORS[event.event_type],
      extendedProps: { ...event }
    }))
  }

  const fullCalendarEvents = computed(() => toFullCalendarEvents(events.value))

  const fetchEvents = async (start: string, end: string) => {
    try {
      loading.value = true
      error.value = null
      const response = await getEvents({ start, end })
      events.value = response.items
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Произошла ошибка при загрузке событий'
    } finally {
      loading.value = false
    }
  }

  const createEvent = async (data: EventCreate): Promise<CalendarEvent> => {
    try {
      loading.value = true
      error.value = null
      const newEvent = await apiCreateEvent(data)
      events.value.push(newEvent)
      return newEvent
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Произошла ошибка при создании события'
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateEvent = async (id: number, data: EventUpdate): Promise<CalendarEvent> => {
    try {
      loading.value = true
      error.value = null
      const updatedEvent = await apiUpdateEvent(id, data)
      const index = events.value.findIndex(e => e.id === id)
      if (index !== -1) {
        events.value[index] = updatedEvent
      }
      return updatedEvent
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Произошла ошибка при обновлении события'
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateEventStatus = async (id: number, status: EventStatus): Promise<CalendarEvent> => {
    try {
      loading.value = true
      error.value = null
      const updatedEvent = await apiUpdateEventStatus(id, status)
      const index = events.value.findIndex(e => e.id === id)
      if (index !== -1) {
        events.value[index] = updatedEvent
      }
      return updatedEvent
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Произошла ошибка при обновлении статуса события'
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteEvent = async (id: number): Promise<void> => {
    try {
      loading.value = true
      error.value = null
      await apiDeleteEvent(id)
      events.value = events.value.filter(e => e.id !== id)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Произошла ошибка при удалении события'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    events,
    fullCalendarEvents,
    loading,
    error,
    fetchEvents,
    createEvent,
    updateEvent,
    updateEventStatus,
    deleteEvent
  }
}