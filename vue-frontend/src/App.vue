<template>
  <RouterView v-if="!auth.isAuthenticated || route.path === '/onboarding'" />

  <Layout v-else />
</template>

<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router'
import Layout from '@/components/layout/Layout.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const route = useRoute()
</script>
