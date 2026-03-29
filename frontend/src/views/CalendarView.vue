<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppBadge from '@/components/ui/AppBadge.vue'
import { useApi } from '@/composables/useApi'
import { getAppointments } from '@/api/calendar'
import { formatDate, formatTime } from '@/utils/formatDate'
import { AppointmentType, type Appointment } from '@/types/calendar'

const { data: appointments, loading, error, execute } = useApi<Appointment[]>()
const currentDate = ref(new Date())

const typeLabels = {
  [AppointmentType.Call]: 'Звонок',
  [AppointmentType.Meeting]: 'Встреча',
  [AppointmentType.Demo]: 'Демо',
  [AppointmentType.Followup]: 'Обратная связь'
}

const typeVariants = {
  [AppointmentType.Call]: 'primary',
  [AppointmentType.Meeting]: 'success',
  [AppointmentType.Demo]: 'warning',
  [AppointmentType.Followup]: 'default'
} as const

const todayAppointments = computed(() => {
  if (!appointments.value) return []

  const today = new Date()
  const todayStr = today.toISOString().split('T')[0]

  return appointments.value.filter(appointment => {
    const appointmentDate = new Date(appointment.start_time).toISOString().split('T')[0]
    return appointmentDate === todayStr
  }).sort((a, b) => new Date(a.start_time).getTime() - new Date(b.start_time).getTime())
})

const upcomingAppointments = computed(() => {
  if (!appointments.value) return []

  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)

  return appointments.value.filter(appointment => {
    const appointmentDate = new Date(appointment.start_time)
    return appointmentDate > tomorrow
  }).sort((a, b) => new Date(a.start_time).getTime() - new Date(b.start_time).getTime())
})

onMounted(() => {
  execute(getAppointments)
})

const goToPrevMonth = () => {
  const prev = new Date(currentDate.value)
  prev.setMonth(prev.getMonth() - 1)
  currentDate.value = prev
}

const goToNextMonth = () => {
  const next = new Date(currentDate.value)
  next.setMonth(next.getMonth() + 1)
  currentDate.value = next
}

const goToToday = () => {
  currentDate.value = new Date()
}
</script>

<template>
  <div class="p-6">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-semibold text-text">Календарь</h1>
        <p class="text-text-secondary mt-1">Управление встречами и звонками</p>
      </div>
      <AppButton variant="primary">
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        Новая встреча
      </AppButton>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Calendar Widget -->
      <div class="lg:col-span-2">
        <div class="card p-6">
          <!-- Calendar Header -->
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-lg font-semibold text-text">
              {{ currentDate.toLocaleDateString('ru-RU', { month: 'long', year: 'numeric' }) }}
            </h2>
            <div class="flex gap-2">
              <button
                @click="goToPrevMonth"
                class="p-2 text-text-secondary hover:text-text hover:bg-gray-100 rounded-lg transition-colors"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <button
                @click="goToToday"
                class="px-3 py-1 text-sm text-accent hover:bg-accent hover:text-white rounded-lg transition-colors"
              >
                Сегодня
              </button>
              <button
                @click="goToNextMonth"
                class="p-2 text-text-secondary hover:text-text hover:bg-gray-100 rounded-lg transition-colors"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Calendar Grid Placeholder -->
          <div class="bg-gray-50 rounded-lg h-96 flex items-center justify-center">
            <div class="text-center">
              <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <p class="text-text-secondary">Календарная сетка будет здесь</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Appointments Sidebar -->
      <div class="space-y-6">
        <!-- Today's Appointments -->
        <div class="card p-5">
          <h3 class="font-medium text-text mb-4 flex items-center">
            <svg class="w-5 h-5 mr-2 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Сегодня
          </h3>

          <!-- Loading -->
          <div v-if="loading" class="flex justify-center py-4">
            <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-accent"></div>
          </div>

          <!-- Error -->
          <div v-else-if="error" class="text-danger text-sm">{{ error }}</div>

          <!-- Today's List -->
          <div v-else-if="todayAppointments.length > 0" class="space-y-3">
            <div
              v-for="appointment in todayAppointments"
              :key="appointment.id"
              class="p-3 bg-gray-50 rounded-lg"
            >
              <div class="flex items-start justify-between mb-2">
                <h4 class="font-medium text-sm text-text truncate">{{ appointment.title }}</h4>
                <AppBadge :variant="typeVariants[appointment.type]" size="sm">
                  {{ typeLabels[appointment.type] }}
                </AppBadge>
              </div>

              <div class="text-xs text-text-secondary space-y-1">
                <div class="flex items-center">
                  <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ formatTime(appointment.start_time) }} - {{ formatTime(appointment.end_time) }}
                </div>

                <div v-if="appointment.lead_name" class="flex items-center">
                  <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  {{ appointment.lead_name }}
                </div>

                <div v-if="appointment.location" class="flex items-center">
                  <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  {{ appointment.location }}
                </div>
              </div>
            </div>
          </div>

          <!-- Empty Today -->
          <div v-else class="text-center py-6">
            <svg class="w-8 h-8 text-gray-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p class="text-sm text-text-secondary">Встреч на сегодня нет</p>
          </div>
        </div>

        <!-- Upcoming Appointments -->
        <div class="card p-5">
          <h3 class="font-medium text-text mb-4 flex items-center">
            <svg class="w-5 h-5 mr-2 text-warning" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            Предстоящие
          </h3>

          <div v-if="!loading && upcomingAppointments.length > 0" class="space-y-3 max-h-64 overflow-y-auto">
            <div
              v-for="appointment in upcomingAppointments.slice(0, 5)"
              :key="appointment.id"
              class="p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <div class="flex items-start justify-between mb-1">
                <h4 class="font-medium text-sm text-text truncate">{{ appointment.title }}</h4>
                <AppBadge :variant="typeVariants[appointment.type]" size="sm">
                  {{ typeLabels[appointment.type] }}
                </AppBadge>
              </div>

              <div class="text-xs text-text-secondary">
                <div>{{ formatDate(appointment.start_time) }}</div>
                <div>{{ formatTime(appointment.start_time) }}</div>
                <div v-if="appointment.lead_name" class="mt-1 font-medium">{{ appointment.lead_name }}</div>
              </div>
            </div>
          </div>

          <div v-else-if="!loading" class="text-center py-6">
            <svg class="w-8 h-8 text-gray-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <p class="text-sm text-text-secondary">Нет предстоящих встреч</p>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="card p-5">
          <h3 class="font-medium text-text mb-4">Быстрые действия</h3>
          <div class="space-y-2">
            <button class="w-full text-left p-2 text-sm text-text hover:bg-gray-50 rounded transition-colors">
              📞 Запланировать звонок
            </button>
            <button class="w-full text-left p-2 text-sm text-text hover:bg-gray-50 rounded transition-colors">
              🤝 Назначить встречу
            </button>
            <button class="w-full text-left p-2 text-sm text-text hover:bg-gray-50 rounded transition-colors">
              🎥 Провести демо
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>