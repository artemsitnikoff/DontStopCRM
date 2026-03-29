<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { Doughnut, Bar } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from 'chart.js'
import { useDashboard } from '@/composables/useDashboard'
import StatCard from '@/components/domain/StatCard.vue'
import UpcomingTasksTable from '@/components/domain/UpcomingTasksTable.vue'
import { SOURCE_LABELS, SOURCE_COLORS, STATUS_LABELS, STATUS_COLORS } from '@/constants/leads'

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement)

const { stats, loading, error, fetchStats } = useDashboard()

// Computed values for stat cards
const newLeadsCount = computed(() => {
  if (!stats.value?.leads_by_status) return 0
  const newStatus = stats.value.leads_by_status.find(s => s.status === 'new')
  return newStatus?.count || 0
})

// Chart data
const sourceChartData = computed(() => {
  if (!stats.value?.leads_by_source) return null

  return {
    labels: stats.value.leads_by_source.map(s => SOURCE_LABELS[s.source] || s.source),
    datasets: [{
      data: stats.value.leads_by_source.map(s => s.count),
      backgroundColor: stats.value.leads_by_source.map(s => SOURCE_COLORS[s.source] || '#6B7280'),
      borderWidth: 0
    }]
  }
})

const statusChartData = computed(() => {
  if (!stats.value?.leads_by_status) return null

  return {
    labels: stats.value.leads_by_status.map(s => STATUS_LABELS[s.status] || s.status),
    datasets: [{
      data: stats.value.leads_by_status.map(s => s.count),
      backgroundColor: stats.value.leads_by_status.map(s => STATUS_COLORS[s.status] || '#6B7280'),
      borderWidth: 0
    }]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom' as const,
      labels: {
        padding: 20,
        usePointStyle: true
      }
    }
  }
}

const barChartOptions = {
  ...chartOptions,
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        stepSize: 1
      }
    }
  }
}

onMounted(() => {
  fetchStats()
})
</script>

<template>
  <div class="min-h-screen p-6" style="background-color: var(--color-bg)">
    <!-- Header -->
    <div class="mb-8">
      <div class="flex items-center space-x-3 mb-2">
        <svg class="w-8 h-8" style="color: var(--color-accent)" fill="currentColor" viewBox="0 0 24 24">
          <path d="M13 2.05v2.02c4.39.54 7.5 4.53 6.96 8.92-.39 3.18-2.78 5.57-5.96 5.96v2.02c5.5-.55 9.5-5.43 8.95-10.93C22.45 5.5 18.05 1.5 13 2.05zM11 2.05C6.5 2.6 2.5 7.48 3.05 12.98c.5 4.5 4.48 8.45 8.95 8.95v-2.02C8.82 19.43 6.5 16.9 6.5 14c0-4.14 3.36-7.5 7.5-7.5V2.05z"/>
        </svg>
        <h1 class="text-3xl font-bold" style="color: var(--color-text)">DontStopCRM</h1>
      </div>
      <p class="text-lg" style="color: var(--color-text-secondary)">Панель управления</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2" style="border-color: var(--color-accent)"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-300 text-red-700 px-4 py-3 rounded-xl mb-6">
      <div class="flex items-center justify-between">
        <span>{{ error }}</span>
        <button @click="fetchStats" class="ml-4 text-red-600 hover:text-red-800 font-medium">
          Повторить
        </button>
      </div>
    </div>

    <!-- Content -->
    <div v-else class="space-y-6">
      <!-- Stats Cards -->
      <div class="grid grid-cols-4 gap-6">
        <StatCard
          title="Всего лидов"
          :value="stats?.total_leads || 0"
          icon="users"
          color="#1929bb"
        />
        <StatCard
          title="Новые лиды"
          :value="newLeadsCount"
          icon="new"
          color="#017d0d"
        />
        <StatCard
          title="Записей сегодня"
          :value="stats?.today_bookings || 0"
          icon="calendar"
          color="#6C5CE7"
        />
        <StatCard
          title="Конверсия"
          :value="`${stats?.conversion_rate || 0}%`"
          icon="percent"
          color="#e6a23c"
        />
      </div>

      <!-- Charts -->
      <div class="grid grid-cols-2 gap-6 mt-6">
        <!-- Sources Chart -->
        <div class="bg-white rounded-xl shadow-sm p-6">
          <h3 class="text-lg font-semibold mb-4" style="color: var(--color-text)">Лиды по каналам</h3>
          <div class="h-80">
            <Doughnut
              v-if="sourceChartData"
              :data="sourceChartData"
              :options="chartOptions"
            />
            <div v-else class="h-full bg-gray-50 rounded-lg flex items-center justify-center">
              <p style="color: var(--color-text-secondary)">Нет данных</p>
            </div>
          </div>
        </div>

        <!-- Status Chart -->
        <div class="bg-white rounded-xl shadow-sm p-6">
          <h3 class="text-lg font-semibold mb-4" style="color: var(--color-text)">Лиды по статусам</h3>
          <div class="h-80">
            <Bar
              v-if="statusChartData"
              :data="statusChartData"
              :options="barChartOptions"
            />
            <div v-else class="h-full bg-gray-50 rounded-lg flex items-center justify-center">
              <p style="color: var(--color-text-secondary)">Нет данных</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Upcoming Tasks -->
      <div class="bg-white rounded-xl shadow-sm p-6 mt-6">
        <h3 class="text-lg font-semibold mb-4" style="color: var(--color-text)">Ближайшие задачи</h3>
        <UpcomingTasksTable :tasks="stats?.upcoming_tasks || []" />
      </div>
    </div>
  </div>
</template>