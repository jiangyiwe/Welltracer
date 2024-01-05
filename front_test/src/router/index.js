import { createRouter, createWebHistory } from 'vue-router'
import Ping from '../components/Ping.vue'
import FindADoctor from "@/components/features/prescription_scan.vue";
import Fitness from "@/components/features/home_fitness.vue";
import MedicationStation from "@/components/features/medication_calendar.vue";
import SelfCareCenter from "@/components/features/sleepwell.vue";
import Food from "@/components/features/scan_a_meal.vue";
import HomePage from '../components/HomePage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/ping',
      name: 'Ping',
      component: Ping
    },
    {
      path: '/homepage',
      name: 'HomePage',
      component: HomePage
    },
    {
      path: '/login',
      name: 'Login',
      component: 'Login'
    },
    {
      path: '/features/find_a_doctor',
      name: 'Find A Doctor',
      component: FindADoctor
    },

    {
      path: '/features/home_fitness',
      name: 'Fitness',
      component: Fitness
    },

    {
      path: '/features/food',
      name: 'Food',
      component: Food
    },

    {
      path: '/features/medication_station',
      name: 'Medication Station',
      component: MedicationStation
    },

    {
      path: '/features/self_care_center',
      name: 'Self Care Center',
      component: SelfCareCenter
    },

  ]
})

export default router
