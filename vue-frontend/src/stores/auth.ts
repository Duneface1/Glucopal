import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import axios from '@/lib/axios'

interface AuthUser {
  id: string | number
  email: string
  roles?: string[]
  [key: string]: unknown
}

interface LoginCredentials {
  email: string
  password: string
}

interface AuthResponse {
  accessToken: string
  user: AuthUser
  mfaRequired?: boolean
  mfaSessionToken?: string
}

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref<string | null>(localStorage.getItem('accessToken'))
  const user = ref<AuthUser | null>(JSON.parse(localStorage.getItem('user') || 'null'))
  const mfaPending = ref<boolean>(false)
  const mfaSessionToken = ref<string | null>(null)

  const isAuthenticated = computed(() => !!accessToken.value && !mfaPending.value)
  const requiresMfa = computed(() => mfaPending.value)

  function setAuth(token: string, userData: AuthUser) {
    accessToken.value = token
    user.value = userData
    localStorage.setItem('accessToken', token)
    localStorage.setItem('user', JSON.stringify(userData))
    localStorage.setItem('userId', String(userData.id))
  }

  function clearAuth() {
    accessToken.value = null
    user.value = null
    mfaPending.value = false
    mfaSessionToken.value = null
    localStorage.removeItem('accessToken')
    localStorage.removeItem('user')
    localStorage.removeItem('userId')
  }

  async function init(): Promise<void> {
    if (!accessToken.value) return
    try {
      const { data } = await axios.get<AuthUser>('/auth/me')
      user.value = data
      localStorage.setItem('user', JSON.stringify(data))
    } catch {
      clearAuth()
    }
  }

  async function login(credentials: LoginCredentials): Promise<{ mfaRequired: boolean }> {
    const { data } = await axios.post<AuthResponse>('/auth/login', credentials)
    if (data.mfaRequired) {
      mfaPending.value = true
      mfaSessionToken.value = data.mfaSessionToken ?? null
      return { mfaRequired: true }
    }
    setAuth(data.accessToken, data.user)
    return { mfaRequired: false }
  }

  async function verifyMfa(code: string): Promise<void> {
    const { data } = await axios.post<AuthResponse>('/auth/mfa/verify', {
      code,
      mfaSessionToken: mfaSessionToken.value,
    })
    setAuth(data.accessToken, data.user)
    mfaPending.value = false
    mfaSessionToken.value = null
  }

  async function handleOAuthCallback(code: string, provider: string): Promise<{ mfaRequired: boolean }> {
    const { data } = await axios.post<AuthResponse>('/auth/oauth/callback', { code, provider })
    if (data.mfaRequired) {
      mfaPending.value = true
      mfaSessionToken.value = data.mfaSessionToken ?? null
      return { mfaRequired: true }
    }
    setAuth(data.accessToken, data.user)
    return { mfaRequired: false }
  }

  function redirectToOAuth(provider: string): void {
    window.location.href = `${import.meta.env.VITE_API_URL}/oauth2/authorization/${provider}`
  }

  async function refreshToken(): Promise<string> {
    const { data } = await axios.post<AuthResponse>('/auth/refresh')
    setAuth(data.accessToken, data.user)
    return data.accessToken
  }

  async function logout(): Promise<void> {
    try {
      await axios.post('/auth/logout')
    } finally {
      clearAuth()
    }
  }

  return {
    user,
    accessToken,
    mfaPending,
    isAuthenticated,
    requiresMfa,
    init,
    login,
    verifyMfa,
    handleOAuthCallback,
    redirectToOAuth,
    refreshToken,
    logout,
  }
})
