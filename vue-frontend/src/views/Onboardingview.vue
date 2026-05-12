<template>
  <div class="min-h-screen bg-background flex flex-col">
    <div class="max-w-md mx-auto w-full px-4 flex flex-col flex-1 justify-center py-12 space-y-6">

      <!-- Header -->
      <div class="space-y-1 text-center">
        <div class="flex justify-center mb-4">
          <div class="size-12 rounded-2xl bg-primary/10 flex items-center justify-center">
            <DropletsIcon class="size-6 text-primary" />
          </div>
        </div>
        <h1 class="text-2xl font-bold text-foreground tracking-tight">Complete your profile</h1>
        <p class="text-sm text-muted-foreground">Help us personalise your experience</p>
      </div>

      <!-- Step indicators -->
      <div class="flex items-center justify-center gap-2">
        <div v-for="i in totalSteps" :key="i"
          :class="['h-1.5 rounded-full transition-all', i === currentStep ? 'w-8 bg-primary' : i < currentStep ? 'w-4 bg-primary/40' : 'w-4 bg-muted']" />
      </div>

      <!-- Step 1: Personal Details -->
      <div v-if="currentStep === 1" class="space-y-4">
        <div class="card p-5 space-y-4">
          <h2 class="font-medium text-foreground flex items-center gap-2">
            <UserIcon class="size-4 text-primary" /> Personal Details
          </h2>

          <div class="space-y-1.5">
            <label class="text-sm font-medium text-foreground">Full Name</label>
            <input v-model="form.name" type="text" placeholder="Jane Smith"
              class="w-full border border-border rounded-lg px-3 py-2.5 bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-primary/30" />
          </div>

          <div class="space-y-1.5">
            <label class="text-sm font-medium text-foreground">Phone <span class="text-muted-foreground font-normal">(optional)</span></label>
            <input v-model="form.phone" type="tel" placeholder="+1 234 567 8900"
              class="w-full border border-border rounded-lg px-3 py-2.5 bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-primary/30" />
          </div>

          <div class="space-y-1.5">
            <label class="text-sm font-medium text-foreground">Date of Birth <span class="text-muted-foreground font-normal">(optional)</span></label>
            <input v-model="form.dateOfBirth" type="date"
              class="w-full border border-border rounded-lg px-3 py-2.5 bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-primary/30" />
          </div>

          <div class="space-y-1.5">
            <label class="text-sm font-medium text-foreground">Location <span class="text-muted-foreground font-normal">(optional)</span></label>
            <input v-model="form.location" type="text" placeholder="City, Country"
              class="w-full border border-border rounded-lg px-3 py-2.5 bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-primary/30" />
          </div>
        </div>
      </div>

      <!-- Step 2: Diabetes Info -->
      <div v-if="currentStep === 2" class="space-y-4">
        <div class="card p-5 space-y-4">
          <h2 class="font-medium text-foreground flex items-center gap-2">
            <HeartIcon class="size-4 text-primary" /> Diabetes Information
          </h2>

          <div class="space-y-1.5">
            <label class="text-sm font-medium text-foreground">Diabetes Type</label>
            <div class="grid grid-cols-2 gap-2">
              <button v-for="type in diabetesTypes" :key="type.value"
                @click="form.diabetesType = type.value"
                :class="['py-2.5 px-3 rounded-lg border text-sm transition-colors text-left',
                  form.diabetesType === type.value
                    ? 'border-primary bg-primary/10 text-primary font-medium'
                    : 'border-border text-foreground hover:bg-muted']">
                {{ type.label }}
              </button>
            </div>
          </div>

          <div class="space-y-1.5">
            <label class="text-sm font-medium text-foreground">Year Diagnosed <span class="text-muted-foreground font-normal">(optional)</span></label>
            <input v-model="form.diagnosedYear" type="number" placeholder="e.g. 2015" min="1900" :max="new Date().getFullYear()"
              class="w-full border border-border rounded-lg px-3 py-2.5 bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-primary/30" />
          </div>
        </div>
      </div>

      <!-- Step 3: Target Goals -->
      <div v-if="currentStep === 3" class="space-y-4">
        <div class="card p-5 space-y-4">
          <h2 class="font-medium text-foreground flex items-center gap-2">
            <ActivityIcon class="size-4 text-primary" /> Target Goals
          </h2>

          <p class="text-xs text-muted-foreground">These help us calculate how well you're managing your glucose. You can update them anytime in your profile.</p>

          <div class="grid grid-cols-2 gap-3">
            <div class="space-y-1.5">
              <label class="text-sm font-medium text-foreground">Target Low (mg/dL)</label>
              <input v-model="form.targetRangeLow" type="number" placeholder="70"
                class="w-full border border-border rounded-lg px-3 py-2.5 bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-primary/30" />
            </div>
            <div class="space-y-1.5">
              <label class="text-sm font-medium text-foreground">Target High (mg/dL)</label>
              <input v-model="form.targetRangeHigh" type="number" placeholder="140"
                class="w-full border border-border rounded-lg px-3 py-2.5 bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-primary/30" />
            </div>
          </div>

          <div class="space-y-1.5">
            <label class="text-sm font-medium text-foreground">HbA1c Goal (%) <span class="text-muted-foreground font-normal">(optional)</span></label>
            <input v-model="form.hba1cGoal" type="number" step="0.1" placeholder="e.g. 7.0"
              class="w-full border border-border rounded-lg px-3 py-2.5 bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-primary/30" />
          </div>

          <p v-if="error" class="text-xs text-red-500 flex items-center gap-1.5">
            <AlertCircleIcon class="size-3.5 shrink-0" /> {{ error }}
          </p>
        </div>
      </div>

      <!-- Navigation Buttons -->
      <div class="space-y-3">
        <button @click="next" :disabled="loading || (currentStep === 1 && !form.name)"
          class="btn-primary w-full py-3">
          <span v-if="loading">Saving...</span>
          <span v-else-if="currentStep === totalSteps">Go to Dashboard →</span>
          <span v-else>Continue →</span>
        </button>

        <button v-if="currentStep > 1" @click="currentStep--"
          class="w-full text-center text-sm text-muted-foreground hover:text-foreground">
          ← Back
        </button>

        <button v-if="currentStep < totalSteps" @click="skip"
          class="w-full text-center text-sm text-muted-foreground hover:text-foreground">
          Skip for now
        </button>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from '@/lib/axios'
