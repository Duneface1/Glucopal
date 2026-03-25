import { createRouter, createWebHistory } from 'vue-router'
import Layout from '../components/layout/Layout.vue'
import Dashboard from '../views/Dashboard.vue'
import Chat from '../views/Chat.vue'
import Books from '../views/Books.vue'
import TestingRecords from '../views/TestingRecords.vue'
import Profile from '../views/Profile.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: Layout,
      children: [
        { path: '', name: 'dashboard', component: Dashboard },
        { path: 'chat', name: 'chat', component: Chat },
        { path: 'books', name: 'books', component: Books },
        { path: 'records', name: 'records', component: TestingRecords },
        { path: 'profile', name: 'profile', component: Profile },
      ],
    },
  ],
})

export default router
