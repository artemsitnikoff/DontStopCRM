<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppModal from '@/components/ui/AppModal.vue'
import KanbanColumn from '@/components/domain/KanbanColumn.vue'
import { useLeads } from '@/composables/useLeads'
import type { LeadStatus, LeadSource } from '@/types/lead'
import { STATUS_LABELS, STATUS_COLORS, SOURCE_LABELS } from '@/constants/leads'

const { leadsByStatus, loading, error, moveLeadStatus, fetchLeads, createLead } = useLeads()

onMounted(() => fetchLeads())

const columns = [
  { status: 'new' as LeadStatus, title: STATUS_LABELS.new, color: STATUS_COLORS.new },
  { status: 'contacted' as LeadStatus, title: STATUS_LABELS.contacted, color: STATUS_COLORS.contacted },
  { status: 'qualified' as LeadStatus, title: STATUS_LABELS.qualified, color: STATUS_COLORS.qualified },
  { status: 'won' as LeadStatus, title: STATUS_LABELS.won, color: STATUS_COLORS.won }
]

// Modal state
const showModal = ref(false)
const saving = ref(false)
const form = ref({
  name: '',
  phone: '',
  source: 'telegram' as LeadSource,
  first_message: ''
})

const resetForm = () => {
  form.value = { name: '', phone: '', source: 'telegram', first_message: '' }
}

const handleSave = async () => {
  if (!form.value.name.trim()) return
  saving.value = true
  try {
    await createLead({
      name: form.value.name,
      phone: form.value.phone || undefined,
      source: form.value.source,
      first_message: form.value.first_message || undefined
    })
    showModal.value = false
    resetForm()
  } catch (_err) {
    // error handled in composable
  } finally {
    saving.value = false
  }
}

const handleLeadMoved = async (leadId: number, newStatus: LeadStatus) => {
  await moveLeadStatus(leadId, newStatus)
}
</script>

<template>
  <div class="p-6">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-semibold text-black">Лиды</h1>
        <p class="text-gray-600 mt-1">Управление воронкой продаж</p>
      </div>
      <AppButton variant="primary" @click="showModal = true">
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        Добавить лида
      </AppButton>
    </div>

    <div v-if="loading" class="flex items-center justify-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2" style="border-color: var(--color-accent)"></div>
    </div>

    <div v-else-if="error" class="bg-red-50 border border-red-300 text-red-700 px-4 py-3 rounded-md">
      {{ error }}
    </div>

    <div v-else class="flex gap-6 overflow-x-auto pb-6">
      <KanbanColumn
        v-for="column in columns"
        :key="column.status"
        :title="column.title"
        :status="column.status"
        :color="column.color"
        :leads="leadsByStatus[column.status] || []"
        @lead-moved="handleLeadMoved"
      />
    </div>

    <!-- Add Lead Modal -->
    <AppModal :show="showModal" title="Новый лид" @close="showModal = false">
      <form @submit.prevent="handleSave" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Имя *</label>
          <input
            v-model="form.name"
            type="text"
            required
            class="input"
            placeholder="Имя клиента"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Телефон</label>
          <input
            v-model="form.phone"
            type="tel"
            class="input"
            placeholder="+7 916 123-45-67"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Источник</label>
          <select v-model="form.source" class="input">
            <option v-for="(label, key) in SOURCE_LABELS" :key="key" :value="key">
              {{ label }}
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Первое сообщение</label>
          <textarea
            v-model="form.first_message"
            rows="3"
            class="input"
            placeholder="Текст первого обращения клиента..."
          />
        </div>
      </form>

      <template #footer>
        <AppButton variant="secondary" @click="showModal = false">Отмена</AppButton>
        <AppButton variant="primary" @click="handleSave" :disabled="!form.name.trim() || saving">
          {{ saving ? 'Сохранение...' : 'Добавить' }}
        </AppButton>
      </template>
    </AppModal>
  </div>
</template>
