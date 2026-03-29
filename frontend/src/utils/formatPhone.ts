export const formatPhone = (phone: string): string => {
  // Remove all non-digit characters
  const digits = phone.replace(/\D/g, '')

  // Russian phone number formatting
  if (digits.length === 11 && digits.startsWith('7')) {
    return `+7 (${digits.slice(1, 4)}) ${digits.slice(4, 7)}-${digits.slice(7, 9)}-${digits.slice(9)}`
  }

  if (digits.length === 10) {
    return `+7 (${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6, 8)}-${digits.slice(8)}`
  }

  // Return original if can't format
  return phone
}

export const validatePhone = (phone: string): boolean => {
  const digits = phone.replace(/\D/g, '')
  return digits.length === 10 || (digits.length === 11 && digits.startsWith('7'))
}