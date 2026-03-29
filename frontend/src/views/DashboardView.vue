<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'
import { getStats } from '@/api/dashboard'
import type { DashboardStats } from '@/types/dashboard'

const { data: stats, loading, error, execute } = useApi<DashboardStats>()

onMounted(() => {
  execute(getStats)
})
</script>

<template>
  <div class="p-6">
    <div class="mb-6">
      <h1 class="text-2xl font-semibold text-text">Дашборд</h1>
      <p class="text-text-secondary mt-1">Обзор ключевых метрик</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-accent"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-danger bg-opacity-10 border border-red-300 text-red-700 px-4 py-3 rounded-md">
      {{ error }}
    </div>

    <!-- Content -->
    <div v-else class="space-y-6">
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <div class="card p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-accent bg-opacity-10 rounded-full flex items-center justify-center">
                <svg class="w-5 h-5 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-text-secondary truncate">Всего лидов</dt>
                <dd class="text-lg font-semibold text-text">{{ stats?.total_leads || 0 }}</dd>
              </dl>
            </div>
          </div>
        </div>

        <div class="card p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-success bg-opacity-10 rounded-full flex items-center justify-center">
                <svg class="w-5 h-5 text-success" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-text-secondary truncate">Закрытых сделок</dt>
                <dd class="text-lg font-semibold text-text">{{ stats?.won_deals || 0 }}</dd>
              </dl>
            </div>
          </div>
        </div>

        <div class="card p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-warning bg-opacity-10 rounded-full flex items-center justify-center">
                <svg class="w-5 h-5 text-warning" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                </svg>
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-text-secondary truncate">Общий доход</dt>
                <dd class="text-lg font-semibold text-text">₽{{ stats?.total_revenue?.toLocaleString() || 0 }}</dd>
              </dl>
            </div>
          </div>
        </div>

        <div class="card p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-accent-light bg-opacity-10 rounded-full flex items-center justify-center">
                <svg class="w-5 h-5 text-accent-light" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-text-secondary truncate">Конверсия</dt>
                <dd class="text-lg font-semibold text-text">{{ stats?.conversion_rate || 0 }}%</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <!-- Placeholder Charts -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="card p-6">
          <h3 class="text-lg font-medium text-text mb-4">График доходов</h3>
          <div class="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
            <p class="text-text-secondary">График будет здесь</p>
          </div>
        </div>

        <div class="card p-6">
          <h3 class="text-lg font-medium text-text mb-4">Лиды по статусам</h3>
          <div class="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
            <p class="text-text-secondary">Диаграмма будет здесь</p>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="card p-6">
        <h3 class="text-lg font-medium text-text mb-4">Последняя активность</h3>
        <div class="h-32 bg-gray-50 rounded-lg flex items-center justify-center">
          <p class="text-text-secondary">Список активности будет здесь</p>
        </div>
      </div>
    </div>
  </div>
</template>