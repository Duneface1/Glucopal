<template>
  <RouterView v-if="!auth.isAuthenticated || route.path === '/onboarding'" />

  <Layout v-else />

    <svg class="cvd-filters" aria-hidden="true" focusable="false">
    <defs>
      <filter id="protan">
        <feColorMatrix type="matrix" values="
          0.567 0.433 0     0 0
          0.558 0.442 0     0 0
          0     0.242 0.758 0 0
          0     0     0     1 0"/>
      </filter>
      <filter id="deutan">
        <feColorMatrix type="matrix" values="
          0.625 0.375 0     0 0
          0.7   0.3   0     0 0
          0     0.3   0.7   0 0
          0     0     0     1 0"/>
      </filter>
      <filter id="tritan">
        <feColorMatrix type="matrix" values="
          0.95  0.05  0     0 0
          0     0.433 0.567 0 0
          0     0.475 0.525 0 0
          0     0     0     1 0"/>
      </filter>
    </defs>
  </svg>
</template>

<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router'
import Layout from '@/components/layout/Layout.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const route = useRoute()
</script>
