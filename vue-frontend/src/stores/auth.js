import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import axios from '@/lib/axios'
import type {User} from '@/stores/user'

export const useAuthStore = defineStore('auth', () => {


  const accessToken = ref<string | null>(null)
  const user = ref<User | null>(null)
  const mfaPending = ref(false)
  const mfaSessionToken = ref<string | null>(null)
  const isAuthenticated = computed(() => !!accessToken.value && !mfaPending.value)
  const requiresMfa = computed(() => mfaPending.value)

  async function init() {
    try {
      const { data } = await axios.post('/auth/refresh')
      accessToken.value = data.accessToken
      user.value = data.user
    } catch {
      accessToken.value = null
      user.value = null
    }
  }

  async function login(credentials: { email: string; password: string }) {
    const { data } = await axios.post('/auth/login', credentials)

    if (data.mfaRequired) {
      mfaPending.value = true
      mfaSessionToken.value = data.mfaSessionToken
      return { mfaRequired: true }
    }
    accessToken.value = data.accessToken
    user.value = data.user
    return { mfaRequired: false }
  }

  async function verifyMfa(code: string) {
    const { data } = await axios.post('/auth/mfa/verify', {
      code,
      mfaSessionToken: mfaSessionToken.value,
    })
    accessToken.value = data.accessToken
    user.value = data.user
    mfaPending.value = false
    mfaSessionToken.value = null
  }

  async function handleOAuthCallback(code: string, provider: string) {
    const { data } = await axios.post('/auth/oauth/callback', { code, provider })

    if (data.mfaRequired) {
      mfaPending.value = true
      mfaSessionToken.value = data.mfaSessionToken
      return { mfaRequired: true }
    }

    accessToken.value = data.accessToken
    user.value = data.user
    return { mfaRequired: false }
  }


  function redirectToOAuth(provider: 'google' | string) {
    window.location.href = `${import.meta.env.VITE_API_URL}/oauth2/authorization/${provider}`
  }

  async function handleSamlCallback() {
    const { data } = await axios.post('/auth/saml/callback')
    accessToken.value = data.accessToken
    user.value = data.user
  }

  function redirectToSaml() {
    window.location.href = `${import.meta.env.VITE_API_URL}/saml2/authenticate/default`
  }

  async function refreshToken(): Promise<string> {
    const { data } = await axios.post('/auth/refresh')
    accessToken.value = data.accessToken
    user.value = data.user
    return data.accessToken
  }


  async function logout() {
    try {
      await axios.post('/auth/logout')
    } finally {
      accessToken.value = null
      user.value = null
      mfaPending.value = false
      mfaSessionToken.value = null
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
    handleSamlCallback,
    redirectToSaml,
    refreshToken,
    logout,
  }
})
