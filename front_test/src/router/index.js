import { createRouter, createWebHistory } from 'vue-router'
import Ping from '../components/Ping.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/ping',
      name: 'Ping',
      component: Ping
    }
  ]
})

export default router