import {
  Droplets as DropletsIcon,
  User as UserIcon,
  Heart as HeartIcon,
  Activity as ActivityIcon,
  AlertCircle as AlertCircleIcon,
} from 'lucide-vue-next'

const router = useRouter()
const auth = useAuthStore()

const totalSteps = 3
const currentStep = ref(1)
const loading = ref(false)
const error = ref('')

const form = ref({
  name: (auth.user?.name as string) ?? '',
  phone: '',
  dateOfBirth: '',
  location: '',
  diabetesType: (auth.user?.diabetesType as string) ?? '',
  diagnosedYear: '',
  targetRangeLow: '',
  targetRangeHigh: '',
  hba1cGoal: '',
})

const diabetesTypes = [
  { value: 'TYPE_1', label: 'Type 1' },
  { value: 'TYPE_2', label: 'Type 2' },
  { value: 'GESTATIONAL', label: 'Gestational' },
  { value: 'PREDIABETES', label: 'Prediabetes' },
  { value: 'OTHER', label: 'Other' },
]

async function next() {
  if (currentStep.value < totalSteps) {
    currentStep.value++
    return
  }
  await saveAndContinue()
}

function skip() {
  if (currentStep.value < totalSteps) {
    currentStep.value++
  } else {
    router.push('/dashboard')
  }
}

async function saveAndContinue() {
  loading.value = true
  error.value = ''
  try {
    await axios.put(`/users/${auth.user?.id}/profile`, {
      name: form.value.name,
      phone: form.value.phone || null,
      dateOfBirth: form.value.dateOfBirth || null,
      location: form.value.location || null,
      diabetesType: form.value.diabetesType || null,
      diagnosedYear: form.value.diagnosedYear ? Number(form.value.diagnosedYear) : null,
      targetRangeLow: form.value.targetRangeLow ? Number(form.value.targetRangeLow) : null,
      targetRangeHigh: form.value.targetRangeHigh ? Number(form.value.targetRangeHigh) : null,
      hba1cGoal: form.value.hba1cGoal ? Number(form.value.hba1cGoal) : null,
    })

    if (auth.user) {
      auth.user = { ...auth.user, ...form.value }
    }
    router.push('/dashboard')
  } catch (e: any) {
    error.value = e?.response?.data?.error ?? 'Failed to save. You can update this in your profile later.'
  } finally {
    loading.value = false
  }
}
</script>
