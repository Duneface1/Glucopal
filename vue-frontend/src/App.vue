<template>
  <Layout v-if="auth.isAuthenticated"/>
  <RouterView v-else />
</template>

<script setup lang="ts">
import { RouterView, RouterLink } from 'vue-router';
import Layout from '@/components/layout/Layout.vue'
import { useAuthStore } from '@/stores/auth';

const auth = useAuthStore()
</script>
