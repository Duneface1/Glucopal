<template>
  <div class="min-h-full bg-background">
    <div class="max-w-md mx-auto p-4 space-y-6">
      <!-- Header -->
      <div class="space-y-1">
        <h2 class="text-xl font-medium text-foreground">Educational Library</h2>
        <p class="text-sm text-muted-foreground">Learn at your own pace with expert-curated content</p>
      </div>

      <!-- Progress Card -->
      <div class="card p-4 bg-gradient-to-br from-primary/10 to-orange-50 border-primary/20 shadow-sm">
        <div class="flex items-center justify-between">
          <div class="space-y-1">
            <div class="text-sm text-muted-foreground">Your Progress</div>
            <div class="text-2xl font-medium text-foreground">{{ completedCount }} of {{ content.length }}</div>
            <div class="text-xs text-muted-foreground">articles completed</div>
          </div>
          <div class="size-16 rounded-full border-4 border-primary flex items-center justify-center bg-background">
            <span class="text-lg font-semibold text-primary">{{ progressPercent }}%</span>
          </div>
        </div>
      </div>

      <!-- Content List -->
      <div class="space-y-3">
        <h3 class="font-medium text-foreground">Available Content</h3>

        <div
          v-for="item in content"
          :key="item.id"
          @click="toggleCompleted(item.id)"
          :class="[
            'card shadow-sm cursor-pointer transition-all hover:shadow-md',
            item.completed ? 'border-primary/30 bg-primary/5' : 'border-border'
          ]"
        >
          <div class="p-4 pb-2">
            <div class="flex items-start justify-between gap-3">
              <div class="flex gap-3 flex-1">
                <div :class="['size-10 rounded-lg flex items-center justify-center flex-shrink-0', item.completed ? 'bg-primary/20' : 'bg-muted']">
                  <component
                    :is="item.completed ? CheckCircle2Icon : BookOpenIcon"
                    :class="['size-5', item.completed ? 'text-primary' : 'text-muted-foreground']"
                  />
                </div>
                <div class="flex-1 space-y-1">
                  <h4 class="text-base font-medium text-foreground">{{ item.title }}</h4>
                  <p class="text-xs text-muted-foreground">{{ item.description }}</p>
                </div>
              </div>
            </div>
          </div>
          <div class="px-4 pb-4 pt-0 flex items-center gap-2">
            <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-muted text-muted-foreground">
              {{ item.category }}
            </span>
            <div class="flex items-center gap-1 text-xs text-muted-foreground">
              <ClockIcon class="size-3" />
              <span>{{ item.duration }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import {
  BookOpen as BookOpenIcon,
  CheckCircle2 as CheckCircle2Icon,
  Clock as ClockIcon,
} from 'lucide-vue-next'

const content = ref([
  { id: 1, title: 'Understanding Blood Glucose', description: 'Learn about blood glucose levels and what they mean for your health.', duration: '10 min read', category: 'Basics', completed: true },
  { id: 2, title: 'Healthy Eating Guide', description: 'Discover nutritious meal planning strategies for diabetes management.', duration: '15 min read', category: 'Nutrition', completed: true },
  { id: 3, title: 'Exercise and Diabetes', description: 'How physical activity affects your blood sugar and overall health.', duration: '12 min read', category: 'Lifestyle', completed: false },
  { id: 4, title: 'Medication Management', description: 'Tips for taking medications and tracking your prescriptions.', duration: '8 min read', category: 'Treatment', completed: false },
  { id: 5, title: 'Stress and Blood Sugar', description: 'Understanding the connection between stress and glucose levels.', duration: '10 min read', category: 'Mental Health', completed: false },
  { id: 6, title: 'Carb Counting 101', description: 'Master the art of counting carbohydrates for better glucose control.', duration: '20 min read', category: 'Nutrition', completed: false },
])

const completedCount = computed(() => content.value.filter(i => i.completed).length)
const progressPercent = computed(() => Math.round((completedCount.value / content.value.length) * 100))

function toggleCompleted(id: number) {
  const item = content.value.find(i => i.id === id)
  if (item) item.completed = !item.completed
}
</script>
