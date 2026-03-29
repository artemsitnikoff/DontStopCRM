import apiClient from './client'
import type { User, LoginRequest, RegisterRequest, TokenResponse } from '@/types/auth'

export const login = async (credentials: LoginRequest): Promise<TokenResponse> => {
  const { data } = await apiClient.post<TokenResponse>('/auth/login', credentials)
  return data
}

export const register = async (userData: RegisterRequest): Promise<TokenResponse> => {
  const { data } = await apiClient.post<TokenResponse>('/auth/register', userData)
  return data
}

export const getMe = async (): Promise<User> => {
  const { data } = await apiClient.get<User>('/auth/me')
  return data
}

export const logout = async (): Promise<void> => {
  await apiClient.post('/auth/logout')
}