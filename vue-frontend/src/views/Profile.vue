<template>
  <div class="min-h-screen bg-background">
    <div class="max-w-md mx-auto px-4 py-6 space-y-6">
      <!-- Profile Header -->
      <div class="card border-primary/20 p-6">
        <div class="flex flex-col items-center gap-4">
          <div class="relative">
            <div class="size-24 rounded-full border-4 border-primary/20 bg-primary/10 flex items-center justify-center text-primary text-3xl font-semibold">
              {{ initials }}
            </div>
            <button class="absolute bottom-0 right-0 size-8 rounded-full bg-primary flex items-center justify-center shadow-lg text-white">
              <CameraIcon class="size-4" />
            </button>
          </div>
          <div class="text-center">
            <h2 class="text-xl font-medium text-foreground">{{ user.profile.name }}</h2>
            <p class="text-sm text-muted-foreground">Managing well 💪</p>
          </div>
        </div>
      </div>

      <!-- Personal Information -->
      <div class="card">
        <div class="p-4 pb-2 flex items-center justify-between">
          <div>
            <h3 class="font-medium text-foreground">Personal Information</h3>
            <p class="text-sm text-muted-foreground">Manage your personal details</p>
          </div>
          <button @click="isEditing = !isEditing" class="p-2 rounded-lg hover:bg-muted transition-colors text-primary">
            <Edit2Icon class="size-4" />
          </button>
        </div>
        <div class="p-4 pt-2 space-y-4">
          <div v-for="field in formFields" :key="field.key" class="space-y-1">
            <label class="text-sm text-muted-foreground flex items-center gap-2">
              <component :is="field.icon" class="size-4" v-if="field.icon" />
              {{ field.label }}
            </label>
            <input
              :type="field.type || 'text'"
              :value="user.profile[field.key as keyof typeof user.profile]"
              @input="e => editedProfile[field.key] = (e.target as HTMLInputElement).value"
              :disabled="!isEditing"
              class="w-full px-3 py-2 border border-border rounded-lg bg-card text-sm disabled:opacity-60 focus:outline-none focus:ring-2 focus:ring-primary/40"
            />
          </div>

          <div v-if="isEditing" class="flex gap-3 pt-2">
            <button @click="saveProfile" class="btn-primary flex-1 py-2.5">Save Changes</button>
            <button @click="isEditing = false" class="flex-1 py-2.5 border border-border rounded-lg text-sm hover:bg-muted transition-colors">Cancel</button>
          </div>
        </div>
      </div>

      <!-- Health Information -->
      <div class="card">
        <div class="p-4 pb-2">
          <h3 class="font-medium text-foreground">Health Information</h3>
          <p class="text-sm text-muted-foreground">Diabetes management details</p>
        </div>
        <div class="p-4 pt-2 space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-1">
              <label class="text-xs text-muted-foreground">Diabetes Type</label>
              <p class="text-foreground text-sm font-medium">{{ user.profile.diabetesType }}</p>
            </div>
            <div class="space-y-1">
              <label class="text-xs text-muted-foreground">Diagnosed Since</label>
              <p class="text-foreground text-sm font-medium">{{ user.profile.diagnosedSince }}</p>
            </div>
            <div class="space-y-1">
              <label class="text-xs text-muted-foreground">Target Range</label>
              <p class="text-foreground text-sm font-medium">{{ user.profile.targetRangeLow }}–{{ user.profile.targetRangeHigh }} mg/dL</p>
            </div>
            <div class="space-y-1">
              <label class="text-xs text-muted-foreground">HbA1c Goal</label>
              <p class="text-foreground text-sm font-medium">&lt; {{ user.profile.hba1cGoal }}%</p>
            </div>
          </div>
          <button class="w-full mt-4 py-2.5 border border-border rounded-lg text-sm hover:bg-muted transition-colors">
            Update Health Info
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed,onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth';
import axios from '@/lib/axios';
import {
  Camera as CameraIcon,
  Edit2 as Edit2Icon,
  Mail as MailIcon,
  Phone as PhoneIcon,
  Calendar as CalendarIcon,
  MapPin as MapPinIcon,
} from 'lucide-vue-next'

const user = useUserStore()
const isEditing = ref(false)
const editedProfile = ref<Record<string, string>>({})

const initials = computed(() =>
  user.profile.name.split(' ').map(n => n[0]).join('').toUpperCase()
)

const formFields = [
  { key: 'name', label: 'Full Name', icon: null },
  { key: 'email', label: 'Email', type: 'email', icon: MailIcon },
  { key: 'phone', label: 'Phone', type: 'tel', icon: PhoneIcon },
  { key: 'dob', label: 'Date of Birth', type: 'date', icon: CalendarIcon },
  { key: 'location', label: 'Location', icon: MapPinIcon },
]

function saveProfile() {
  user.updateProfile(editedProfile.value as any)
  isEditing.value = false
  editedProfile.value = {}
}
</script>
