import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface UserProfile {
  name: string
  email: string
  phone: string
  dob: string
  location: string
  diabetesType: string
  diagnosedSince: string
  targetRangeLow: number
  targetRangeHigh: number
  hba1cGoal: number
}

export const useUserStore = defineStore('user', () => {
  const profile = ref<UserProfile>({
    name: 'Sarah Johnson',
    email: 'sarah.johnson@email.com',
    phone: '+1 (555) 123-4567',
    dob: '1985-06-15',
    location: 'San Francisco, CA',
    diabetesType: 'Type 2',
    diagnosedSince: '2018',
    targetRangeLow: 80,
    targetRangeHigh: 130,
    hba1cGoal: 7.0,
  })

  function updateProfile(updates: Partial<UserProfile>) {
    profile.value = { ...profile.value, ...updates }
  }

  return { profile, updateProfile }
})
