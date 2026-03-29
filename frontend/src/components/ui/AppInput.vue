<script setup lang="ts">
interface Props {
  modelValue?: string | number
  type?: 'text' | 'email' | 'password' | 'tel' | 'number' | 'datetime-local'
  placeholder?: string
  disabled?: boolean
  readonly?: boolean
  error?: string
  label?: string
  required?: boolean
  autocomplete?: string
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  disabled: false,
  readonly: false,
  required: false
})

const emit = defineEmits<{
  'update:modelValue': [value: string | number]
  focus: [event: FocusEvent]
  blur: [event: FocusEvent]
}>()

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}
</script>

<template>
  <div class="w-full">
    <label v-if="label" class="block text-sm font-medium text-text mb-1">
      {{ label }}
      <span v-if="required" class="text-danger">*</span>
    </label>
    <input
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :readonly="readonly"
      :required="required"
      :autocomplete="autocomplete"
      @input="handleInput"
      @focus="emit('focus', $event)"
      @blur="emit('blur', $event)"
      class="input"
      :class="{
        'border-danger focus:border-danger focus:ring-danger': error,
        'bg-gray-50 cursor-not-allowed': disabled
      }"
    />
    <p v-if="error" class="mt-1 text-sm text-danger">
      {{ error }}
    </p>
  </div>
</template>