import { createRouter, createWebHistory } from 'vue-router'
import ChatRoom from '@/components/ChatRoom.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: ChatRoom
    },
  ]
})

export default router
