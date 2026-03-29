export interface User {
  id: number
  email: string
  name: string
  avatar?: string
  created_at: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  password: string
  name: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
  expires_in: number
  user: User
}