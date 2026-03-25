import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface GlucoseRecord {
  id: string
  value: number
  time: string
  date: string
  note?: string
  mealContext?: 'before' | 'after' | 'fasting'
}

export const useGlucoseStore = defineStore('glucose', () => {
  const records = ref<GlucoseRecord[]>([
    { id: '1', value: 120, time: '8:30 AM', date: 'Today', mealContext: 'fasting', note: 'Morning reading' },
    { id: '2', value: 145, time: '12:45 PM', date: 'Today', mealContext: 'after', note: 'After lunch' },
    { id: '3', value: 110, time: '6:15 PM', date: 'Today', mealContext: 'before' },
    { id: '4', value: 125, time: '9:20 PM', date: 'Yesterday', mealContext: 'after', note: 'Post-dinner' },
    { id: '5', value: 105, time: '7:45 AM', date: 'Yesterday', mealContext: 'fasting' },
    { id: '6', value: 130, time: '1:30 PM', date: 'Yesterday', mealContext: 'after' },
  ])

  const weeklyData = ref([
    { time: 'Mon', value: 110 },
    { time: 'Tue', value: 125 },
    { time: 'Wed', value: 118 },
    { time: 'Thu', value: 130 },
    { time: 'Fri', value: 115 },
    { time: 'Sat', value: 122 },
    { time: 'Sun', value: 120 },
  ])

  const todayRecords = computed(() => records.value.filter(r => r.date === 'Today'))
  const avgToday = computed(() => {
    const today = todayRecords.value
    if (!today.length) return 0
    return Math.round(today.reduce((sum, r) => sum + r.value, 0) / today.length)
  })
  const avgWeek = computed(() => {
    if (!records.value.length) return 0
    return Math.round(records.value.reduce((sum, r) => sum + r.value, 0) / records.value.length)
  })

  function addRecord(record: Omit<GlucoseRecord, 'id'>) {
    records.value.unshift({ ...record, id: Date.now().toString() })
  }

  function getStatusInfo(value: number) {
    if (value < 70) return { label: 'Low', colorClass: 'text-yellow-600', badgeClass: 'bg-red-100 text-red-700' }
    if (value <= 140) return { label: 'Normal', colorClass: 'text-green-600', badgeClass: 'bg-green-100 text-green-700' }
    return { label: 'High', colorClass: 'text-red-600', badgeClass: 'bg-red-100 text-red-700' }
  }

  function getMealContextLabel(ctx?: string) {
    const map: Record<string, string> = { fasting: 'Fasting', before: 'Before Meal', after: 'After Meal' }
    return ctx ? map[ctx] ?? '' : ''
  }

  return { records, weeklyData, todayRecords, avgToday, avgWeek, addRecord, getStatusInfo, getMealContextLabel }
})
