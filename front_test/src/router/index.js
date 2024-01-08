import { createRouter, createWebHistory } from 'vue-router'
import Ping from '@/components/Ping.vue'
import PrescriptionScan from "@/components/features/prescription_scan.vue";
import Fitness from "@/components/features/home_fitness.vue";
import MedicationCalendar from "@/components/features/medication_calendar.vue";
import Sleepwell from "@/components/features/sleepwell.vue";
import ScanAMeal from "@/components/features/scan_a_meal.vue";
import HomePage from '@/components/HomePage.vue'
import navBar from "@/components/NavBar.vue";

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
      path: '/features/home_fitness',
      name: 'Fitness',
      component: Fitness
    },

    {
      path: '/features/scan_a_meal',
      name: 'Scan A Meal',
      component: ScanAMeal
    },


    {
      path: '/features/prescription_scan',
      name: 'Prescription Scan',
      component: PrescriptionScan
    },

    {
      path: '/features/medication_calendar',
      name: 'Medication Calendar',
      component: MedicationCalendar
    },
      {
      path: '/features/sleepwell',
      name: 'Sleepwell',
      component: Sleepwell
    },

    {
      path: '/navbar',
      name: 'NavBar',
      component: navBar
    }

  ]
})

export default router
